from django import template
from django.db.models import Count

from blog.models import BlogPage, BlogCategory
from taggit.models import Tag

register = template.Library()


@register.simple_tag
def get_blog_categories():
	"""获取所有博客分类，并按文章数量排序"""
	return BlogCategory.objects.annotate(
		post_count=Count('blogpage')
	).filter(post_count__gt=0).order_by('-post_count')


@register.simple_tag
def get_popular_tags(limit=10):
	"""获取热门标签，按文章数量排序"""
	return Tag.objects.annotate(
		post_count=Count('taggit_taggeditem_items')
	).filter(post_count__gt=0).order_by('-post_count')[:limit]


@register.simple_tag
def get_recent_posts(limit=5):
	"""获取最近发布的文章"""
	return BlogPage.objects.live().order_by('-date')[:limit]


@register.simple_tag
def get_related_posts(page, limit=3):
	"""获取相关文章"""
	return page.get_related_posts()[:limit] if hasattr(page, 'get_related_posts') else []


@register.inclusion_tag('blog/tags/categories_list.html', takes_context=True)
def categories_list(context):
	"""显示分类列表"""
	categories = get_blog_categories()
	return {
		'categories': categories,
		'request': context['request'],
	}


@register.inclusion_tag('blog/tags/tags_cloud.html', takes_context=True)
def tags_cloud(context, limit=20):
	"""显示标签云"""
	tags = get_popular_tags(limit=limit)
	return {
		'tags': tags,
		'request': context['request'],
	}


@register.inclusion_tag('blog/tags/recent_posts.html', takes_context=True)
def recent_posts_list(context, limit=5):
	"""显示最近文章列表"""
	posts = get_recent_posts(limit=limit)
	return {
		'recent_posts': posts,
		'request': context['request'],
	}


@register.filter
def get_first_image(page):
	"""获取博客页面的第一张图片"""
	for block in page.body:
		if block.block_type == 'image':
			return block.value
	return None


@register.filter
def format_date_cn(date):
	"""格式化日期为中文显示"""
	months = [
		"一月", "二月", "三月", "四月", "五月", "六月",
		"七月", "八月", "九月", "十月", "十一月", "十二月"
	]
	
	month_name = months[date.month - 1]
	return f"{date.year}年{month_name}{date.day}日"