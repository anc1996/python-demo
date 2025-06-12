# comments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import BlogPageComment


@receiver(post_save, sender=BlogPageComment)
def notify_new_comment(sender, instance, created, **kwargs):
	"""新评论通知"""
	if not created or instance.status != 'approved':
		return
	
	# 获取站点管理员邮箱
	admin_email = getattr(settings, 'ADMIN_EMAIL', None)
	if not admin_email:
		return
	
	# 准备通知内容
	edit_url = reverse('wagtail_modeladmin_comments_blogpagecomment:edit', args=[instance.id])
	
	context = {
		'comment': instance,
		'page': instance.page,
		'admin_url': settings.WAGTAILADMIN_BASE_URL + edit_url
	}
	
	# 发送邮件通知
	subject = f'新评论: {instance.page.title}'
	html_message = render_to_string('comments/email/new_comment.html', context)
	plain_message = f"收到新评论\n页面: {instance.page.title}\n作者: {instance.author_user.username}\n内容: {instance.content}"
	
	send_mail(
		subject=subject,
		message=plain_message,
		from_email=settings.DEFAULT_FROM_EMAIL,
		recipient_list=[admin_email],
		html_message=html_message
	)
	
	# 如果是回复评论，通知被回复的用户
	if instance.replied_to_user and instance.replied_to_user.email:
		subject = f'您在 {instance.page.title} 的评论收到了新回复'
		
		html_message = render_to_string('comments/email/reply_notification.html', context)
		plain_message = f"您的评论收到了新回复\n页面: {instance.page.title}\n回复者: {instance.author_user.username}\n回复内容: {instance.content}"
		
		send_mail(
			subject=subject,
			message=plain_message,
			from_email=settings.DEFAULT_FROM_EMAIL,
			recipient_list=[instance.replied_to_user.email],
			html_message=html_message
		)