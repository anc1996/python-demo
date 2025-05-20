# archive/wagtail_hooks.py
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse, path
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.dateparse import parse_date  # 用于解析日期字符串
from blog.models import BlogPage
from .views import get_archive_data  # 假设这个函数仍然用于左侧的年/月统计


@hooks.register('register_admin_menu_item')
def register_archive_menu_item():
	return MenuItem(
		'博客归档',
		reverse('archive_admin_dashboard'),
		icon_name='folder-open-inverse',
		order=950
	)


@hooks.register('register_admin_urls')
def register_archive_admin_urls():
	def archive_dashboard(request):
		archive_data_for_sidebar = get_archive_data()  # 用于归档统计表格
		total_posts_count = BlogPage.objects.live().count()
		
		start_date_str = request.GET.get('start_date')
		end_date_str = request.GET.get('end_date')
		page_number = request.GET.get('page')
		
		date_filtered_posts_page = None  # 重命名为 paged_items 或类似
		is_date_filter_active = False
		
		posts_prefetch = ['authors', 'categories', 'tags'] # 预取相关对象以优化查询
		
		if start_date_str and end_date_str:
			
			selected_start_date_obj = parse_date(start_date_str)  # 解析开始日期
			selected_end_date_obj = parse_date(end_date_str) # 解析结束日期
			
			if selected_start_date_obj and selected_end_date_obj and selected_start_date_obj <= selected_end_date_obj:
				is_date_filter_active = True # 日期过滤器处于活动状态
				date_filtered_posts_qs = BlogPage.objects.live().filter(
					date__range=(selected_start_date_obj, selected_end_date_obj)
				).order_by('-date').prefetch_related(*posts_prefetch)
				
				paginator = Paginator(date_filtered_posts_qs, 20)
				try:
					date_filtered_posts_page = paginator.page(page_number)
				except PageNotAnInteger:
					date_filtered_posts_page = paginator.page(1) # 如果页码不是整数，返回第一页
				except EmptyPage:
					date_filtered_posts_page = paginator.page(paginator.num_pages)
		
		if not is_date_filter_active:
			context_posts = BlogPage.objects.live().order_by('-date').prefetch_related(*posts_prefetch)[:10]
			is_paginated_list = False  # 最近10篇不分页
		else:
			context_posts = date_filtered_posts_page  # 这是一个 Page 对象
			is_paginated_list = True if date_filtered_posts_page else False  # 确保 date_filtered_posts_page 存在
		
		context = {
			'archive_data_for_sidebar': archive_data_for_sidebar,# 侧边栏归档数据
			'total_posts_count': total_posts_count, # 总文章数
			'posts_to_display': context_posts, # 传递给模板的文章列表
			'is_date_filter_active': is_date_filter_active, # 是否启用日期过滤器
			'is_paginated_list': is_paginated_list, # 是否分页
			'selected_start_date': start_date_str,  # 用于表单回填
			'selected_end_date': end_date_str,  # 用于表单回填
			'range_1_to_12': range(1, 13),  # <--- 新增：传递月份范围给模板
		}
		return render(request, 'archive/admin/dashboard.html', context)
	
	return [
		path('archive/dashboard/', archive_dashboard, name='archive_admin_dashboard'),
	]