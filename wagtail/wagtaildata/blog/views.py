# blog/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import logging

from wagtail.models import Page
from wagtail.contrib.search_promotions.models import SearchPromotion

from blog.models import BlogPage, BlogCategory
from blog.search import blog_search, advanced_search, hybrid_search

# 设置日志
logger = logging.getLogger(__name__)


def search(request):
	"""基本搜索视图"""
	
	# 获取搜索查询
	search_data = hybrid_search(request)  # 使用混合搜索
	
	# 获取推广内容
	search_picks = []
	if search_data['search_query']:
		search_picks = SearchPromotion.objects.filter(
			query__query_string__iexact=search_data['search_query']
		)
	
	# 渲染模板
	return render(request, 'search/search.html', {
		'search_query': search_data['search_query'],
		'search_results': search_data['search_results'],
		'search_picks': search_picks,
	})


def advanced_search_view(request):
	"""高级搜索视图"""
	
	# 获取搜索查询
	search_data = advanced_search(request)
	
	# 渲染模板
	return render(request, 'search/advanced_search.html', search_data)


@require_GET
def api_search(request):
	"""搜索API，返回JSON结果，用于异步搜索功能"""
	search_query = request.GET.get('query', '')
	
	if not search_query:  # 如果没有搜索关键词，返回空结果
		return JsonResponse({
			'count': 0,
			'results': [],
		})
	
	# 使用混合搜索
	from wagtail.search.backends import get_search_backend
	search_backend = get_search_backend()
	
	# 执行搜索
	search_results = search_backend.search(
		search_query,
		BlogPage.objects.live(),
		fields=['title', 'intro', 'body']
	)
	
	# 格式化结果
	results = []
	for page in search_results[:10]:  # 限制最多10个结果
		results.append({
			'id': page.id,
			'title': page.title,
			'url': page.url,
			'intro': page.specific.intro if hasattr(page.specific, 'intro') else '',
			'date': page.specific.date.isoformat() if hasattr(page.specific, 'date') else '',
		})
	
	return JsonResponse({
		'count': len(results),
		'results': results,
	})


class BlogCategoryView(TemplateView):
	"""显示特定分类的博客文章"""
	
	template_name = 'blog/blog_category.html'
	
	def get_context_data(self, **kwargs):
		# 该视图用于显示特定分类的博客文章
		context = super().get_context_data(**kwargs)
		# 获取分类slug
		category_slug = self.kwargs.get('category_slug')
		
		try:
			category = BlogCategory.objects.get(slug=category_slug)
			context['category'] = category
			
			blog_pages = BlogPage.objects.live().filter(categories=category).order_by('-date')
			
			# 分页
			paginator = Paginator(blog_pages, 12)
			page = self.request.GET.get('page')
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			
			context['posts'] = posts
		
		except BlogCategory.DoesNotExist:
			context['category'] = None
			context['posts'] = []
		
		return context


class BlogTagView(TemplateView):
	"""显示特定标签的博客文章"""
	
	# 该视图用于显示特定标签的博客文章
	template_name = 'blog/blog_tag.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tag = self.kwargs.get('tag')
		
		if tag:
			context['tag'] = tag
			blog_pages = BlogPage.objects.live().filter(tags__name=tag).order_by('-date')
			
			# 分页
			paginator = Paginator(blog_pages, 12)
			page = self.request.GET.get('page')
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			
			context['posts'] = posts
		else:
			context['tag'] = None
			context['posts'] = []
		
		return context


@method_decorator(csrf_exempt, name='dispatch')
class BlogArchiveView(TemplateView):
	"""显示博客归档页面"""
	
	# 该视图用于显示博客的归档页面
	template_name = 'blog/blog_archive.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# 按年份月份归档
		blog_dates = BlogPage.objects.live().dates('date', 'month', order='DESC')
		
		archive_data = {}
		for date in blog_dates:
			year = date.year
			month = date.month
			
			if year not in archive_data:
				archive_data[year] = {}
			
			# 获取该月的文章数量
			count = BlogPage.objects.live().filter(date__year=year, date__month=month).count()
			archive_data[year][month] = {
				'count': count,
				'date': date,
			}
		
		context['archive_data'] = archive_data
		
		# 如果指定了年份和月份，则显示相应的文章
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		
		if year and month:
			blog_pages = BlogPage.objects.live().filter(
				date__year=year,
				date__month=month
			).order_by('-date')
			
			# 分页
			paginator = Paginator(blog_pages, 12)
			page = self.request.GET.get('page')
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			
			context['posts'] = posts
			context['year'] = year
			context['month'] = month
		
		return context