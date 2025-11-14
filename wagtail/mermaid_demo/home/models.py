from django.db import models
from wagtail.models import Page


class HomePage(Page):
	pass
	
	# --- 1. (重要) 允许在 Home 页面下创建 BlogPage ---
	# 将 'blog.BlogPage' 添加到 subpage_types
	subpage_types = ['blog.BlogPage']

# (您也可以在这里添加其他页面类型，例如 'home.HomePage')