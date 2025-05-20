# home/models.py

from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField

from blog.models import  BlogIndexPage, BlogImage # 确保导入路径正确

class HomePage(Page):

    # body 是一个 RichTextField，一种特殊的 Wagtail 字段。blank=True 表示这个字段不是必须的，可以留空。你可以使用任何 Django 的核心字段。
    body = RichTextField(blank=True) # 主页的正文内容

    banner_image  = models.ForeignKey(
        'blog.BlogImage', # <-- 使用你自定义的 BlogImage 模型
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )  # 特色图片

    # 添加 CTA 相关的字段
    hero_text = models.CharField(
        blank=True,
        max_length=255,
        help_text="为网站撰写简介"
    ) # 英雄区文本

    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="在行动动员按钮上显示的文本"
    ) # CTA 按钮文本

    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="主召 CTA 链接",
        help_text="选择要链接到行动号召的页面"
    ) # CTA 链接到的页面

    # content_panels 定义了编辑界面的功能和布局。将字段添加到 content_panels 让你可以在 Wagtail 后台编辑它们。
    content_panels = Page.content_panels + [
        # 使用 MultiFieldPanel 将 Hero 区的字段分组
        MultiFieldPanel(
            [
                FieldPanel('banner_image'),
                FieldPanel('hero_text'),
                FieldPanel('hero_cta'),
                FieldPanel('hero_cta_link'),
            ],
            heading="英雄区", # 后台编辑界面的分组标题
        ),
        FieldPanel('body'),  # <-- 添加特色图片到编辑面板
    ]


    # 添加一个方法来获取最新的博客文章和博客索引页面
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # 获取 BlogIndexPage 实例
        # 这里假设你的 BlogIndexPage 是网站中唯一的，或者你可以通过其他方式获取
        blog_index_page = BlogIndexPage.objects.live().first() # 获取第一个 live 的 BlogIndexPage

        if blog_index_page:
            # 获取最新的博客文章，例如获取最近的 5 篇文章
            # 使用 BlogIndexPage 模型自带的 get_context 方法可能会更方便，如果它已经实现了分页和排序
            # 或者直接获取其子页面并排序
            latest_posts = blog_index_page.get_children().live().order_by('-first_published_at')[:5]

            context['latest_posts'] = latest_posts
            context['blog_index'] = blog_index_page # 将 BlogIndexPage 也添加到 context，方便在模板中生成“查看所有文章”的链接

        # 如果您希望在主页上展示其他信息（如热门文章、分类等），可以在这里添加逻辑

        return context

    class Meta:
        verbose_name = "首页"
        verbose_name_plural = "首页"
