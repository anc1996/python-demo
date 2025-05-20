# blog/wagtail_hooks.py
from django.templatetags.static import static
from wagtail import hooks
from django.utils.html import format_html
import logging

from .markdown_helpers import MarkdownHelper
from .models import PageViewCount
from django.db.models import Sum, Q
from wagtail.models import Page
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.contrib import messages
from wagtail.admin.views.reports import ReportView
from wagtail.admin.menu import MenuItem
from wagtail.admin.ui.tables import Column, DateColumn, Table
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from wagtail.admin.auth import require_admin_access
from .forms import PageViewCountForm

# 设置日志记录器
logger = logging.getLogger(__name__)


@hooks.register('before_edit_page')
def before_edit_page(request, page):
	"""在编辑页面前从MongoDB加载内容"""
	if hasattr(page, 'get_content_from_mongodb') and hasattr(page, 'body'):
		try:
			# 获取MongoDB内容
			content = page.get_content_from_mongodb()
			
			if content and 'body' in content and isinstance(content['body'], list):
				# 从MongoDB创建StreamValue
				from wagtail.blocks.stream_block import StreamValue
				from wagtailblog3.mongodb import MongoDBStreamFieldAdapter
				
				# 获取StreamBlock定义
				stream_block = page.body.stream_block
				
				# 预处理内容 - 特别是处理Markdown块
				for block in content['body']:
					if isinstance(block, dict) and block.get('type') == 'markdown_block' and 'value' in block:
						block['value'] = MarkdownHelper.process_markdown_for_editor(block['value'])
				
				# 使用适配器创建StreamValue
				try:
					page.body = MongoDBStreamFieldAdapter.from_mongodb(content['body'], stream_block)
				except Exception as e:
					logger.error(f"从MongoDB创建StreamValue失败: {e}")
					# 尝试使用更简单的方法
					page.body = StreamValue(stream_block, content['body'], is_lazy=True)
			else:
				if not content:
					logger.warning(f"未找到页面ID={page.id}的MongoDB内容")
				elif 'body' not in content:
					logger.warning(f"MongoDB内容中缺少body字段: {list(content.keys())}")
				elif not isinstance(content['body'], list):
					logger.warning(f"MongoDB中的body不是列表格式: {type(content['body'])}")
		except Exception as e:
			import traceback
			logger.error(f"在编辑页面前加载MongoDB内容时出错: {e}")
			logger.error(traceback.format_exc())


@hooks.register('insert_editor_js')
def editor_js():
	"""添加JavaScript支持到编辑器"""
	return format_html(
		'<script src="{}"></script>',
		static('js/editor-enhancements.js')
	)


@hooks.register('after_edit_page')
def after_edit_page(request, page):
	"""编辑页面后清空body字段，避免存入MySQL"""
	if hasattr(page, 'mongo_content_id') and hasattr(page, 'body'):
		try:
			# 确保body内容已保存到MongoDB (save方法会处理)
			if page.id:
				type(page).objects.filter(id=page.id).update(body=[])
		except Exception as e:
			import traceback
			logger.error(f"清空页面body字段时出错: {e}")
			logger.error(traceback.format_exc())


# 页面统计报告
@hooks.register('register_admin_urls')
def register_page_views_report_url():
	
	@method_decorator(require_admin_access, name='dispatch')
	class PageViewsReportView(ReportView):
		template_name = 'wagtailadmin/reports/page_views_report.html'
		title = "页面访问统计"
		header_icon = "site"
		
		def get_queryset(self):
			# 基础查询
			queryset = Page.objects.filter(
				id__in=PageViewCount.objects.values('page').distinct()
			).annotate(
				total_views=Sum('view_counts__count'),
				total_unique_views=Sum('view_counts__unique_count')
			)
			
			# 应用搜索筛选
			search_query = self.request.GET.get('q', '')
			if search_query:
				# 标题搜索
				queryset = queryset.filter(title__icontains=search_query)
			
			# 数值范围筛选
			min_views = self.request.GET.get('min_views', '')
			max_views = self.request.GET.get('max_views', '')
			
			if min_views and min_views.isdigit():
				queryset = queryset.filter(total_views__gte=int(min_views))
			
			if max_views and max_views.isdigit():
				queryset = queryset.filter(total_views__lte=int(max_views))
			
			# 日期范围筛选
			start_date = self.request.GET.get('start_date', '')
			end_date = self.request.GET.get('end_date', '')
			
			if start_date:
				queryset = queryset.filter(first_published_at__gte=start_date)
			
			if end_date:
				queryset = queryset.filter(first_published_at__lte=end_date)
			
			# 排序
			sort_by = self.request.GET.get('sort', '-total_views')
			valid_sort_fields = ['total_views', '-total_views', 'total_unique_views',
			                     '-total_unique_views', 'first_published_at', '-first_published_at', 'title', '-title']
			
			if sort_by in valid_sort_fields:
				queryset = queryset.order_by(sort_by)
			else:
				queryset = queryset.order_by('-total_views')
			
			return queryset
		
		def get_table(self, parent_context=None):
			# 创建空表格以满足Wagtail需求
			headers = [
				Column('title', label="页面标题"),
				Column('total_views', label="总访问量"),
				Column('total_unique_views', label="唯一访问量"),
			]
			return Table(headers, [], caption=self.title)
		
		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			
			# 添加分页
			paginator = context['paginator']
			page_obj = context['page_obj']
			
			# 添加搜索信息
			context['search_query'] = self.request.GET.get('q', '')
			context['min_views'] = self.request.GET.get('min_views', '')
			context['max_views'] = self.request.GET.get('max_views', '')
			context['start_date'] = self.request.GET.get('start_date', '')
			context['end_date'] = self.request.GET.get('end_date', '')
			context['sort'] = self.request.GET.get('sort', '-total_views')
			
			# 分页URL参数保留
			query_params = self.request.GET.copy()
			if 'page' in query_params:
				del query_params['page']
			context['query_string'] = query_params.urlencode()
			
			return context
	
	@method_decorator(require_admin_access, name='dispatch')
	class PageViewCountEditView(UpdateView):
		model = PageViewCount
		form_class = PageViewCountForm
		template_name = 'wagtailadmin/reports/edit_page_view_count.html'
		pk_url_kwarg = 'count_id'
		
		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			context['page_title'] = f"编辑 {self.object.page.title} 的访问数据"
			return context
		
		def form_valid(self, form):
			response = super().form_valid(form)
			messages.success(self.request, f"已成功更新 {self.object.page.title} 的访问统计")
			return response
		
		def get_success_url(self):
			return reverse('page_views_report')
	
	@require_admin_access
	def page_view_counts_for_page(request, page_id):
		"""查看某个页面的所有访问统计记录"""
		page = get_object_or_404(Page, id=page_id)
		counts = PageViewCount.objects.filter(page=page).order_by('-date')
		
		return render(request, 'wagtailadmin/reports/page_view_counts_detail.html', {
			'page': page,
			'counts': counts,
			'total_views': counts.aggregate(Sum('count'))['count__sum'] or 0,
			'total_unique_views': counts.aggregate(Sum('unique_count'))['unique_count__sum'] or 0,
		})
	
	return [
		path('reports/page-views/', PageViewsReportView.as_view(), name='page_views_report'),
		path('reports/page-views/edit/<int:count_id>/', PageViewCountEditView.as_view(), name='edit_page_view_count'),
		path('reports/page-views/page/<int:page_id>/', page_view_counts_for_page, name='page_view_counts_detail'),
	]


@hooks.register('register_reports_menu_item')
def register_page_views_report_menu_item():
	return MenuItem(
		label="页面访问统计",
		url='/admin/reports/page-views/',
		icon_name="site",
		order=700
	)