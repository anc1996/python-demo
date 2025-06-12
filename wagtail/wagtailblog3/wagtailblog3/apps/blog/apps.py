# blog/apps.py
from django.apps import AppConfig
from blog.markdown_helpers import MarkdownHelper

class BlogConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'blog'
	
	def ready(self):
		"""当应用准备好时执行初始化"""
		# 导入信号处理器
		import blog.signals
		if MarkdownHelper.is_markdown_installed():
			MarkdownHelper.register_wagtail_markdown_hooks()