#!/user/bin/env python3
# -*- coding: utf-8 -*-
# wagtailblog/search.py
from wagtail.search.backends.database.fallback import DatabaseSearchBackend
from utils.mongo import MongoManager
from wagtail.models import Page


class CustomSearchBackend(DatabaseSearchBackend):
	"""自定义搜索后端，结合 MySQL 和 MongoDB 搜索"""
	
	def __init__(self, params):
		super().__init__(params)
		self.mongo = MongoManager()
	
	def search(self, query, model_or_queryset, fields=None, operator=None, order_by_relevance=True, partial_match=True,
	           **kwargs):
		"""实现混合搜索"""
		# 首先使用 Wagtail 的标准搜索
		standard_results = super().search(
			query,
			model_or_queryset,
			fields=fields,
			operator=operator,
			order_by_relevance=order_by_relevance,
			partial_match=partial_match,
			**kwargs
		)
		
		# 如果搜索的不是页面模型，直接返回标准结果
		if not issubclass(model_or_queryset.model if hasattr(model_or_queryset, 'model') else model_or_queryset, Page):
			return standard_results
		
		# 在 MongoDB 中搜索
		mongo_results = self.mongo.search_blog_content(query)
		
		# 提取所有找到的页面 ID
		mongo_page_ids = [result.get('page_id') for result in mongo_results if result.get('page_id')]
		
		# 如果有 MongoDB 结果，合并到查询集中
		if mongo_page_ids:
			# 获取这些页面
			mongo_pages = Page.objects.filter(id__in=mongo_page_ids)
			
			# 合并结果集
			# 注意：这种简单合并可能需要根据实际情况调整
			combined_results = list(standard_results)
			
			# 添加 MongoDB 找到但标准搜索没找到的页面
			for page in mongo_pages:
				if page not in combined_results:
					combined_results.append(page)
			
			# 返回合并后的结果
			# 这里的排序可能需要自定义
			return combined_results
		
		# 如果没有 MongoDB 结果，返回标准结果
		return standard_results