#!/user/bin/env python3
# -*- coding: utf-8 -*-

from django import template
from wagtail.models import Site

from base.models import FooterText

register = template.Library()  # 使用它来创建和呈现模板标签和过滤器。

# 注册了名为 get_footer_text 的包含标签的装饰器
# inclusion_tag 是 Django 模板标签的一个装饰器，用于创建包含标签。
# takes_context=True 表示 footer_text.html 模板的上下文将作为参数传递给包含标签函数。
# context 表示您将使用该标签的模板 context
@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    """获取网站页脚的文本内容，并将其传递给一个模板 (base/includes/footer_text.html) 进行渲染。"""
    
    # footer_text 存储任何检索到的值。如果上下文中没有 footer_text 值，则变量存储空字符串 "" 。
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()  # 获取 FooterText 模型的第一个实例
        footer_text = instance.body if instance else "" # 如果实例存在，则获取实例的正文，否则返回空字符串

    return {
        "footer_text": footer_text,
    }

"""如何创建网站菜单，以便在添加时链接到您的主页和其他页面。网站菜单将出现在您的作品集网站的所有页面上，就像您的页脚一样。"""
# 注册了名为 get_site_root 的简单标签
# simple_tag 是 Django 模板标签的一个装饰器，用于创建简单的模板标签。
# takes_context=True 表示 get_site_root 函数将接收模板上下文作为参数。
@register.simple_tag(takes_context=True)
def get_site_root(context):
    
    # 用于查找与当前请求关联的站点的根页面。
    return Site.find_for_request(context["request"]).root_page