# 在blog/middleware.py文件中
import os


class DisableProxyMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		# 临时禁用所有代理设置
		old_proxies = {}
		for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
			old_proxies[var] = os.environ.pop(var, None)
		
		# 确保NO_PROXY设置为全部
		os.environ['NO_PROXY'] = '*'
		
		# 处理请求
		response = self.get_response(request)
		
		# 如果需要，恢复原始代理设置
		# 根据你的需求，这一步可能不需要
		# for var, value in old_proxies.items():
		#     if value:
		#         os.environ[var] = value
		
		return response