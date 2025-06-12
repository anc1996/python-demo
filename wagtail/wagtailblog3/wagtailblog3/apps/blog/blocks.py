# blog/blocks.py

from wagtail.documents.models import AbstractDocument
from django.db import models
from wagtailmedia.blocks import  AudioChooserBlock, VideoChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.documents.models import Document, AbstractDocument
from django.template.loader import render_to_string


# 自定义文档模型
class BlogDocument(AbstractDocument):
	"""自定义博客文档模型"""
	
	description = models.TextField(blank=True)  # 文档描述
	admin_form_fields = Document.admin_form_fields + ('description',)  # 添加描述字段到后台表单


class AudioBlock(AudioChooserBlock):
	"""音频选择器块 - 使用外部模板渲染，并支持标题"""
	
	def render(self, value, context=None):
		# 调用 render_to_string，将渲染工作交给模板文件
		return render_to_string(
			"blog/streams/audio_block.html",
			{
				'value': value,  # 将完整的音频对象传递给模板
			}
		)


class VideoBlock(VideoChooserBlock):
	"""
	视频选择器块 - 使用外部模板进行Gretzia风格渲染
	"""
	
	def render(self, value, context=None):
		"""
		覆盖 render 方法，使用 video_block.html 模板来渲染。
		"""
		# 即使 value 为 None，我们也渲染模板，
		# 让模板文件内部的 {% if value %} 逻辑来处理空状态。
		return render_to_string(
			"blog/streams/video_block.html",
			{
				'value': value,  # 将整个视频对象 (value) 传递给模板
			}
		)


# 添加自定义TableBlock类
class CustomTableBlock(WagtailTableBlock):
	"""自定义表格块，继承自 Wagtail 的 TableBlock。"""
	
	def render(self, value, context=None):
		"""
		覆盖render方法，使用自定义模板。
		这个实现参考了 Wagtail 官方 TableBlock 的 render 方法，
		以确保所有需要的数据（包括单元格合并信息）都被传递到模板。
		"""
		template = getattr(self.meta, "template", None)
		if not template or not value:
			return ""
		
		# 从 value 中提取数据
		table_header = (
			value["data"][0]
			if value.get("data") and len(value["data"]) > 0 and value.get("first_row_is_table_header")
			else None
		)
		table_data = (
			value["data"][1:] if table_header else value.get("data", [])
		)
		
		# 准备一个新的上下文
		new_context = context.copy() if context else {}
		
		# 更新上下文，加入表格所需的所有变量
		new_context.update({
			'self': value,
			self.TEMPLATE_VAR: value,
			'table_header': table_header,
			'data': table_data,
			'first_col_is_header': value.get("first_col_is_header", False),
			'html_renderer': self.is_html_renderer(),
			'table_caption': value.get("table_caption"),
		})
		
		# --- 新增的关键部分：处理单元格元数据 ---
		# 处理单元格的 CSS 类名
		if value.get("cell"):
			new_context["classnames"] = {
				(meta["row"], meta["col"]): meta["className"]
				for meta in value["cell"] if "className" in meta
			}
		
		# 处理合并单元格 (rowspan/colspan)
		if value.get("mergeCells"):
			new_context["spans"] = {
				(merge["row"], merge["col"]): {
					"rowspan": merge["rowspan"],
					"colspan": merge["colspan"],
				}
				for merge in value["mergeCells"]
			}
		
		return render_to_string(template, new_context)
	
	class Meta:
		template = "blog/streams/table_block.html"
		icon = "table"
		label = "表格"
		help_text = "创建一个包含标题和表头的表格。"