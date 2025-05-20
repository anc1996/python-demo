"""
博客 API 视图集
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from wagtail.models import Page
from blog.models import BlogPage, BlogIndexPage
from ..serializers import (
	BlogIndexPageSerializer,
	BlogPageListSerializer,
	BlogPageDetailSerializer
)


class BlogIndexPageViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	博客索引页 API 视图集
	"""
	queryset = BlogIndexPage.objects.live().public()
	serializer_class = BlogIndexPageSerializer


class BlogPageViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	博客文章 API 视图集
	"""
	queryset = BlogPage.objects.live().public().order_by('-date')
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['title', 'intro', 'author']
	ordering_fields = ['date', 'title']
	ordering = ['-date']  # 默认按发布日期降序
	
	def get_serializer_class(self):
		"""
		根据操作选择不同的序列化器
		"""
		if self.action == 'list':
			return BlogPageListSerializer
		return BlogPageDetailSerializer
	
	def get_queryset(self):
		"""
		自定义查询集
		"""
		queryset = super().get_queryset()
		
		# 按作者筛选
		author = self.request.query_params.get('author', None)
		if author:
			queryset = queryset.filter(author__icontains=author)
		
		# 按年份筛选
		year = self.request.query_params.get('year', None)
		if year:
			queryset = queryset.filter(date__year=year)
		
		# 按月份筛选
		month = self.request.query_params.get('month', None)
		if month and year:
			queryset = queryset.filter(date__month=month)
		
		return queryset
	
	@action(detail=False, methods=['get'])
	def years(self, request):
		# 注意这里添加了 request 参数
		years = BlogPage.objects.live().public().dates('date', 'year')
		year_list = [date.year for date in years]
		return Response(year_list)
	
	@action(detail=False, methods=['get'])
	def authors(self, request):
		# 注意这里添加了 request 参数
		authors = BlogPage.objects.live().public().values_list('author', flat=True).distinct()
		return Response(list(authors))
	
	@action(detail=False, methods=['get'])
	def search(self, request):
		"""
		搜索博客文章
		"""
		query = request.query_params.get('q', '')
		if not query:
			return Response({'error': '请提供搜索关键词'}, status=status.HTTP_400_BAD_REQUEST)
		
		# 使用 Wagtail 搜索功能
		search_results = BlogPage.objects.live().public().search(query)
		page = self.paginate_queryset(search_results)
		
		if page is not None:
			serializer = BlogPageListSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		
		serializer = BlogPageListSerializer(search_results, many=True)
		return Response(serializer.data)