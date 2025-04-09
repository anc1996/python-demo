#!/user/bin/env python3
# -*- coding: utf-8 -*-

# base应用

"""您为通用应用中的不同内容类型创建了可重复使用的 Wagtail 自定义块。
您可以按任意顺序在整个网站上使用这些块。"""
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock

class CaptionedImageBlock(StructBlock):
	"""CaptionedImageBlock 是一个编辑器可以用来将图像添加到 StreamField 部分的块。"""
	
	# StructBlock允许你在 StreamField 中创建可重复使用的、具有固定字段组合的块。 您的 CaptionedImageBlock 有三个子块。
	
	# ImageBlock是一个用于处理图像的块，required=True表示该字段是必需的
	image = ImageBlock(required=True)
	# CharBlock是一个用于处理文本的块，required=False表示该字段不是必需的
	caption = CharBlock(required=False)
	attribution = CharBlock(required=False) # 图片来源
	
	class Meta:
	    icon = "image" # 图像
	    template = "base/blocks/captioned_image_block.html"


class HeadingBlock(StructBlock):
	
	
    heading_text = CharBlock(classname="title", required=True) # 标题文本,required=True表示该字段是必需的
    # 第二个子块 size 使用 ChoiceBlock 来选择标题大小。它为 h2 、 h3 和 h4 提供选项。
    size = ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,# 允许空值
        required=False, # 该字段不是必需的
    )

    class Meta:
        icon = "title"
        template = "base/blocks/heading_block.html"

"""
	StreamBlock 用于定义可包含其他块的块，是构建灵活和动态内容结构的关键组件。 它可以让你创建嵌套的、可重复使用的块结构。
		块的容器： StreamBlock 本身是一个块，但它主要作为其他块的容器存在。它可以包含任何类型的块。
		嵌套结构： 你可以将 StreamBlock 嵌套在另一个 StreamBlock 中，从而创建多层次的、复杂的结构。
		顺序和组合： 在 StreamBlock 中，你可以定义允许的块的类型以及它们的顺序和组合方式。
		动态内容结构： 允许用户在编辑页面时动态地添加、删除和重新排列块。
	与 StructBlock 相比，StreamBlock 主要区别在于它包含的是块的列表，而不是具体的字段。
		这些块可以是任何 Wagtail 提供的块，包括 StructBlock, CharBlock, ImageChooserBlock，甚至其他的 StreamBlock。
"""
class BaseStreamBlock(StreamBlock):
	
    heading_block = HeadingBlock()
    # RichTextBlock 创建格式化文本的所见即所得编辑器，icon="pilcrow" 表示它在 Wagtail 后台的图标
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
    
    # EmbedBlock 用于嵌入视频或其他媒体内容，icon="media" 表示它在 Wagtail 后台的图标
    embed_block = EmbedBlock(
        help_text="插入要嵌入的 URL。例如, https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
    )
    

