# blog/models.py
from django.db import models
from wagtail_ai.panels import AITitleFieldPanel, AIDescriptionFieldPanel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import RichTextBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtailmarkdown.blocks import MarkdownBlock



class BlogIndexPage(Page):
	"""博客索引页（列表页）"""
	
	# 这个字段没有 'features'，所以它会使用 Wagtail 7.2 的新版块编辑器
	# 它会显示“星星”图标，但需要 'PROVIDERS' 配置才能工作
	intro = RichTextField(blank=True, verbose_name="简介")
	
	content_panels = Page.content_panels + [
		FieldPanel('intro'),
	]
	
	class Meta:
		verbose_name = "博客索引页"
		verbose_name_plural = "博客索引页"
	
	def get_context(self, request):
		context = super().get_context(request)
		blog_pages = BlogPage.objects.live().public().order_by('-date')
		context['blog_pages'] = blog_pages
		return context


class BlogPage(Page):
	"""博客页面 - 集成 AI 辅助写作"""
	
	date = models.DateField("发布日期", auto_now_add=True)
	
	# 这个字段有 'features'，所以它会使用旧版 Draftail 编辑器
	intro = RichTextField(
		"简介",
		features=[
			'ai',  # <--- 1. 添加 'ai'
			'bold', 'italic', 'strikethrough',
			'superscript', 'subscript',  # <--- 2. 确保 'ai' 后面有逗号！
			'link', 'code', 'blockquote'
		],
		help_text="博客简介，选中文字后点击工具栏上的魔法棒图标使用 AI"
	)
	
	body = StreamField([
		# 这个块有 'features'，所以它也会使用旧版 Draftail 编辑器
		('rich_text', RichTextBlock(  # <--- 3. 使用 wagtail.blocks.RichTextBlock
			features=[
				'ai',  # <--- 4. 在这里也添加 'ai'
				'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
				'bold', 'italic', 'ol', 'ul', 'hr',  # <--- 5. 确保 'ai' 后面有逗号！
				'link', 'document-link', 'image', 'embed',
				'code', 'superscript', 'subscript',
				'strikethrough', 'blockquote', 'underline'
			],
			label="富文本（支持 AI）",
			icon='doc-full',
			help_text="AI 功能已启用，请先输入并【选中文字】，工具栏会出现魔法棒"
		)),
		
		('markdown', MarkdownBlock(
			icon='code',
			label="Markdown",
			help_text="支持 Markdown 语法和代码高亮"
		)),
	
	], use_json_field=True, blank=True, null=True)
	
	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
		index.FilterField('date'),
	]
	
	content_panels = [
		AITitleFieldPanel('title'),  # AI 生成标题
		FieldPanel('intro'),
		FieldPanel('body'),
		InlinePanel('gallery_images', label="画廊图片"),
	]
	
	promote_panels = Page.promote_panels + [
		MultiFieldPanel(
			[
				FieldPanel('slug'),
				FieldPanel('seo_title'),
				AIDescriptionFieldPanel('search_description'),  # AI 生成 SEO 描述
			],
			heading="SEO 设置",
		),
	]
	
	class Meta:
		verbose_name = "博客文章"
		verbose_name_plural = "博客文章"


class BlogPageGalleryImage(Orderable):
	"""博客画廊图片"""
	
	page = ParentalKey(
		BlogPage,
		on_delete=models.CASCADE,
		related_name='gallery_images'
	)
	image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.CASCADE,
		related_name='+'
	)
	caption = models.CharField("图片说明", blank=True, max_length=250)
	
	panels = [
		FieldPanel('image'),
		FieldPanel('caption'),
	]