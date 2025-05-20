#!/user/bin/env python3
# -*- coding: utf-8 -*-
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _

# 这个blocks.py文件定义了一些自定义的Wagtail块，用于在博客文章中使用。

class HeadingBlock(blocks.StructBlock):
	"""标题块"""
	heading_text = blocks.CharBlock(required=True) # 标题文本
	level = blocks.ChoiceBlock( # 标题级别
		choices=[
			('h2', 'H2'),
			('h3', 'H3'),
			('h4', 'H4'),
			('h5', 'H5'),
			('h6', 'H6'),
		],
		default='h2'
	)
	
	class Meta:
		icon = 'title' # 标题图标
		template = 'blog/blocks/heading_block.html'
		label = _('标题')


class RichTextBlock(blocks.RichTextBlock):
	"""富文本块"""
	
	class Meta:
		icon = 'doc-full' # 文档图标
		template = 'blog/blocks/richtext_block.html'
		label = _('段落')


class CodeBlock(blocks.StructBlock):
	"""代码块，带有代码高亮功能"""
	language = blocks.ChoiceBlock( # 编程语言选择
		choices=[
			('python', 'Python'),
			('javascript', 'JavaScript'),
			('html', 'HTML'),
			('css', 'CSS'),
			('bash', 'Bash/Shell'),
			('sql', 'SQL'),
			('java', 'Java'),
			('cpp', 'C++'),
			('csharp', 'C#'),
			('php', 'PHP'),
			('ruby', 'Ruby'),
			('go', 'Go'),
			('rust', 'Rust'),
			('typescript', 'TypeScript'),
			('swift', 'Swift'),
			('kotlin', 'Kotlin'),
			('scala', 'Scala'),
			('r', 'R'),
			('dart', 'Dart'),
			('plaintext', '纯文本'),
		],
		default='python'
	)
	code = blocks.TextBlock() # 代码文本
	show_line_numbers = blocks.BooleanBlock(required=False, default=True) # 是否显示行号
	
	class Meta:
		icon = 'code'
		template = 'blog/blocks/code_block.html'
		label = _('代码块')


class MathFormulaBlock(blocks.StructBlock):
	"""数学公式块，使用KaTeX或MathJax渲染"""
	formula = blocks.TextBlock(help_text=_('使用LaTeX语法输入数学公式'))
	display_mode = blocks.BooleanBlock( # 显示模式选择
		required=False,
		default=True,
		help_text=_('选择是否使用显示模式（display mode）')
	)
	
	class Meta:
		icon = 'superscript'
		template = 'blog/blocks/math_formula_block.html'
		label = _('数学公式')


class MarkdownBlock(blocks.TextBlock):
	"""Markdown块，允许直接使用Markdown语法"""
	
	class Meta:
		icon = 'pilcrow'
		template = 'blog/blocks/markdown_block.html'
		label = _('Markdown')


class QuoteBlock(blocks.StructBlock):
	"""引用块"""
	text = blocks.TextBlock() # 引用文本
	source = blocks.CharBlock(required=False) # 引用来源
	
	class Meta:
		icon = 'openquote'
		template = 'blog/blocks/quote_block.html'
		label = _('引用')


class ImageWithCaptionBlock(blocks.StructBlock):
	"""带标题的图片块"""
	image = ImageChooserBlock() # 图片选择
	caption = blocks.CharBlock(required=False)
	alignment = blocks.ChoiceBlock(
		choices=[
			('left', '左对齐'),
			('center', '居中'),
			('right', '右对齐'),
		],
		default='center'
	)
	
	class Meta:
		icon = 'image'
		template = 'blog/blocks/image_with_caption_block.html'
		label = _('带标题图片')