#!/user/bin/env python3
# -*- coding: utf-8 -*-
# blog/management/commands/setup_minio.py
import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3


class Command(BaseCommand):
	help = '设置MinIO存储桶并迁移现有媒体文件'
	
	def add_arguments(self, parser):
		parser.add_argument(
			'--migrate',
			action='store_true',
			help='迁移现有media文件到MinIO',
		)
		
		parser.add_argument(
			'--cleanup',
			action='store_true',
			help='迁移后删除本地文件（谨慎使用）',
		)
	
	def handle(self, *args, **options):
		# 创建S3客户端(连接MinIO)
		s3_client = boto3.client(
			's3',
			endpoint_url=settings.AWS_S3_ENDPOINT_URL,
			aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			region_name='us-east-1',  # MinIO默认区域
			verify=False,  # 本地开发不验证SSL
		)
		
		bucket_name = settings.AWS_STORAGE_BUCKET_NAME
		
		# 检查存储桶是否存在
		try:
			s3_client.head_bucket(Bucket=bucket_name)
			self.stdout.write(self.style.SUCCESS(f'存储桶 {bucket_name} 已存在'))
		except:
			# 创建存储桶
			try:
				s3_client.create_bucket(Bucket=bucket_name)
				self.stdout.write(self.style.SUCCESS(f'已创建存储桶 {bucket_name}'))
			except Exception as e:
				self.stdout.write(self.style.ERROR(f'创建存储桶失败: {e}'))
				return
		
		# 设置桶策略为公开读取（使图片和文档可以直接访问）
		if getattr(settings, 'AWS_DEFAULT_ACL', None) == 'public-read':
			try:
				# 设置存储桶策略
				bucket_policy = {
					'Version': '2012-10-17',
					'Statement': [
						{
							'Sid': 'PublicReadGetObject',
							'Effect': 'Allow',
							'Principal': '*',
							'Action': ['s3:GetObject'],
							'Resource': [f'arn:aws:s3:::{bucket_name}/*']
						}
					]
				}
				# 将策略转换为JSON字符串
				s3_client.put_bucket_policy(
					Bucket=bucket_name,
					Policy=json.dumps(bucket_policy)
				)
				self.stdout.write(self.style.SUCCESS(f'已设置存储桶 {bucket_name} 为公开读取'))
			except Exception as e:
				self.stdout.write(self.style.WARNING(f'设置桶策略失败: {e}'))
		
		# 如果指定了--migrate参数，则迁移现有文件
		if options['migrate']:
			self.migrate_media_files(s3_client, bucket_name, options['cleanup'])
	
	def migrate_media_files(self, s3_client, bucket_name, cleanup=False):
		"""迁移media目录下的文件到MinIO"""
		self.stdout.write('开始迁移media文件到MinIO...')
		
		# 获取MEDIA_ROOT路径
		media_root = settings.MEDIA_ROOT
		if not os.path.exists(media_root):
			self.stdout.write(self.style.ERROR(f'媒体目录不存在: {media_root}'))
			return
		
		# 计数器
		success_count = 0
		error_count = 0
		
		# 遍历媒体目录
		for root, dirs, files in os.walk(media_root):
			for filename in files:
				# 完整文件路径
				local_path = os.path.join(root, filename)
				# 相对于MEDIA_ROOT的路径
				relative_path = os.path.relpath(local_path, media_root)
				# MinIO中的键名
				minio_key = relative_path.replace('\\', '/')
				
				try:
					# 检查文件是否已存在于MinIO中
					try:
						s3_client.head_object(Bucket=bucket_name, Key=minio_key)
						self.stdout.write(f'已存在，跳过: {relative_path}')
						continue
					except:
						pass  # 文件不存在，继续上传
					
					self.stdout.write(f'上传: {relative_path}')
					# 上传文件到MinIO
					with open(local_path, 'rb') as file_data:
						s3_client.upload_fileobj(
							file_data,
							bucket_name,
							minio_key
						)
					success_count += 1 # 成功计数
					
					# 如果指定了cleanup，则删除本地文件
					if cleanup:
						os.remove(local_path)
						self.stdout.write(f'已删除本地文件: {relative_path}')
				
				except Exception as e:
					self.stdout.write(self.style.ERROR(f'上传失败 {relative_path}: {e}'))
					error_count += 1
		
		# 删除空目录（如果指定了cleanup）
		if cleanup:
			for root, dirs, files in os.walk(media_root, topdown=False):
				for dir_name in dirs:
					dir_path = os.path.join(root, dir_name)
					if not os.listdir(dir_path):  # 检查目录是否为空
						os.rmdir(dir_path)
						self.stdout.write(f'已删除空目录: {os.path.relpath(dir_path, media_root)}')
		
		self.stdout.write(self.style.SUCCESS(
			f'迁移完成: 成功 {success_count} 个文件, 失败 {error_count} 个文件'
		))