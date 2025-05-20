from django.db import models
from wagtail.admin.panels import FieldPanel

from wagtail.models import Page
from wagtail.fields import RichTextField

class HomePage(Page):
    # body 是一个 RichTextField，一种特殊的 Wagtail 字段。blank=True 表示这个字段不是必须的，可以留空。你可以使用任何 Django 的核心字段。
    body = RichTextField(blank=True) # 主页的正文内容

    # content_panels 定义了编辑界面的功能和布局。将字段添加到 content_panels 让你可以在 Wagtail 后台编辑它们。
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
