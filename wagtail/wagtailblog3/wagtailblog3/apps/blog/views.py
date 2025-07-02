# blog/views.py 中修改视图
from django.http import JsonResponse
from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import models
from django.views.generic import ListView, DetailView

from blog.models import Author, BlogPage


def get_client_ip(request):
	"""获取客户端IP地址"""
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


@require_POST
def toggle_reaction(request, page_id):
	"""添加或移除用户对页面的反应"""
	# 检查页面是否存在
	page = get_object_or_404(Page, id=page_id)
	
	# 获取反应类型
	reaction_type_id = request.POST.get('reaction_type')
	if not reaction_type_id:
		return JsonResponse({'error': '缺少反应类型'}, status=400)
	
	from .models import ReactionType
	reaction_type = get_object_or_404(ReactionType, id=reaction_type_id)
	
	# 获取用户或会话
	user = request.user if request.user.is_authenticated else None
	
	# 对于匿名用户，使用会话ID
	if not user and not request.session.session_key:
		request.session.save()
	session_key = request.session.session_key if not user else None
	
	# 获取IP地址
	ip = get_client_ip(request)
	
	# 检查用户是否已经有反应
	from .models import Reaction
	if user:
		existing = Reaction.objects.filter(page=page, user=user).first()
	else:
		existing = Reaction.objects.filter(
			page=page,
			session_key=session_key,
			ip_address=ip
		).first()
	
	# 如果已有同样的反应，则删除
	if existing and existing.reaction_type_id == int(reaction_type_id):
		existing.delete()
		action = 'removed'
	else:
		# 如果有不同的反应，更新它
		if existing:
			existing.reaction_type = reaction_type
			existing.save()
			action = 'changed'
		else:
			# 创建新反应
			Reaction.objects.create(
				page=page,
				reaction_type=reaction_type,
				user=user,
				session_key=session_key,
				ip_address=ip
			)
			action = 'added'
	
	# 获取更新后的反应计数
	reaction_counts = Reaction.objects.filter(page=page).values(
		'reaction_type'
	).annotate(
		count=models.Count('id')
	)
	
	counts = {r['reaction_type']: r['count'] for r in reaction_counts}
	
	return JsonResponse({
		'success': True,
		'action': action,
		'counts': counts
	})


def get_reaction_counts(request, page_id):
	"""获取页面的反应计数"""
	page = get_object_or_404(Page, id=page_id)
	
	# 获取所有反应类型
	from .models import ReactionType
	reaction_types = ReactionType.objects.all().order_by('display_order')
	
	# 获取该页面的反应计数
	from .models import Reaction
	reaction_counts = Reaction.objects.filter(page=page).values(
		'reaction_type'
	).annotate(
		count=models.Count('id')
	)
	
	# 转换为字典格式
	counts = {r['reaction_type']: r['count'] for r in reaction_counts}
	
	# 构建完整响应
	result = []
	for rt in reaction_types:
		result.append({
			'id': rt.id,
			'name': rt.name,
			'icon': rt.icon,
			'count': counts.get(rt.id, 0)
		})
	
	# 检查当前用户是否有反应
	user_reaction = None
	if request.user.is_authenticated:
		reaction = Reaction.objects.filter(
			page=page,
			user=request.user
		).first()
	else:
		if not request.session.session_key:
			request.session.save()
		reaction = Reaction.objects.filter(
			page=page,
			session_key=request.session.session_key
		).first()
	
	if reaction:
		user_reaction = reaction.reaction_type_id
	
	return JsonResponse({
		'reactions': result,
		'user_reaction': user_reaction
	})

def test_search_backend(request):
	"""测试 CustomSearchBackend 搜索功能"""
	query = request.GET.get('q', '')
	if not query:
		return JsonResponse({'error': '请提供搜索关键词'})
	
	# 获取搜索后端
	search_backend = get_search_backend()
	
	# 执行搜索 - 移除可能不兼容的参数
	search_results = search_backend.search(
		query,
		Page.objects.live(),
		operator='or'  # 使用更通用的参数
	)
	
	# 格式化结果
	results = []
	for page in search_results:
		results.append({
			'id': page.id,
			'title': page.title,
			'url': page.url if hasattr(page, 'url') else None,
			'type': page.specific_class.__name__
		})
	
	return JsonResponse({
		'query': query,
		'results_count': len(results),
		'results': results
	})


class AuthorListView(ListView):
	"""
	显示作者列表，支持搜索和分页。
	"""
	model = Author
	template_name = 'blog/author_list.html'
	context_object_name = 'authors'
	paginate_by = 10  # 每页显示 10 位作者
	
	def get_queryset(self):
		queryset = super().get_queryset()
		search_query = self.request.GET.get('q')  # 获取搜索参数 'q'
		page_number = self.request.GET.get('page')
		
		if search_query:
			# 如果有搜索参数，则根据姓名过滤
			queryset = queryset.filter(name__icontains=search_query)
		# 分页
		
		
		
		return queryset.order_by('name')  # 按姓名排序
	
	def get_context_data(self, **kwargs):
		# 获取上下文数据
		context = super().get_context_data(**kwargs)
		# 将搜索查询传递给模板，以便在搜索框中显示
		context['search_query'] = self.request.GET.get('q', '')
		return context


class AuthorDetailView(DetailView):
	"""
	显示单个作者的详细信息及其发表的文章。
	"""
	model = Author
	template_name = 'blog/author_detail.html'
	context_object_name = 'author'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		author = self.get_object()
		
		# 获取该作者的所有已发布的博客文章 (按日期倒序)
		# 注意: 这假设你的 BlogPage 模型有一个 'authors' 字段 (ManyToManyField 或 ForeignKey)
		# 并且 BlogPage 是 'live' (已发布) 的。你需要根据你的 BlogPage 模型调整。
		context['blog_posts'] = BlogPage.objects.live().filter(authors=author).order_by('-date')
		
		return context
