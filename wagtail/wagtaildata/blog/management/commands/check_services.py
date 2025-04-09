#!/user/bin/env python3
# -*- coding: utf-8 -*-
# blog/management/commands/check_services.py
from django.core.management.base import BaseCommand
import pymongo
import boto3
import requests
from django.conf import settings
import mysql.connector


class Command(BaseCommand):
	help = '检查所有服务是否正常工作'
	
	def handle(self, *args, **options):
		self.stdout.write('开始检查服务状态...')
		
		# 检查MySQL
		self.check_mysql()
		
		# 检查MongoDB
		self.check_mongodb()
		
		# 检查MinIO
		self.check_minio()
		
		# 检查Elasticsearch
		self.check_elasticsearch()
		
		self.stdout.write(self.style.SUCCESS('检查完成!'))
	
	def check_mysql(self):
		self.stdout.write('检查MySQL连接...')
		try:
			conn = mysql.connector.connect(
				host=settings.DATABASES['default']['HOST'],
				user=settings.DATABASES['default']['USER'],
				password=settings.DATABASES['default']['PASSWORD'],
				database=settings.DATABASES['default']['NAME']
			)
			if conn.is_connected():
				self.stdout.write(self.style.SUCCESS('MySQL连接成功!'))
				conn.close()
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'MySQL连接失败: {e}'))
	
	def check_mongodb(self):
		self.stdout.write('检查MongoDB连接...')
		try:
			client = pymongo.MongoClient(f'mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/')
			client.server_info()
			self.stdout.write(self.style.SUCCESS('MongoDB连接成功!'))
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'MongoDB连接失败: {e}'))
	
	def check_minio(self):
		self.stdout.write('检查MinIO连接...')
		try:
			s3 = boto3.client(
				's3',
				endpoint_url=settings.AWS_S3_ENDPOINT_URL,
				aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
				aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			buckets = s3.list_buckets()
			self.stdout.write(self.style.SUCCESS(f'MinIO连接成功! 存储桶: {[b["Name"] for b in buckets["Buckets"]]}'))
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'MinIO连接失败: {e}'))
	
	def check_elasticsearch(self):
		self.stdout.write('检查Elasticsearch连接...')
		try:
			url = settings.WAGTAILSEARCH_BACKENDS['default']['URLS'][0]
			response = requests.get(url)
			if response.status_code == 200:
				self.stdout.write(self.style.SUCCESS('Elasticsearch连接成功!'))
			else:
				self.stdout.write(self.style.WARNING(f'Elasticsearch返回状态码: {response.status_code}'))
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'Elasticsearch连接失败: {e}'))