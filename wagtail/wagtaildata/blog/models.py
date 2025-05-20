from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django import forms

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from blog.blocks import (
	CodeBlock,
	MathFormulaBlock,
	MarkdownBlock,
	HeadingBlock,
	QuoteBlock,
	RichTextBlock
)


class BlogIndexPage(Page):
	"""博客索引页，列出所有的博客文章"""
	intro = RichTextField(blank=True) # 简介字段
	
	content_panels = Page.content_panels + [
		FieldPanel('intro')
	] # 内容面板，显示在Wagtail管理界面
	
	def get_context(self, request, *args, **kwargs):
		"""获取上下文数据"""
		
		# 调用父类的get_context方法
		context = super().get_context(request, *args, **kwargs)
		# 获取所有已发布的博客文章
		all_posts = self.get_posts()
		
		# 分页
		paginator = Paginator(all_posts, 10)  # 每页10篇文章
		page = request.GET.get('page')
		try:
			posts = paginator.page(page) # 获取当前页的文章
		except PageNotAnInteger: # 如果请求的页码不是整数
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages) # 如果请求的页码超出范围，返回最后一页
		
		context['posts'] = posts # 将文章列表添加到上下文
		return context
	
	def get_posts(self):
		"""获取所有已发布的博客文章"""
		
		# 使用descendant_of方法获取当前页面的所有子页面,并按发布时间降序排列
		return BlogPage.objects.live().descendant_of(self).order_by('-first_published_at')
	
	class Meta:
		verbose_name = "博客首页"
		verbose_name_plural = "博客首页"


class BlogPageTag(TaggedItemBase):
	"""博客标签模型"""
	
	# 关联到BlogPage模型
	content_object = ParentalKey(
		'BlogPage',
		related_name='tagged_items',
		on_delete=models.CASCADE
	)


class BlogCategory(models.Model):
	"""博客分类模型"""
	
	name = models.CharField(max_length=255) # 分类名称
	slug = models.SlugField(unique=True, max_length=80) # 唯一标识符
	description = models.TextField(blank=True) # 分类描述
	
	panels = [ # Wagtail管理界面显示的字段面板
		FieldPanel('name'),
		FieldPanel('slug'),
		FieldPanel('description'),
	]
	
	def __str__(self):
		"""返回分类名称"""
		return self.name
	
	class Meta:
		verbose_name = "博客分类"
		verbose_name_plural = "博客分类"


class BlogPage(Page):
	"""博客页面模型"""
	# 继承自Wagtail的Page模型
	
	# 定义页面的标题和内容
	date = models.DateField(_("发布日期"))
	intro = models.CharField(_("简介"), max_length=250)
	
	# 使用StreamField提供多种内容块类型
	body = StreamField([
		('heading', HeadingBlock()), # 标题块
		('paragraph', RichTextBlock()), # 段落块
		('code', CodeBlock()), # 代码块
		('math_formula', MathFormulaBlock()), # 数学公式块
		('markdown', MarkdownBlock()), # Markdown块
		('image', ImageChooserBlock()), # 图片块
		('video', EmbedBlock()), # 视频块
		('quote', QuoteBlock()), # 引用块
	], use_json_field=True, verbose_name=_("内容"))
	
	# ParentalManyToManyField用于多对多关系：比如文章与分类的关系
	categories = ParentalManyToManyField('blog.BlogCategory', blank=True) # 分类
	
	# 专门用于标签管理，提供了更丰富的标签功能，
	tags = ClusterTaggableManager(through=BlogPageTag, blank=True) # 标签
	
	# MongoDB存储的附加内容ID (关联到存储在MongoDB的额外内容)
	mongo_content_id = models.CharField(max_length=24, blank=True, null=True,
	                                    help_text=_("MongoDB中存储的额外内容ID"))
	
	# 用于搜索的索引字段
	search_fields = Page.search_fields + [
		index.SearchField('intro'),# 简介搜索
		index.SearchField('body'), # 支持全文搜索
		index.FilterField('date'), # 按日期过滤
		index.RelatedFields('categories', [
			index.SearchField('name'), # 分类名称搜索
		]),
	]
	
	content_panels = Page.content_panels + [ # Wagtail管理界面显示的字段面板
		FieldPanel('date'),
		FieldPanel('intro'),
		FieldPanel('body'),
		MultiFieldPanel([
			FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
			FieldPanel('tags'),
		], heading="分类与标签"),
	]
	
	def get_related_posts(self):
		"""获取相关文章，基于相同标签或分类"""
		# 获取当前博客的标签
		tags = self.tags.all()
		
		# 获取所有已发布的博客文章，排除当前文章
		related_posts = BlogPage.objects.live().exclude(id=self.id)
		
		if tags:
			# 修改这里 - 使用tags__name__in而不是循环使用tags__tag_id
			tag_names = [tag.name for tag in tags]
			related_posts = related_posts.filter(tags__name__in=tag_names)
		
		# 如果找不到相关文章，则尝试使用分类
		if not related_posts.exists():
			categories = self.categories.all() # 获取当前文章的分类
			if categories:
				cat_ids = [cat.id for cat in categories]
				related_posts = BlogPage.objects.live().exclude(id=self.id).filter(
					categories__id__in=cat_ids
				) # 获取相关文章
		
		return related_posts.distinct()[:3]  # 返回至多3篇相关文章
	
	def save(self, *args, **kwargs):
		"""重写保存方法，同步MongoDB内容"""
		# 避免递归调用save方法
		should_sync = kwargs.pop('sync_to_mongo', True)
		
		# 先调用父类的save方法
		super().save(*args, **kwargs)
		
		# 只有当明确要求同步时才执行
		if should_sync:
			from blog.utils import sync_to_mongodb
			sync_to_mongodb(self)
	
	class Meta:
		verbose_name = "博客页面"
		verbose_name_plural = "博客页面"


@receiver(post_save, sender=BlogPage)
def update_blog_search_index(sender, instance, **kwargs):
	"""
	博客保存后更新搜索索引
	- 简化MySQL索引
	- 完整MongoDB内容
	"""
	from wagtail.search.backends import get_search_backend
	search_backend = get_search_backend()
	
	# 更新搜索索引 (我们的自定义后端会处理简化)
	search_backend.add(instance)