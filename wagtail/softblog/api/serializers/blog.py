"""
博客应用的 API 序列化器
"""

from rest_framework import serializers
from wagtail.images.shortcuts import get_rendition_or_not_found
from blog.models import BlogPage, BlogIndexPage
from .stream_field import StreamFieldSerializer


class BlogIndexPageSerializer(serializers.ModelSerializer):
	"""
	博客索引页序列化器
	"""
	
	class Meta:
		model = BlogIndexPage
		fields = ['id', 'title', 'intro', 'slug', 'url_path']


class BlogPageListSerializer(serializers.ModelSerializer):
	"""
	用于列表显示的博客页面序列化器
	"""
	url = serializers.SerializerMethodField()
	featured_image = serializers.SerializerMethodField()
	
	class Meta:
		model = BlogPage
		fields = [
			'id', 'title', 'slug', 'url', 'date',
			'author', 'intro', 'featured_image'
		]
	
	def get_url(self, obj):
		"""获取博客文章的 URL"""
		return obj.url
	
	def get_featured_image(self, obj):
		"""获取特色图片信息"""
		if not obj.featured_image:
			return None
		
		# 获取不同尺寸的图片
		try:
			rendition = get_rendition_or_not_found(obj.featured_image, 'fill-400x240')
			return {
				'id': obj.featured_image.id,
				'title': obj.featured_image.title,
				'thumbnail': rendition.url,
				'full': obj.featured_image.file.url,
				'width': rendition.width,
				'height': rendition.height,
				'alt': obj.featured_image.title,
			}
		except Exception as e:
			# 如果图片处理失败，返回原始路径
			return {
				'id': obj.featured_image.id,
				'title': obj.featured_image.title,
				'full': obj.featured_image.file.url,
				'alt': obj.featured_image.title,
			}


class BlogPageDetailSerializer(serializers.ModelSerializer):
	"""
	博客页面详情序列化器
	"""
	url = serializers.SerializerMethodField()
	featured_image = serializers.SerializerMethodField()
	body = serializers.SerializerMethodField()
	
	class Meta:
		model = BlogPage
		fields = [
			'id', 'title', 'slug', 'url', 'date',
			'author', 'intro', 'featured_image', 'body'
		]
	
	def get_url(self, obj):
		"""获取博客文章的 URL"""
		return obj.url
	
	def get_featured_image(self, obj):
		"""获取特色图片信息"""
		if not obj.featured_image:
			return None
		
		# 获取不同尺寸的图片
		try:
			rendition = get_rendition_or_not_found(obj.featured_image, 'fill-1200x600')
			return {
				'id': obj.featured_image.id,
				'title': obj.featured_image.title,
				'thumbnail': rendition.url,
				'full': obj.featured_image.file.url,
				'width': rendition.width,
				'height': rendition.height,
				'alt': obj.featured_image.title,
			}
		except Exception as e:
			# 如果图片处理失败，返回原始路径
			return {
				'id': obj.featured_image.id,
				'title': obj.featured_image.title,
				'full': obj.featured_image.file.url,
				'alt': obj.featured_image.title,
			}
	
	def get_body(self, obj):
		"""序列化 StreamField 内容"""
		serializer = StreamFieldSerializer()
		return serializer.to_representation(obj.body)