from django.db import models
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock  # 修正导入路径
from wagtailmedia.blocks import AbstractMediaChooserBlock, AudioChooserBlock, VideoChooserBlock


# 创建自定义媒体块以自定义渲染
class CustomMediaBlock(AbstractMediaChooserBlock):
	def render_basic(self, value, context=None):
		if not value:
			return ""
		
		if value.type == "video":
			player_code = """
            <div class="media-block video-block">
                <video width="100%" controls>
                    {0}
                    您的浏览器不支持视频播放。
                </video>
                {1}
            </div>
            """
		else:
			player_code = """
            <div class="media-block audio-block">
                <audio controls>
                    {0}
                    您的浏览器不支持音频播放。
                </audio>
                {1}
            </div>
            """
		
		# 构建可能的标题
		title_html = ""
		if hasattr(value, 'title') and value.title:
			title_html = format_html('<p class="media-title">{0}</p>', value.title)
		
		# 获取媒体源
		sources = []
		if hasattr(value, 'sources'):
			sources = value.sources
		elif hasattr(value, 'file') and value.file:
			file_url = value.file.url
			file_ext = file_url.split('.')[-1].lower()
			mime_type = f"video/{file_ext}" if value.type == "video" else f"audio/{file_ext}"
			sources = [{'src': file_url, 'type': mime_type}]
		
		return format_html(
			player_code,
			format_html_join("\n", "<source{0}>", [[flatatt(s)] for s in sources]),
			title_html
		)


class BlogIndexPage(Page):
	"""博客文章列表页面"""
	
	intro = models.TextField("页面介绍", blank=True)
	
	content_panels = Page.content_panels + [
		FieldPanel('intro')
	]
	
	def get_context(self, request):
		context = super().get_context(request)
		# 获取所有已发布的博客文章
		blogpages = BlogPage.objects.live().order_by('-date')
		context['blogpages'] = blogpages
		return context
	
	class Meta:
		verbose_name = "博客索引页"
		verbose_name_plural = "博客索引页"


class BlogPage(Page):
	"""技术博客文章页面"""
	
	# 基本信息
	date = models.DateField("发布日期")
	author = models.CharField("作者", max_length=255, blank=True)
	intro = models.TextField("简介", max_length=250)
	featured_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+',
		verbose_name="特色图片"
	)
	
	# 内容主体 - 混合编辑器支持
	body = StreamField([
		# 富文本块 - 使用Wagtail内置编辑器
		('rich_text', blocks.RichTextBlock(
			features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic',
			          'ol', 'ul', 'hr', 'link', 'document-link', 'image',
			          'embed', 'code', 'superscript', 'subscript', 'strikethrough',
			          'blockquote'],
			label="富文本"
		)),
		
		# Markdown块 - 使用wagtail-markdown (包含代码高亮和数学公式支持)
		('markdown', MarkdownBlock(
			icon='code',
			label="Markdown"
		)),
		
		# 表格块
		('table', TableBlock(
			label="表格"
		)),
		
		# 媒体块 - 支持音频和视频
		('media', CustomMediaBlock(
			icon='media',
			label="媒体"
		)),
		
		# 专用音频块
		('audio', AudioChooserBlock(
			icon='media',
			label="音频"
		)),
		
		# 专用视频块
		('video', VideoChooserBlock(
			icon='media',
			label="视频"
		)),
		
		# 嵌入块 - 用于嵌入外部内容
		('embed', EmbedBlock(
			label="嵌入媒体",
			help_text="从YouTube、Vimeo等插入内容"
		)),
		
		# 原始HTML - 高级用户使用
		('raw_html', blocks.RawHTMLBlock(
			label="原始HTML",
			help_text="适用于高级用户的HTML代码插入"
		)),
	], use_json_field=True, verbose_name="内容主体")
	
	# 搜索配置
	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]
	
	# 管理界面配置
	content_panels = Page.content_panels + [
		FieldPanel('author'),
		FieldPanel('date'),
		FieldPanel('intro'),
		FieldPanel('featured_image'),
		FieldPanel('body'),
	]
	
	class Meta:
		verbose_name = "技术博客"
		verbose_name_plural = "技术博客"