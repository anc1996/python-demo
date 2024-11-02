#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from minio import Minio
from minio.error import S3Error


class Bucket(object):
	
	client=None
	
	# __new__作用：创建对象时调用，返回对象的引用
	def __new__(cls, *args, **kwargs):
		if not cls.client:
			cls.client=object.__new__(cls)
		return cls.client
	
	def __init__(self, service, access_key, secret_key, bucket_name, secure=False):
		self.service = service
		self.bucket_name = bucket_name  # 存储 bucket_name 作为类的属性
		self.client = Minio(endpoint=service, access_key=access_key, secret_key=secret_key, secure=secure)
	
	def __exists_bucket(self,bucket_name):
		"""
		判断桶是否存在
		:param bucket_name: 桶名称
		:return:
		"""
		return self.client.bucket_exists(bucket_name=bucket_name)
	
	def exists_bucket(self):
		"""
		判断桶是否存在
		:param bucket_name: 桶名称
		:return:
		"""
		return self.__exists_bucket(bucket_name=self.bucket_name)
	
	
	def __create_bucket(self,bucket_name:str,is_policy:bool=True):
		"""
		创建桶 + 赋予策略
		:param bucket_name: 桶名
		:param is_policy: 策略
		:return:
		"""
		if self.exists_bucket(bucket_name=bucket_name):
			return False
		else:
			self.client.make_bucket(bucket_name=bucket_name)
			return True
		
	def create_bucket(self,is_policy:bool=True):
		"""
		创建桶 + 赋予策略
		:param is_policy: 策略
		:return:
		"""
		return self.__create_bucket(bucket_name=self.bucket_name,is_policy=is_policy)
		
	def get_bucket_list(self):
		"""
		获取桶列表
		:return:
		"""
		buckets=self.client.list_buckets()
		bucket_list=[]
		for bucket in buckets:
			bucket_list.append({"bucket_name":bucket.name,"create_time":bucket.creation_date})
			
		return bucket_list
	
	def __remove_bucket(self,bucket_name):
		"""
		删除桶
		:param bucket_name:
		:return:
		"""
		try:
			self.client.remove_bucket(bucket_name=bucket_name)
		except S3Error as e:
			print("[error]:",e)
			return False
		return True
	
	def remove_bucket(self):
		"""
		删除桶
		:return:
		"""
		return self.__remove_bucket(bucket_name=self.bucket_name)
	
	def __bucket_list_files(self,bucket_name,prefix):
		"""
		列出桶中文件
		:param bucket_name:同名
		:param prefix:前缀
		:return:
		"""
		return self.client.list_objects(bucket_name=bucket_name,prefix=prefix)
	
	def bucket_list_files(self,prefix):
		"""
		列出桶中文件
		"""
		return self.__bucket_list_files(bucket_name=self.bucket_name,prefix=prefix)
	
	
	def __download_file(self, bucket_name, bucket_source_file, local_file_path, stream=1024 * 32):
		"""
		下载文件
		:param bucket_name: 桶名
		:param file: 文件名
		:param file_path: 文件路径
		:param stream: 流大小
		:return: 成功返回 True，失败返回 False 并打印错误信息
		"""
		try:
			# 获取对象数据
			# 返回的对象可以被读取，通常用于在内存中处理数据或流式传输数据。
			data = self.client.get_object(bucket_name=bucket_name, object_name=bucket_source_file)
			# 使用 with 语句管理文件资源
			with open(local_file_path, "wb") as file_data:
				for d in data.stream(stream):
					file_data.write(d)
		except S3Error as e:
			print(f"[error]: {e}")
			return False
		except Exception as e:
			print(f"[error]: An unexpected error occurred: {e}")
			return False
		return True
	
	def download_file(self, bucket_source_file, local_file_path):
		"""
		下载文件
		:param bucket_name:
		:return True or False
		"""
		return self.__download_file(bucket_name=self.bucket_name, bucket_source_file=bucket_source_file,
		                             local_file_path=local_file_path)
	
	def __fget_object(self,bucket_name,bucket_source_file,local_file_path):
		"""
		下载文件
		:param bucket_name: 桶名
		:param file: 文件名
		:param file_path: 文件路径
		:return:
		"""
		try:
			# 这个方法直接将对象下载并保存到指定的本地文件路径。它会创建一个新的本地文件（如果不存在）或覆盖现有文件。
			self.client.fget_object(bucket_name=bucket_name,object_name=bucket_source_file,file_path=local_file_path)
		except S3Error as e:
			print("[error]:",e)
			return False
		except Exception as e:
			print("[error]:",e)
			return False
		return True
	
	def fget_object(self,bucket_source_file,local_file_path):
		return self.__fget_object(bucket_name=self.bucket_name,bucket_source_file=bucket_source_file,local_file_path=local_file_path)
		
	def __copy_file(self,bucket_name,file,file_path):
		"""
		复制文件
		:param bucket_name: 桶名
		:param file: 文件名
		:param file_path: 文件路径
		:return:
		"""
		try:
			self.client.copy_object(bucket_name=bucket_name,object_name=file,new_bucket_name=bucket_name,new_object_name=file_path)
		except S3Error as e:
			print("[error]:",e)
			return False
		except Exception as e:
			print("[error]:",e)
			return False
		return True
	
	def copy_file(self,file,file_path):
		return self.__copy_file(bucket_name=self.bucket_name,file=file,file_path=file_path)
		
	def __upload_file(self,bucket_name,bucket_file_name,local_file_path,content_type):
		"""
		上传文件
		:param bucket_name: 桶名
		:param file: 文件名
		:param file_path: 文件路径
		:param content_type: 文件类型
		:return:
		"""
		try:
			with open(local_file_path, "rb") as file_data:
				# 获取文件大小
				file_stat=os.stat(local_file_path)
				self.client.put_object(bucket_name=bucket_name,object_name=bucket_file_name,data=file_data,length=file_stat.st_size,content_type=content_type)
		except S3Error as e:
			print("[error]:",e)
			return False
		return True
		
	def upload_file(self,local_file_path,bucket_file_name,content_type):
		return self.__upload_file(bucket_name=self.bucket_name,bucket_file_name=bucket_file_name,local_file_path=local_file_path,content_type=content_type)
		
	def __fput_file(self,bucket_name,bucket_file_name,source_file):
		"""

		上传文件
		:param bucket_name: 桶名
		:param file: 文件名
		:param file_path: 文件路径
		:return:
		bucket_name=bucket_name,
	                          destination_file='/files/article/content/list.txt',
	                          source_file=source_file)
		"""
		
		try:
			self.client.fput_object(bucket_name=bucket_name,object_name=bucket_file_name,file_path=source_file)
		except S3Error as e:
			print("[error]:",e)
			return False
		return True
	
	def fput_file(self,source_file,bucket_file_name):
		return self.__fput_file(bucket_name=self.bucket_name,bucket_file_name=bucket_file_name,source_file=source_file)
	
		
	def __flask_upload_file(self,bucket_name,bucket_file,data):
		"""
		:param bucket_name:
		:param bucket_file: 文件名
		:param data: 文件数据
		:return:
		"""
		try:
			self.client.put_object(bucket_name=bucket_name,object_name=bucket_file,data=data,length=-1,part_size=10*1024*1024)
		except S3Error as e:
			print("[error]:",e)
			return False
		return True
	
	def flask_upload_file(self,bucket_file,data):
		return self.__flask_upload_file(bucket_name=self.bucket_name,bucket_file=bucket_file,data=data)
	
	
	def __flask_read_file(self,bucket_name,bucket_file):
		"""
		读取文件
		:param bucket_name: 桶名
		:param bucket_file: 文件名
		:return:
		"""
		try:
			data=self.client.get_object(bucket_name=bucket_name,object_name=bucket_file)
		except S3Error as e:
			print("[error]:",e)
			data=None
		return data
	
	def flask_read_file(self,bucket_file):
		return self.__flask_read_file(bucket_name=self.bucket_name,bucket_file=bucket_file)
	
	
	def __stat_object(self,bucket_name,bucket_file):
		"""
		获取文件信息
		:param bucket_name: 桶名
		:param bucket_file: 文件名
		:return:
		"""
		content=None
		try:
			data=self.client.stat_object(bucket_name=bucket_name,object_name=bucket_file)
			content={
				'content_type':data.content_type,
				'last_modified':data.last_modified,
				'bucker_name':data.bucket_name,
				'object_name':data.object_name,
				'etag':data.etag,# 文件的MD5哈希值
				'metadata':data.metadata,# 文件元数据
				'version_id':data.version_id# 文件版本号
			}
		except S3Error as e:
			print("[error]:",e)
			content=None
		
		return content
	
	def stat_object(self,bucket_file):
		return self.__stat_object(bucket_name=self.bucket_name,bucket_file=bucket_file)
	
	def __remove_file(self,bucket_name,bucket_file):
		"""
		删除文件
		:param bucket_name: 桶名
		:param bucket_file: 文件名
		:return:
		"""
		try:
			self.client.remove_object(bucket_name=bucket_name,object_name=bucket_file)
		except S3Error as e:
			print("[error]:",e)
			return False
		except Exception as e:
			print("[error]:",e)
			return False
		return True
	
	def remove_file(self,bucket_file):
		return self.__remove_file(bucket_name=self.bucket_name,bucket_file=bucket_file)
	
	
	def __get_Url(self,bucket_name,bucket_file):
		"""
		获取文件的url
		:param bucket_name: 桶名
		:param bucket_file: 文件名
		:return:
		"""
		try:
			url=self.client.presigned_get_object(bucket_name=bucket_name,object_name=bucket_file)
		except S3Error as e:
			print("[error]:",e)
			url=None
		return url
	
	def get_Url(self,bucket_file):
		return self.__get_Url(bucket_name=self.bucket_name,bucket_file=bucket_file)
		

		
		