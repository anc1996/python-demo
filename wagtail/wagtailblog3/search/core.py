# search/core.py
from wagtail.models import Page
from blog.models import BlogPage
from wagtail.contrib.search_promotions.models import Query
from django.db.models import Count, QuerySet
import logging,traceback

logger = logging.getLogger(__name__)


def perform_search(query_string, search_type='all', page_number=1, per_page=10):
	"""
	执行搜索并返回结果

	参数:
		query_string: 搜索关键词
		search_type: 搜索类型 (all, blog, pages)
		page_number: 页码
		per_page: 每页结果数

	返回:
		搜索结果对象 (QuerySet)
	"""
	
	# 初始化空结果
	search_results = Page.objects.none()
	
	if query_string:
		# 记录搜索查询（用于搜索推广功能）
		query = Query.get(query_string)
		query.add_hit()
		
		try:
			# 根据搜索类型选择不同的查询
			if search_type == "blog":
				# 只搜索博客文章
				search_results = BlogPage.objects.live().search(query_string)
				logger.debug(f"博客搜索结果数: {search_results.count()}")
			elif search_type == "pages":
				# 只搜索普通页面（排除博客）
				search_results = Page.objects.live().exclude(
					id__in=BlogPage.objects.values_list('id', flat=True)
				).search(query_string)
				logger.debug(f"页面搜索结果数: {search_results.count()}")
			else:
				# 搜索所有内容
				search_results = Page.objects.live().search(query_string)
				logger.debug(f"全部搜索结果数: {search_results.count()}")
			
			
			# 确保返回的是QuerySet
			if not isinstance(search_results, QuerySet):
				logger.warning(f"搜索结果不是QuerySet，而是{type(search_results)}，转换为QuerySet")
				# 如果是列表，获取ID并查询
				if isinstance(search_results, list) and search_results:
					ids = [r.id for r in search_results if hasattr(r, 'id')]
					search_results = Page.objects.filter(id__in=ids)
				else:
					# 如果无法转换，返回空QuerySet
					search_results = Page.objects.none()
		
		except Exception as e:
			logger.error(f"搜索出错: {e}")
			logger.error(traceback.format_exc())
			# 发生错误时返回空结果
			search_results = Page.objects.none()
	
	return search_results


def get_search_suggestions(query_string, limit=5):
	"""
	获取搜索建议列表

	参数:
		query_string: 搜索关键词前缀
		limit: 最大返回数量

	返回:
		搜索建议列表
		
	"""
	if not query_string or len(query_string) < 2:
		return []
	
	# 获取包含查询字符串的搜索记录，按点击量排序
	try:
		# 使用 daily_hits 聚合得到总点击量
		suggestions = Query.objects.filter(
			query_string__icontains=query_string
		).annotate(
			total_hits=Count('daily_hits')
		).order_by('-total_hits')[:limit]
		
		# 构建建议列表
		results = [
			{
				'query': item.query_string,
				'hits': item.total_hits  # 使用聚合的 total_hits
			}
			for item in suggestions
		]
		
		return results
	except Exception as e:
		logger.error(f"获取搜索建议时出错: {e}")
		return []


def format_search_results_for_api(search_results):
	"""
	将搜索结果格式化为API响应格式

	参数:
		search_results: 搜索结果对象

	返回:
		API格式的结果列表
	"""
	results_data = []
	
	# 确保search_results是可迭代的
	if search_results is None:
		return results_data
	
	try:
		for result in search_results:
			data = {
				'id': result.id,
				'title': result.title,
				'url': result.url,
				'type': result._meta.model_name,
			}
			
			# 添加特定类型的额外字段
			if hasattr(result.specific, 'intro'):
				data['intro'] = result.specific.intro
			if hasattr(result.specific, 'date'):
				data['date'] = result.specific.date.isoformat() if result.specific.date else None
			
			results_data.append(data)
	except Exception as e:
		logger.error(f"格式化搜索结果出错: {e}")
	
	return results_data