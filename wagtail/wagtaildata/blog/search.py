# blog/search.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.search.backends import get_search_backend
from itertools import chain
import time, logging

from blog.models import BlogPage, BlogCategory
from blog.utils import get_mongo_db

# 设置日志
logger = logging.getLogger(__name__)


def hybrid_search(request):
	"""
	混合搜索功能，通过自定义搜索后端同时使用MySQL和MongoDB搜索
	"""
	start_time = time.time()
	search_query = request.GET.get('query', None)
	page = request.GET.get('page', 1)
	search_results = []
	
	# 记录查询信息
	logger.info(f"执行混合搜索: {search_query}")
	
	if search_query:
		# 使用自定义搜索后端执行搜索
		search_backend = get_search_backend()
		
		# 搜索开始时间
		backend_start = time.time()
		
		# 执行搜索 - HybridSearchBackend会自动处理MySQL和MongoDB的搜索
		search_results = search_backend.search(
			search_query,
			BlogPage.objects.live(),
			fields=['title', 'intro', 'body']
		)
		
		# 按相关性排序
		if hasattr(search_results, 'order_by_relevance'):
			search_results = search_results.order_by_relevance()
		
		# 计算搜索耗时
		backend_time = time.time() - backend_start
		logger.info(f"搜索后端耗时: {backend_time:.3f}秒，找到结果数: {len(search_results)}")
	
	# 分页
	paginator = Paginator(search_results, 10)
	try:
		search_results = paginator.page(page)
	except PageNotAnInteger:
		search_results = paginator.page(1)
	except EmptyPage:
		search_results = paginator.page(paginator.num_pages)
	
	total_time = time.time() - start_time
	logger.info(f"混合搜索总耗时: {total_time:.3f}秒，总结果数: {len(search_results)}")
	
	# 返回结果
	return {
		'search_query': search_query,
		'search_results': search_results,
	}


def blog_search(request):
	"""
	博客搜索功能，支持全文搜索
	"""
	search_query = request.GET.get('query', None)
	page = request.GET.get('page', 1)
	search_results = []
	
	# 检查是否有搜索关键词
	if search_query:
		# 记录搜索查询
		# Query.get(search_query).add_hit()
		
		# 获取搜索后端
		search_backend = get_search_backend()
		
		# 执行搜索，指定模型和字段
		search_results = search_backend.search(
			search_query,
			BlogPage.objects.live(),
			fields=['title', 'intro', 'body']
		)
		
		# 按相关性排序
		search_results = search_results.order_by('-_score')
	
	# 分页
	paginator = Paginator(search_results, 10)
	try:
		search_results = paginator.page(page)
	except PageNotAnInteger:
		search_results = paginator.page(1)
	except EmptyPage:
		search_results = paginator.page(paginator.num_pages)
	
	# 返回结果
	return {
		'search_query': search_query,
		'search_results': search_results,
	}


def advanced_search(request):
	"""高级搜索功能，支持按分类、标签和日期筛选"""
	
	search_query = request.GET.get('query', '')
	category_id = request.GET.get('category', '')
	tag = request.GET.get('tag', '')
	date_from = request.GET.get('date_from', '')
	date_to = request.GET.get('date_to', '')
	page = request.GET.get('page', 1)
	
	# 获取搜索后端
	search_backend = get_search_backend()
	
	# 基础查询 - 所有发布的博客页面
	query_set = BlogPage.objects.live()
	
	# 应用全文搜索
	if search_query:
		search_results = search_backend.search(  # 使用搜索后端进行全文搜索
			search_query,
			query_set,
			fields=['title', 'intro', 'body']
		)
		query_set = search_results
	
	# 应用过滤条件
	if category_id:
		try:
			category = BlogCategory.objects.get(id=category_id)  # 获取分类对象
			query_set = query_set.filter(categories=category)  # 过滤分类
		except (BlogCategory.DoesNotExist, ValueError):
			# 处理无效分类ID
			pass
	
	if tag:  # 过滤标签
		query_set = query_set.filter(tags__name=tag)
	
	if date_from:  # 过滤开始日期
		query_set = query_set.filter(date__gte=date_from)
	
	if date_to:  # 过滤结束日期
		query_set = query_set.filter(date__lte=date_to)
	
	# 确保结果唯一
	query_set = query_set.distinct()
	
	# 按发布日期排序(如果没有搜索词)或按相关性排序(如果有搜索词)
	if search_query and hasattr(query_set, 'order_by_relevance'):
		# Elasticsearch结果已经按相关性排序
		pass
	else:
		query_set = query_set.order_by('-date')
	
	# 分页
	paginator = Paginator(query_set, 10)
	try:
		search_results = paginator.page(page)
	except PageNotAnInteger:
		search_results = paginator.page(1)
	except EmptyPage:
		search_results = paginator.page(paginator.num_pages)
	
	# 获取所有分类用于过滤
	categories = BlogCategory.objects.all()
	
	# 返回结果
	return {
		'search_query': search_query,
		'search_results': search_results,
		'categories': categories,
		'current_category': category_id,
		'current_tag': tag,
		'date_from': date_from,
		'date_to': date_to,
	}