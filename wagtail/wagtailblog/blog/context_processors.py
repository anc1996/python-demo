#!/user/bin/env python3
# -*- coding: utf-8 -*-
# 创建新文件: blog/context_processors.py
def blog_content(request):
	"""使所有MongoDB博客内容可用于模板"""
	# 仅处理BlogPage
	if not hasattr(request, 'page') or not hasattr(request.page, 'specific') or not hasattr(request.page.specific,
	                                                                                        'get_content_from_mongodb'):
		return {}
	
	# 获取页面
	page = request.page.specific
	
	# 获取MongoDB内容
	mongo_content = page.get_content_from_mongodb()
	
	return {
		'mongo_content': mongo_content
	}