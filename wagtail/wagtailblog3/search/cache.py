# search/cache.py
from django.core.cache import cache
import hashlib
import json


class SearchCache:
	"""搜索缓存管理"""
	
	@staticmethod
	def get_cache_key(query, search_type='all', page=1):
		"""生成缓存键"""
		key_string = f"search:{query}:{search_type}:{page}"
		return hashlib.md5(key_string.encode()).hexdigest()
	
	@staticmethod
	def get_cached_results(query, search_type='all', page=1):
		"""获取缓存的搜索结果"""
		cache_key = SearchCache.get_cache_key(query, search_type, page)
		return cache.get(cache_key)
	
	@staticmethod
	def set_cached_results(query, results, search_type='all', page=1, timeout=300):
		"""设置搜索结果缓存，默认5分钟过期"""
		cache_key = SearchCache.get_cache_key(query, search_type, page)
		cache.set(cache_key, results, timeout)
	
	@staticmethod
	def clear_search_cache():
		"""清除所有搜索缓存"""
		cache.delete_pattern("search:*")