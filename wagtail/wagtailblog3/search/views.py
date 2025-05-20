# search/views.py
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.http import JsonResponse
from .analytics import SearchAnalytics
from .core import perform_search, get_search_suggestions, format_search_results_for_api
import logging

logger = logging.getLogger(__name__)


def search(request):
    """搜索视图"""
    # 获取参数
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    search_type = request.GET.get("type", "all")  # all, blog, pages

    # 执行搜索
    search_results = perform_search(search_query, search_type)

    # 分页处理
    paginator = Paginator(search_results, 10) # 假设每页10条
    try:
        paginated_results = paginator.page(page)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)

    # 如果是AJAX请求（例如，用于无限滚动或动态加载），则返回JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # 注意：这里的 search_ajax 逻辑需要根据你的具体 AJAX 实现来调整
        # 简单示例是直接返回当前页的 JSON 数据
        return search_ajax(request, paginated_results, search_query, search_type)

    # 非 AJAX 请求，准备完整页面渲染
    # 获取热门搜索词 (例如最近30天的前10个)
    try:
        popular_search_terms_list = SearchAnalytics.get_popular_searches(days=30, limit=10)
    except Exception as e:
        logger.error(f"获取热门搜索词失败: {e}")
        popular_search_terms_list = []

    # 记录搜索分析 (只有在实际执行搜索时)
    if search_query:
        try:
            SearchAnalytics.log_search(
                search_query,
                results_count=paginator.count, # 使用 paginator.count 获取总结果数
                search_type=search_type
            )
        except Exception as e:
            logger.error(f"记录搜索分析错误: {e}")

    context = {
        "search_query": search_query,
        "search_results": paginated_results,
        "search_type": search_type,
        "popular_search_terms": popular_search_terms_list, # 热门搜索词
    }
    return TemplateResponse(
        request,
        "search/search.html",
        context,
    )

def search_ajax(request, search_results, search_query, search_type=None):
    """AJAX搜索响应"""
    try:
        results_data = format_search_results_for_api(search_results.object_list) # 确保传递列表

        response_data = {
            'query': search_query,
            'results': results_data,
            'has_next': search_results.has_next(),
            'has_previous': search_results.has_previous(),
            'total_count': search_results.paginator.count,
            'current_page': search_results.number,
            'total_pages': search_results.paginator.num_pages,
            'search_type': search_type,  # 添加搜索类型
        }
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"AJAX搜索响应错误: {e}")
        return JsonResponse({
            'error': f"搜索处理错误: {str(e)}",
            'query': search_query,
            'results': []
        }, status=500)


def search_suggestions(request):
	"""搜索建议API"""
	query = request.GET.get('q', '')
	
	# 获取搜索建议
	try:
		suggestions = get_search_suggestions(query)
		
		# 返回结果
		return JsonResponse({'suggestions': suggestions})
	except Exception as e:
		logger.error(f"获取搜索建议错误: {e}")
		return JsonResponse({
			'error': f"获取搜索建议错误: {str(e)}",
			'suggestions': []
		}, status=500)