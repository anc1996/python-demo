from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.documents.models import Document, AbstractDocument
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from utils.mongo import MongoManager


# 自定义图片模型
class BlogImage(AbstractImage):
	"""自定义博客图片模型"""
	caption = models.CharField(max_length=255, blank=True)
	
	admin_form_fields = Image.admin_form_fields + ('caption',)
	
	@property
	def default_alt_text(self):
		# 如果没有指定alt文本，使用caption作为替代
		return self.caption or self.title


class BlogRendition(AbstractRendition):
	"""博客图片渲染模型"""
	image = models.ForeignKey(
		'BlogImage',
		on_delete=models.CASCADE,
		related_name='renditions'
	)
	
	class Meta:
		unique_together = (
			('image', 'filter_spec', 'focal_point_key'),
		)


# 自定义文档模型
class BlogDocument(AbstractDocument):
	"""自定义博客文档模型"""
	description = models.TextField(blank=True)
	
	admin_form_fields = Document.admin_form_fields + ('description',)


# 标签模型
class BlogPageTag(TaggedItemBase):
	"""博客页面标签"""
	content_object = ParentalKey(
		'BlogPage',
		related_name='tagged_items',
		on_delete=models.CASCADE
	)


# 博客分类
@register_snippet
class BlogCategory(models.Model):
	"""博客分类"""
	name = models.CharField(max_length=255)
	icon = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	
	panels = [
		FieldPanel('name'),
		FieldPanel('icon'),
	]
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "博客分类"
		verbose_name_plural = "博客分类"


# 自定义 Markdown 块
class MarkdownBlock(blocks.TextBlock):
	"""Markdown 内容块"""
	
	class Meta:
		icon = 'code'
		label = "Markdown块"
		template = 'blog/blocks/markdown_block.html'


# 自定义视频块
class VideoBlock(blocks.StructBlock):
	"""视频内容块"""
	video_type = blocks.ChoiceBlock(choices=[
		('upload', '上传视频'),
		('youtube', 'YouTube链接'),
		('bilibili', 'Bilibili链接'),
		('vimeo', 'Vimeo链接'),
	], icon='media', label='视频类型')
	
	# 上传视频路径
	uploaded_video_path = blocks.CharBlock(required=False, label='上传视频路径')
	
	# 外部视频链接
	external_video_url = blocks.URLBlock(required=False, label='外部视频链接')
	
	# 视频配置选项
	autoplay = blocks.BooleanBlock(required=False, default=False, label='自动播放')
	loop = blocks.BooleanBlock(required=False, default=False, label='循环播放')
	muted = blocks.BooleanBlock(required=False, default=False, label='静音')
	thumbnail = ImageChooserBlock(required=False, label='视频封面')
	
	class Meta:
		icon = 'media'
		label = '视频块'
		template = 'blog/blocks/video_block.html'


# 博客索引页面
class BlogIndexPage(Page):
	"""博客索引页面"""
	intro = RichTextField(blank=True)
	
	content_panels = Page.content_panels + [
		FieldPanel('intro')
	]
	
	def get_context(self, request):
		# 更新上下文以包含分页的博客页面
		context = super().get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context


# 博客页面
class BlogPage(Page):
	"""博客页面，内容存储在 MongoDB"""
	date = models.DateField("发布日期")
	intro = models.CharField("简介", max_length=250)
	mongo_content_id = models.CharField("MongoDB内容ID", max_length=50, blank=True, null=True)
	
	# 使用 StreamField 定义四种内容块
	# 修改 StreamField 定义，将其设为空字段，但保留编辑界面
	body = StreamField([
		('document_block', DocumentChooserBlock(icon='doc-full', label="文档块")),
		('image_block', ImageChooserBlock(icon='image', label="图片块")),
		('video_block', VideoBlock(icon='media', label="视频块")),
		('markdown_block', MarkdownBlock(icon='code', label="Markdown块")),
	], use_json_field=True, verbose_name="内容", blank=True, null=True, default=[])
	
	categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
	tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
	
	# 索引字段
	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
		index.FilterField('date'),
		index.FilterField('tags'),
		index.FilterField('categories'),
	]
	
	# 后台编辑面板
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('date'),
			FieldPanel('tags'),
			FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
		], heading="博客信息"),
		FieldPanel('intro'),
		FieldPanel('body'),
	]
	
	def save(self, *args, **kwargs):
		"""重写保存方法，将内容同步到 MongoDB"""
		is_new = self.pk is None
		
		# 保存body的临时副本
		temp_body = self.body
		
		# 清空body，避免存储到MySQL
		self.body = []
		
		# 先调用父类的保存方法保存元数据到 MySQL（此时body为空）
		super().save(*args, **kwargs)
		
		# 恢复body以便后续处理
		self.body = temp_body
		
		# 存储内容到 MongoDB
		mongo_manager = MongoManager()
		
		# 准备要存储的内容数据
		content_data = {
			'page_id': self.pk,
			'title': self.title,
			'intro': self.intro,
			'last_updated': self.last_published_at.isoformat() if self.last_published_at else None,
		}
		
		# 获取body内容
		body_data = []
		try:
			# 将body转换为列表
			if hasattr(self.body, 'raw_data'):
				body_data = list(self.body.raw_data)
			else:
				# 手动构建body数据
				for block in self.body:
					block_data = {
						'type': block.block_type,
						'id': block.id,
						'value': self._get_block_value(block)
					}
					body_data.append(block_data)
		except Exception as e:
			import traceback
			print(f"StreamField数据处理错误: {e}")
			print(traceback.format_exc())
		
		# 添加body数据到content
		content_data['body'] = body_data
		
		# 保存或更新 MongoDB 内容
		content_id = mongo_manager.save_blog_content(content_data, self.mongo_content_id)
		
		# 更新 mongo_content_id 字段（如果是新内容）
		if is_new or not self.mongo_content_id:
			self.mongo_content_id = content_id
			# 更新数据库中的mongo_content_id，同时确保body为空
			self.__class__.objects.filter(pk=self.pk).update(mongo_content_id=content_id, body=[])
	
	def _get_block_value(self, block):
		"""从块中提取可序列化的值"""
		value = block.value
		block_type = block.block_type
		
		if block_type == 'document_block':
			# 文档块：返回文档ID
			return value.id if value else None
		elif block_type == 'image_block':
			# 图片块：返回图片ID
			return value.id if value else None
		elif block_type == 'video_block':
			# 视频块：返回视频配置
			if isinstance(value, dict):
				return value
			# 如果是复杂对象，提取关键属性
			video_data = {
				'video_type': getattr(value, 'video_type', None),
				'uploaded_video_path': getattr(value, 'uploaded_video_path', ''),
				'external_video_url': getattr(value, 'external_video_url', ''),
				'autoplay': getattr(value, 'autoplay', False),
				'loop': getattr(value, 'loop', False),
				'muted': getattr(value, 'muted', False),
				'thumbnail': getattr(value, 'thumbnail', None)
			}
			# 处理缩略图ID
			if video_data['thumbnail'] and hasattr(video_data['thumbnail'], 'id'):
				video_data['thumbnail'] = video_data['thumbnail'].id
			return video_data
		elif block_type == 'markdown_block':
			# Markdown块：直接返回文本内容
			return str(value)
		else:
			# 其他类型：尝试转换为基本类型
			if hasattr(value, 'id'):
				return value.id
			return str(value)
	
	def get_content_from_mongodb(self):
		"""从 MongoDB 获取内容"""
		if not self.mongo_content_id:
			return None
		
		try:
			mongo_manager = MongoManager()
			content = mongo_manager.get_blog_content(self.mongo_content_id)
			
			# 验证内容结构
			if content and 'body' in content and isinstance(content['body'], list):
				return content
			else:
				print(f"从MongoDB获取的内容结构不完整或无效: {content}")
				return None
		except Exception as e:
			import traceback
			print(f"从MongoDB获取内容时出错: {e}")
			print(traceback.format_exc())
			return None
	
	def delete(self, *args, **kwargs):
		"""重写删除方法，同时删除 MongoDB 中的内容"""
		if self.mongo_content_id:
			mongo_manager = MongoManager()
			mongo_manager.delete_blog_content(self.mongo_content_id)
		
		super().delete(*args, **kwargs)