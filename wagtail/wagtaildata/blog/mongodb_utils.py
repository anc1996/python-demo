#!/user/bin/env python3
# -*- coding: utf-8 -*-

# blog/mongodb_utils.py
import pymongo
from django.conf import settings


# 创建一个空的集合对象作为回退
class MockCollection:
	def find_one(self, *args, **kwargs):
		return {"content": "MongoDB连接失败，这是一个临时内容"}
	
	def update_one(self, *args, **kwargs):
		print("MongoDB连接失败，无法更新内容")
	
	def delete_one(self, *args, **kwargs):
		print("MongoDB连接失败，无法删除内容")

# MongoDB连接
try:
	mongo_client = pymongo.MongoClient(
		f'mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/',
		serverSelectionTimeoutMS=3000  # 3秒超时
	)
	mongo_client.server_info() # 测试连接
	mongo_db = mongo_client[settings.MONGODB_NAME]
	page_content_collection = mongo_db[settings.MONGODB_COLLECTION]
	print("MongoDB连接成功")
except Exception as e:
	print(f"MongoDB连接失败: {e}")
	page_content_collection = MockCollection()