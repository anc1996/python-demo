# blog/templatetags/comment_tags.py

from django import template
from comments.models import BlogPageComment, CommentReaction
from django.core.paginator import Paginator
register = template.Library()


@register.inclusion_tag('comments/tags/comment_block.html', takes_context=True)
def render_comments(context, page):
	"""渲染评论区块"""
	request = context['request']
	
	# 获取一级评论（按热门排序）
	comments = BlogPageComment.objects.filter(
		page=page,
		parent__isnull=True,
		status='approved'
	).select_related('author_user').order_by('-like_count', '-created_at')
	
	# 分页
	
	paginator = Paginator(comments, 20)  # 每页20条
	comments_page = paginator.get_page(1)  # 默认第一页
	
	# 获取用户反应状态
	user_reactions = {}
	if request.user.is_authenticated:
		reactions = CommentReaction.objects.filter(
			comment__in=comments_page,
			user=request.user
		)
		user_reactions = {r.comment_id: r.reaction_type for r in reactions}
	
	# 评论总数
	comment_count = BlogPageComment.objects.filter(
		page=page,
		status='approved'
	).count()
	
	return {
		'page': page,
		'comments': comments_page,
		'comments_page': comments_page,
		'user': request.user,
		'user_reactions': user_reactions,
		'comment_count': comment_count,
		'sort_by': 'hot'  # 默认排序
	}


@register.filter
def get_item(dictionary, key):
	"""获取字典中的项目（用于模板中访问字典）"""
	if dictionary:
		key = str(key)  # 确保键是字符串
		return dictionary.get(key)
	return None