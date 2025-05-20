#!/user/bin/env python3
# -*- coding: utf-8 -*-
# wagtailblog/utils/mongo.py
import pymongo
import json,logging
from django.conf import settings
from bson import ObjectId, json_util
from datetime import datetime

# 设置日志记录器
logger = logging.getLogger(__name__)

class MongoManager:
	"""MongoDB 操作管理类"""
	
	_instance = None
	
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(MongoManager, cls).__new__(cls)
			cls._instance._connect()
		return cls._instance
	
	# 修改_connect方法，添加日志
	def _connect(self):
		"""连接到 MongoDB"""
		mongo_settings = settings.MONGO_DB
		try:
			client = pymongo.MongoClient(
				host=mongo_settings['HOST'],
				port=mongo_settings['PORT']
			)
			self.db = client[mongo_settings['NAME']]
			# 创建博客内容集合
			self.blog_content = self.db['blog_content']
			logger.info("MongoDB连接成功")
		except Exception as e:
			logger.error(f"MongoDB连接失败: {e}")
			raise
	
	def _prepare_for_mongo(self, data):
		"""
			将数据准备为可存储到MongoDB的格式
			处理StreamField的RawDataView对象和其他不可直接序列化的类型
		"""
		if isinstance(data, dict):
			result = {}
			for key, value in data.items():
				result[key] = self._prepare_for_mongo(value)
			return result
		elif isinstance(data, list):
			return [self._prepare_for_mongo(item) for item in data]
		elif hasattr(data, 'isoformat') and callable(data.isoformat):
			# 处理日期时间对象
			return data.isoformat()
		elif hasattr(data, 'raw_data') and callable(getattr(data, 'raw_data')):
			# 处理StreamValue对象
			return self._prepare_for_mongo(data.raw_data)
		elif hasattr(data, '__iter__') and not isinstance(data, (str, bytes)):
			# 处理其他可迭代对象
			return [self._prepare_for_mongo(item) for item in data]
		else:
			# 处理基本类型
			return data
	
	def save_blog_content(self, content_data, content_id=None):
		"""保存博客内容到 MongoDB"""
		# 预处理数据，确保所有数据都是MongoDB可序列化的
		prepared_data = self._prepare_for_mongo(content_data)
		
		# 添加时间戳
		prepared_data['updated_at'] = datetime.now().isoformat()
		
		if content_id:
			# 更新现有内容
			try:
				mongo_id = ObjectId(content_id)
				self.blog_content.update_one(
					{'_id': mongo_id},
					{'$set': prepared_data}
				)
				return str(content_id)
			except Exception as e:
				print(f"MongoDB更新错误: {e}")
				# 如果更新失败，尝试创建新文档
				result = self.blog_content.insert_one(prepared_data)
				return str(result.inserted_id)
		else:
			# 创建新内容
			try:
				result = self.blog_content.insert_one(prepared_data)
				return str(result.inserted_id)
			except Exception as e:
				print(f"MongoDB插入错误: {e}")
				# 尝试更严格的JSON序列化
				json_str = json.dumps(prepared_data, default=json_util.default)
				clean_data = json.loads(json_str)
				result = self.blog_content.insert_one(clean_data)
				return str(result.inserted_id)
	
	def get_blog_content(self, content_id):
		"""从 MongoDB 获取博客内容"""
		if not content_id:
			return None
		
		try:
			mongo_id = ObjectId(content_id)
			content = self.blog_content.find_one({'_id': mongo_id})
			return content
		except Exception as e:
			print(f"MongoDB获取错误: {e}")
			return None
	
	def delete_blog_content(self, content_id):
		"""从 MongoDB 删除博客内容"""
		if not content_id:
			return False
		
		try:
			mongo_id = ObjectId(content_id)
			result = self.blog_content.delete_one({'_id': mongo_id})
			return result.deleted_count > 0
		except Exception as e:
			print(f"MongoDB删除错误: {e}")
			return False
	
	def search_blog_content(self, query):
		"""在 MongoDB 中搜索博客内容"""
		try:
			# 创建文本索引（如果尚未创建）
			self.blog_content.create_index([('title', 'text'), ('intro', 'text')])
			
			# 执行文本搜索
			results = self.blog_content.find(
				{'$text': {'$search': query}},
				{'score': {'$meta': 'textScore'}}
			).sort([('score', {'$meta': 'textScore'})])
			
			return list(results)
		except Exception as e:
			print(f"MongoDB搜索错误: {e}")
			# 如果文本搜索失败，尝试基本查询
			results = self.blog_content.find({
				'$or': [
					{'title': {'$regex': query, '$options': 'i'}},
					{'intro': {'$regex': query, '$options': 'i'}}
				]
			})
			return list(results)