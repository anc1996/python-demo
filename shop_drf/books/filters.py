#!/user/bin/env python3
# -*- coding: utf-8 -*-

import django_filters

from books.models import BookInfo, PeopleInfo


class BookInfoFilter(django_filters.FilterSet):
	"""
	过滤类
	"""
	# name,模糊查询
	name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
	# 发布日期范围
	min_pub_date = django_filters.DateFilter(field_name='pub_date', lookup_expr='gte') # 大于等于
	max_pub_date = django_filters.DateFilter(field_name='pub_date', lookup_expr='lte') # 小于等于
	# 阅读量范围
	min_readcount = django_filters.NumberFilter(field_name='readcount', lookup_expr='gte')
	max_readcount = django_filters.NumberFilter(field_name='readcount', lookup_expr='lte')
	# 评论量范围
	min_commentcount = django_filters.NumberFilter(field_name='commentcount', lookup_expr='gte')
	max_commentcount = django_filters.NumberFilter(field_name='commentcount', lookup_expr='lte')
	
	class Meta:
		model = BookInfo
		fields = ['name', 'min_pub_date', 'max_pub_date', 'min_readcount',
		          'max_readcount', 'min_commentcount', 'max_commentcount'
		          ]
		

class PeopleInfoFilter(django_filters.FilterSet):
	"""
	过滤类
	"""
	# name,模糊查询
	name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
	# description,模糊查询
	description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
	
	class Meta:
		model = PeopleInfo
		fields = ['name', 'description']
		
