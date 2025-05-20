#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.utils.html import format_html
from django.templatetags.static import static
from django.urls import path, include,reverse


from wagtail.admin.menu import MenuItem
from wagtail import hooks

# 导入你的视图函数
from .views import video_management, video_upload  # 添加这一行


from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

# 注册自定义 JS 和 CSS
@hooks.register('insert_global_admin_js')
def global_admin_js():
    """添加全局管理界面 JS"""
    return format_html(
        '<script src="{}"></script>',
        static('js/admin/blog_admin.js')
    )

@hooks.register('insert_global_admin_css')
def global_admin_css():
    """添加全局管理界面 CSS"""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/admin/blog_admin.css')
    )

# 在编辑器加载前获取 MongoDB 内容
@hooks.register('before_edit_page')
def before_edit_page(request, page):
    """在编辑页面前从 MongoDB 获取内容"""
    if hasattr(page, 'get_content_from_mongodb') and hasattr(page, 'body'):
        try:
            # 获取MongoDB内容
            content = page.get_content_from_mongodb()
            if content and 'body' in content:
                # 重要：不要直接设置raw_data，而是构建StreamValue
                from wagtail.blocks.stream_block import StreamValue
                from wagtail.blocks.stream_block import StreamBlock
                
                # 找到body字段对应的StreamBlock定义
                stream_block = page.body.stream_block
                
                # 创建新的StreamValue
                page.body = StreamValue(stream_block, content['body'], is_lazy=True)
                
                print(f"成功从MongoDB加载内容到页面 {page.id}")
        except Exception as e:
            import traceback
            print(f"从MongoDB加载内容到页面时出错: {e}")
            print(traceback.format_exc())
            

# 注册 Markdown 编辑器 JS
@hooks.register('insert_editor_js')
def editor_js():
    """添加 Markdown 编辑器 JS"""
    return format_html(
        '<script src="{}"></script>',
        static('js/admin/markdown_editor.js')
    )

