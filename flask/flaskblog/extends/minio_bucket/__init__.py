#!/user/bin/env python3
# -*- coding: utf-8 -*-
from extends.minio_bucket.bucket import Bucket
from settings import Config


flask_bucket=Bucket(service=Config.MINIO_SERVICE,access_key=Config.MINIO_ACCESS_KEY,
              secret_key=Config.MINIO_SECRET,
              bucket_name=Config.MINIO_BUCKET,
              secure=Config.MINIO_SECURE)




# print(flask_bucket.get_bucket_list())
# # 获取文件信息
# print(flask_bucket.stat_object(bucket_file='/files/article/content/list.txt'))
# # 下载文件
# print(flask_bucket.fget_object(bucket_source_file='/files/article/content/list.txt',destination_file_name='/root/list.txt'))

# print(flask_bucket.get_Url(bucket_file='images/user/icon/Flask_logo2.png'))
#
# class flask_bucket(object):
#
# 	def __init__(self,bucket_name):
# 		self.bucket = Bucket(service=Config.MINIO_SERVICE,access_key=Config.MINIO_ACCESS_KEY,
# 	                secret_key=Config.MINIO_SECRET,secure=Config.MINIO_SECURE)
# 		self.bucket_name = bucket_name
#
# 	# 上传文件
# 	def upload_file(self,bucket_file,data):
# 		"""
# 		上传文件,存在
# 		:param object_name: 文件名
# 		:param data: 文件数据
# 		:param bucket_file: 存在minio哪个位置。
# 		:return:
# 		"""
# 		return self.bucket.flask_upload_file(bucket_name=self.bucket_name,bucket_file=bucket_file,data=data)
#
# 	# 下载文件
# 	def get_object(self,bucket_file):
# 		"""
# 		下载文件
# 		:param object_name: 文件名
# 		:return:
# 		"""
# 		return self.bucket.client.get_object(bucket_name=self.bucket_name,object_name=bucket_file)
#
# flask_bucket=flask_bucket(Config.MINIO_BUCKET)