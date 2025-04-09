#!/user/bin/env python3
# -*- coding: utf-8 -*-
# blog/minio_utils.py
import io
import boto3
from django.conf import settings


def get_minio_client():
	"""获取MinIO客户端"""
	try:
		client = boto3.client(
			's3',
			endpoint_url=settings.AWS_S3_ENDPOINT_URL,
			aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
		)
		# 测试连接
		client.list_buckets()
		print("MinIO连接成功")
		return client
	except Exception as e:
		print(f"MinIO连接失败: {e}")
		return None


def upload_file_to_minio(file_obj, object_name, content_type=None):
	"""上传文件到MinIO"""
	s3_client = get_minio_client()
	if not s3_client:
		print("MinIO客户端不可用")
		return False
	
	try:
		# 如果是文件对象
		if hasattr(file_obj, 'read'):
			s3_client.upload_fileobj(
				file_obj,
				settings.AWS_STORAGE_BUCKET_NAME,
				object_name,
				ExtraArgs={'ContentType': content_type} if content_type else None
			)
		# 如果是文本内容
		else:
			s3_client.upload_fileobj(
				io.BytesIO(file_obj.encode('utf-8')),
				settings.AWS_STORAGE_BUCKET_NAME,
				object_name,
				ExtraArgs={'ContentType': 'text/plain'}
			)
		return True
	except Exception as e:
		print(f"上传到MinIO失败: {e}")
		return False


def get_file_from_minio(object_name):
	"""从MinIO获取文件"""
	s3_client = get_minio_client()
	if not s3_client:
		print("MinIO客户端不可用")
		return None
	
	try:
		response = s3_client.get_object(
			Bucket=settings.AWS_STORAGE_BUCKET_NAME,
			Key=object_name
		)
		return response['Body'].read()
	except Exception as e:
		print(f"从MinIO获取文件失败: {e}")
		return None


# 初始化时检查并创建必要的桶
def check_and_create_buckets():
	client = get_minio_client()
	if not client:
		return
	
	try:
		buckets = [bucket['Name'] for bucket in client.list_buckets()['Buckets']]
		
		if settings.MINIO_MEDIA_BUCKET not in buckets:
			print(f"创建媒体桶: {settings.MINIO_MEDIA_BUCKET}")
			client.create_bucket(Bucket=settings.MINIO_MEDIA_BUCKET)
		
		if settings.MINIO_STATIC_BUCKET not in buckets:
			print(f"创建静态文件桶: {settings.MINIO_STATIC_BUCKET}")
			client.create_bucket(Bucket=settings.MINIO_STATIC_BUCKET)
	except Exception as e:
		print(f"检查和创建桶失败: {e}")


# 尝试初始化桶
check_and_create_buckets()