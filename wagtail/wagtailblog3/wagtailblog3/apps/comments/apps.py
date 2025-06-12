# comments/apps.py
from django.apps import AppConfig


class CommentsConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'comments'
	verbose_name = "评论系统"
	
	def ready(self):
		"""应用就绪时执行初始化"""
		# 注册信号
		import comments.signals