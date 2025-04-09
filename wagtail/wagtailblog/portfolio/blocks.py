#!/user/bin/env python3
# -*- coding: utf-8 -*-
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock, PageChooserBlock
from wagtail.images.blocks import ImageBlock

from base.blocks import BaseStreamBlock


class CardBlock(StructBlock):
	
    """CardBlock 是一个结构块，用于创建一个包含标题、富文本内容和可选图片的卡片式内容块。"""
    
    heading = CharBlock()# 标题块
    text = RichTextBlock(features=["bold", "italic", "link"])# 富文本块,features=["bold", "italic", "link"]表示该字段支持粗体、斜体和链接功能
    image = ImageBlock(required=False) # 图片块,required=False表示该字段不是必需的
    
    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html" # 负责渲染卡片的 HTML 结构和内容。



class FeaturedPostsBlock(StructBlock):
    
    """用于创建一个展示精选文章的块。"""
    
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"], required=False)
    posts = ListBlock(PageChooserBlock(page_type="blog.BlogPage")) # 列表块，允许选择多个页面
    # listBlock 是一个块，它允许你创建一个包含多个相同类型块的列表。它可以包含任何类型的块。
    # PageChooserBlock 是一个块，它允许你选择一个页面作为值。它可以用于选择任何类型的页面。这里将其与 PageChooserBlock 一起使用以仅选择 Blog Page 类型的页面。

    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"


class PortfolioStreamBlock(BaseStreamBlock):
	
    """用于组合 CardBlock 和 FeaturedPostsBlock。 StreamField 允许用户以灵活的方式添加和排序不同的内容块。"""
    
    
    """使用了 group="Sections" 将 card 和 featured_posts 子块归类到名为 section 的类别中。"""
    card = CardBlock(group="Sections")
    # CardBlock 是一个结构块，允许编辑器添加标题、文本和可选的图像。
    # group="Sections" 表示该块属于 "Sections" 组。
    
    featured_posts = FeaturedPostsBlock(group="Sections")
    # FeaturedPostsBlock 是一个结构块，允许编辑器添加标题、文本和可选的图像。
    # group="Sections" 表示该块属于 "Sections" 组。
    

    