# blog/templatetags/blog_tags.py
from django import template

register = template.Library()


@register.simple_tag
def get_user_reaction(page, request):
	"""获取当前用户对页面的反应"""
	from blog.models import Reaction
	
	if request.user.is_authenticated:
		reaction = Reaction.objects.filter(
			page=page,
			user=request.user
		).values_list('reaction_type_id', flat=True).first()
		return reaction
	elif request.session.session_key:
		reaction = Reaction.objects.filter(
			page=page,
			session_key=request.session.session_key
		).values_list('reaction_type_id', flat=True).first()
		return reaction
	return None