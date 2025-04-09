#!/user/bin/env python3
# -*- coding: utf-8 -*-



try:
	from wagtail.search.backends.elasticsearch7 import Elasticsearch7SearchBackend
	from .mongodb_utils import page_content_collection
	
	class CustomElasticsearchBackend(Elasticsearch7SearchBackend):
		"""自定义Elasticsearch后端，处理MongoDB内容"""
		
		def add(self, obj):
			"""添加对象到索引"""
			# 确保MongoDB中的内容被索引
			if hasattr(obj, 'mongo_content_id') and obj.mongo_content_id:
				try:
					mongo_id = obj.mongo_content_id
					mongo_doc = page_content_collection.find_one({'_id': mongo_id})
					if mongo_doc:
						# 临时设置内容以便索引
						original_body = obj.body
						obj.body = mongo_doc.get('content', '')
						super().add(obj)
						# 恢复原始引用
						obj.body = original_body
						return
				except Exception as e:
					print(f"索引MongoDB内容失败: {e}")
			
			# 默认处理
			super().add(obj)
except ImportError:
	# 如果Elasticsearch不可用，使用基本搜索后端
	from wagtail.search.backends.database import DatabaseSearchBackend
	
	
	class CustomElasticsearchBackend(DatabaseSearchBackend):
		pass