"""
中间件用于处理应用程序启动时的初始化任务
"""

import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)


class DisableProxyMiddleware:
	"""
	禁用代理中间件
	用于确保应用程序不使用代理连接到MongoDB和MinIO
	"""
	
	def __init__(self, get_response):
		"""初始化中间件"""
		self.get_response = get_response
		
		# 在应用程序启动时执行一次
		self._disable_proxy()
		
		# 初始化MongoDB连接和索引
		self._setup_mongodb()
	
	def __call__(self, request):
		"""处理请求"""
		# 代码仅在应用程序启动时执行一次，不需要在每个请求上执行
		response = self.get_response(request)
		return response
	
	def _disable_proxy(self):
		"""禁用代理设置"""
		try:
			# 保存原始代理设置
			self._original_proxy = {
				'HTTP_PROXY': os.environ.pop('HTTP_PROXY', None),
				'HTTPS_PROXY': os.environ.pop('HTTPS_PROXY', None),
				'http_proxy': os.environ.pop('http_proxy', None),
				'https_proxy': os.environ.pop('https_proxy', None),
			}
			
			# 设置NO_PROXY为通配符
			os.environ['NO_PROXY'] = '*'
			logger.info("已禁用代理设置")
		except Exception as e:
			logger.error(f"禁用代理设置失败: {e}")
	
	def _setup_mongodb(self):
		"""
		设置MongoDB连接和索引
		仅在应用程序启动时执行一次
		"""
		try:
			from blog.utils import get_mongo_db
			
			# 获取MongoDB连接
			mongo_db = get_mongo_db()
			if not mongo_db:
				logger.error("无法连接到MongoDB，索引创建失败")
				return
			
			# 获取博客内容集合
			collection = mongo_db['blog_contents']
			
			# 检查索引是否已存在
			existing_indexes = list(collection.list_indexes())
			has_text_index = any('text' in idx.get('name', '') for idx in existing_indexes)
			
			if has_text_index:
				logger.info("MongoDB文本索引已经存在")
			else:
				# 创建文本索引，用于全文搜索
				# 为标题和内容字段设置不同的权重
				index_result = collection.create_index(
					[
						('title', 'text'),
						('plain_text', 'text'),
						('stream_data.value', 'text')
					],
					weights={
						'title': 10,
						'plain_text': 5,
						'stream_data.value': 1
					},
					name='blog_content_text_search',
					default_language='chinese'  # 设置默认语言为中文
				)
				logger.info(f"创建MongoDB文本索引成功: {index_result}")
			
			# 创建page_id索引，用于快速查找
			id_indexes = [idx for idx in existing_indexes if 'page_id' in idx.get('name', '')]
			if not id_indexes:
				id_index = collection.create_index('page_id', unique=True)
				logger.info(f"创建MongoDB page_id索引成功: {id_index}")
			else:
				logger.info("MongoDB page_id索引已经存在")
		
		except Exception as e:
			logger.error(f"MongoDB索引设置失败: {e}")