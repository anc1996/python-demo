# archive/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncYear, TruncMonth
from blog.models import BlogPage
import datetime
import logging

logger = logging.getLogger(__name__)


def get_archive_data():
	"""获取归档数据的工具函数"""
	
	# 获取所有已发布的博客页面
	blog_pages = BlogPage.objects.live()
	
	# 按年份分组统计
	yearly_archives = blog_pages.annotate( # annotate函数用于在查询集中添加额外的字段
		year=TruncYear('date') # TruncYear函数用于将日期截断到年份
	).values('year').annotate(
		count=Count('id')
	).order_by('-year') # 按年份降序排列
	
	# 按月份分组统计
	monthly_archives = blog_pages.annotate(
		year=TruncYear('date'),
		month=TruncMonth('date')
	).values('year', 'month').annotate(
		count=Count('id')
	).order_by('-year', '-month') # 按年份和月份降序排列
	
	# 组织成树形结构
	archive_tree = {}
	
	for item in yearly_archives:
		year = item['year'].year
		archive_tree[year] = {
			'count': item['count'],
			'months': {}
		}
	
	for item in monthly_archives:
		year = item['year'].year
		month = item['month'].month
		month_name = item['month'].strftime('%B')
		
		if year in archive_tree:
			archive_tree[year]['months'][month] = {
				'count': item['count'],
				'name': month_name,
				'display_name': f"{month}月"  # 中文显示
			}
	
	return archive_tree


def archives_api(request):
	"""归档数据的JSON API"""
	archive_data = get_archive_data()
	
	# 转换为可序列化的格式
	data = []
	for year, year_data in archive_data.items():
		year_obj = {
			'year': year,
			'count': year_data['count'],
			'months': []
		}
		
		for month, month_data in year_data['months'].items():
			year_obj['months'].append({
				'month': month,
				'name': month_data['name'],
				'display_name': month_data['display_name'],
				'count': month_data['count']
			})
		
		data.append(year_obj)
	
	return JsonResponse({'archives': data})


def year_archive(request, year):
	"""年份归档视图"""
	# 获取指定年份的博客文章
	pages = BlogPage.objects.live().filter(date__year=year).order_by('-date')
	
	# 获取归档数据用于侧边栏
	archive_data = get_archive_data()
	
	return render(request, 'archive/year_archive.html', {
		'year': year,
		'pages': pages,
		'archive_data': archive_data
	})


def month_archive(request, year, month):
	"""月份归档视图"""
	# 计算日期范围
	start_date = datetime.date(year, month, 1)
	# 计算下个月的第一天
	if month == 12:
		end_date = datetime.date(year + 1, 1, 1)
	else:
		end_date = datetime.date(year, month + 1, 1)
	
	# 获取特定年月的博客文章
	pages = BlogPage.objects.live().filter(
		date__gte=start_date,
		date__lt=end_date
	).order_by('-date')
	
	# 获取归档数据用于侧边栏
	archive_data = get_archive_data()
	
	# 获取月份名称
	month_name = datetime.date(year, month, 1).strftime('%B')
	
	return render(request, 'archive/month_archive.html', {
		'year': year,
		'month': month,
		'month_name': month_name,
		'pages': pages,
		'archive_data': archive_data
	})