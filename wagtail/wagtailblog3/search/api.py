# search/api.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .core import perform_search, get_search_suggestions, format_search_results_for_api
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def search_api(request):
	"""REST API搜索端点"""
	# 获取参数
	query = request.GET.get('q', '')
	search_type = request.GET.get('type', 'all')
	page = int(request.GET.get('page', 1))
	per_page = int(request.GET.get('per_page', 10))
	
	if not query:
		return Response({'error': '请提供搜索查询'}, status=400)
	
	try:
		# 执行搜索
		search_results = perform_search(query, search_type)
		
		# 计算总数
		total_count = search_results.count()
		
		# 计算分页
		start = (page - 1) * per_page
		end = start + per_page
		paginated_results = search_results[start:end]
		
		# 格式化结果
		results_data = format_search_results_for_api(paginated_results)
		
		# 构建响应
		data = {
			'query': query,
			'total': total_count,
			'page': page,
			'per_page': per_page,
			'results': results_data
		}
		
		return Response(data)
	except Exception as e:
		logger.error(f"API搜索出错: {e}")
		return Response({
			'error': f"搜索处理错误: {str(e)}",
			'query': query,
			'results': []
		}, status=500)


@api_view(['GET'])
def search_suggestions_api(request):
	"""搜索建议API"""
	query = request.GET.get('q', '')
	
	try:
		# 获取搜索建议
		suggestions = get_search_suggestions(query)
		
		# 返回结果
		return Response({'suggestions': suggestions})
	except Exception as e:
		logger.error(f"API搜索建议出错: {e}")
		return Response({
			'error': f"获取搜索建议错误: {str(e)}",
			'suggestions': []
		}, status=500)