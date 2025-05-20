# search/views.py
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
import logging

from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from wagtail.search.utils import separate_filters_from_query

# 启用搜索查询日志记录
from wagtail.contrib.search_promotions.models import Query

# 设置日志
logger = logging.getLogger(__name__)


def search(request):
	search_query = request.GET.get("query", None)
	page = request.GET.get("page", 1)
	search_type = request.GET.get("type", None)  # 新增：可选搜索类型参数
	
	# 搜索
	if search_query:
		# 日志记录查询以用于"推广搜索结果"功能
		query = Query.get(search_query)
		query.add_hit()
		
		# 分离过滤器和查询
		query_string, filters = separate_filters_from_query(search_query)
		
		# 获取搜索后端
		search_backend = get_search_backend()
		
		# 判断是否为混合搜索后端
		is_hybrid_backend = hasattr(search_backend, 'database_backend')
		is_elasticsearch = hasattr(search_backend, 'es')
		
		logger.info(f"搜索后端类型: {'混合' if is_hybrid_backend else '标准'} (ES: {is_elasticsearch})")
		
		# 构建基础查询集
		queryset = Page.objects.live()
		
		# 根据搜索类型过滤
		from blog.models import BlogPage
		if search_type == 'blog':
			queryset = BlogPage.objects.live()
			logger.info("仅搜索博客页面")
		
		# 根据后端类型使用不同的搜索策略
		if is_elasticsearch:  # Elasticsearch后端
			search_results = queryset.search(
				query_string,
				operator="or",  # 使用OR操作符增加结果范围
				boost_fields={  # 提高标题匹配的权重
					'title': 10,
					'search_description': 5,
				},
				partial_match=True  # 启用部分匹配
			)
		else:  # 数据库或混合后端
			# 直接使用搜索后端而不是模型的search方法，确保混合后端正确工作
			search_results = search_backend.search(
				query_string,
				queryset,
				fields=['title', 'search_description', 'body'],
				operator="or",
				order_by_relevance=True
			)
		
		# 应用过滤器
		for field, value in filters.items():
			try:
				search_results = search_results.filter(**{field: value})
			except Exception as e:
				logger.warning(f"应用过滤器 {field}={value} 失败: {e}")
	else:
		search_results = Page.objects.none()
	
	# 获取推广内容
	search_picks = []
	if search_query:
		search_picks = Query.get(search_query).editors_picks.all()
	
	# 分页
	paginator = Paginator(search_results, 10)
	try:
		search_results = paginator.page(page)
	except PageNotAnInteger:
		search_results = paginator.page(1)
	except EmptyPage:
		search_results = paginator.page(paginator.num_pages)
	
	return TemplateResponse(
		request,
		"search/search.html",
		{
			"search_query": search_query,
			"search_results": search_results,
			"search_picks": search_picks,
			"search_type": search_type,  # 传递搜索类型到模板
		},
	)


def hybrid_search(request):
	"""
    专门使用混合搜索后端的视图函数
    优化博客内容搜索体验
    """
	search_query = request.GET.get("query", None)
	page = request.GET.get("page", 1)
	
	# 搜索
	if search_query:
		# 日志记录查询
		query = Query.get(search_query)
		query.add_hit()
		
		# 获取搜索后端 - 应该是混合后端
		search_backend = get_search_backend()
		
		# 检查是否具有混合搜索能力
		if hasattr(search_backend, 'database_backend'):
			logger.info(f"使用混合搜索后端搜索: {search_query}")
			
			# 从blog.models导入BlogPage
			from blog.models import BlogPage
			
			# 使用混合后端搜索BlogPage
			search_results = search_backend.search(
				search_query,
				BlogPage.objects.live(),
				fields=['title', 'intro', 'body'],
				operator="or",
				order_by_relevance=True
			)
		else:
			# 兜底使用普通搜索
			logger.warning("未找到混合搜索后端，回退到标准搜索")
			from blog.models import BlogPage
			search_results = BlogPage.objects.live().search(search_query)
	else:
		from blog.models import BlogPage
		search_results = BlogPage.objects.none()
	
	# 获取推广内容
	search_picks = []
	if search_query:
		search_picks = Query.get(search_query).editors_picks.all()
	
	# 分页
	paginator = Paginator(search_results, 10)
	try:
		search_results = paginator.page(page)
	except PageNotAnInteger:
		search_results = paginator.page(1)
	except EmptyPage:
		search_results = paginator.page(paginator.num_pages)
	
	return TemplateResponse(
		request,
		"search/hybrid_search.html",  # 可以使用不同的模板
		{
			"search_query": search_query,
			"search_results": search_results,
			"search_picks": search_picks,
			"is_hybrid_search": True,
		},
	)