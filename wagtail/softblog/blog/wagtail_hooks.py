from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static

@hooks.register('insert_global_admin_css')
def global_admin_css():
    """添加自定义管理界面CSS"""
    return format_html('<link rel="stylesheet" href="{}">', static('css/custom-admin.css'))

@hooks.register('insert_global_admin_js', order=100)
def markdown_editor_js():
    """添加自定义Markdown编辑器配置"""
    return format_html('<script src="{}"></script>', static('js/easymde_custom.js'))