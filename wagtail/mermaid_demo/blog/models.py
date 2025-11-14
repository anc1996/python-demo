
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel


# --- 1. 定义我们的 MermaidBlock ---
# 这是一个 StructBlock，它允许我们将多个字段组合在一起。
# 在本例中，我们只需要一个 'code' 字段。

class MermaidBlock(blocks.StructBlock):
	"""
	一个专门用于Mermaid图表代码的StreamField Block。
	"""
	code = blocks.TextBlock(
		label="Mermaid 代码",
		help_text="在此处粘贴您的 Mermaid.js 语法代码 (例如: graph TD; A-->B;)"
	)
	
	class Meta:
		icon = 'code'  # 在编辑器中显示一个代码图标
		label = 'Mermaid 图表'
		# 关键！指定一个模板用于前端渲染
		# 这个路径对应我们在 settings.py 中配置的全局 templates 目录
		template = "blocks/mermaid_block.html"

# --- 2. 创建页面模型 ---


# 这个页面将作为我们博客文章或文档的容器

class BlogPage(Page):
	body = StreamField([
		# ('name', blocks.BlockType())
		('heading', blocks.CharBlock(
			label="大标题",
			icon="title"
		)),
		('paragraph', blocks.RichTextBlock(
			label="段落内容",
			icon="pilcrow"
		)),
		
		# --- 3. 在 StreamField 中注册我们的 MermaidBlock ---
		('mermaid_chart', MermaidBlock()),
	
	], use_json_field=True, blank=True, null=True)  # 允许 body 为空
	
	content_panels = Page.content_panels + [
		FieldPanel('body'),
	]
	
	# --- 4. (重要) 定义子页面类型 ---
	# BlogPage 下面不能再创建子页面
	subpage_types = []