# base/models.py
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,  # 字段面板：用于在 Wagtail 管理界面中显示单个字段的面板。
    MultiFieldPanel,  # 多字段面板：用于在 Wagtail 管理界面中显示多个字段的面板。
    PublishingPanel, InlinePanel, FieldRowPanel  # 发布面板：用于处理与发布相关的操作和信息的面板。
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting, # 定义适用于所有网页（而不仅仅是一个页面）的设置模型。
    register_setting, # 注册设置模型的装饰器。
)
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin, # 草稿状态混合类：用于处理草稿状态的模型混合类。
    PreviewableMixin, # 可预览混合类：用于处理预览功能的模型混合类。
    RevisionMixin, # 修订混合类：用于处理版本控制和修订的模型混合类。
    TranslatableMixin, # 可翻译混合类：用于处理多语言翻译的模型混合类。
)

from wagtail.snippets.models import register_snippet


# register_setting 是一个装饰器，用于将设置模型注册到 Wagtail 的设置系统中。
@register_setting
class NavigationSettings(BaseGenericSetting):
	
	# 定义导航设置的字段
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True) # LinkedIn URL
    github_url = models.URLField(verbose_name="GitHub URL", blank=True) # GitHub URL
    bilibili_url = models.URLField(verbose_name="Bilibili URL", blank=True) # 哔哩哔哩 URL
    wechat_url = models.URLField(verbose_name="WeChat URL", blank=True) # 微信 URL
    instagram_url = models.URLField(verbose_name="Instagram URL", blank=True) # Instagram URL
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('linkedin_url'),
                FieldPanel('github_url'),
                FieldPanel('bilibili_url'),
                FieldPanel('wechat_url'),
                FieldPanel('instagram_url'),
            ],
            "社交链接",
        )
    ]
    
    class Meta:
        verbose_name = "社交链接"

    
@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField() # 页脚文本字段

    panels = [
        FieldPanel("body"),
        PublishingPanel(), # 发布面板：用于处理与发布相关的操作和信息的面板。
    ]

    def __str__(self):
        return "Footer text" # 返回字符串表示形式

    def get_preview_template(self, request, mode_name):
        # 返回预览模板的路径
        return "base.html"

    def get_preview_context(self, request, mode_name):
        # 返回预览上下文
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "页脚文本"
        
#  保留 NavigationSettings 和 FooterText 的定义。添加 FormField 和 FormPage：
class FormField(AbstractFormField):
    """表单字段模型"""
    
    # 父表是 FormPage，FormField : FormPage= 1 : N
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

        
class FormPage(AbstractEmailForm):
    
    """联系人表单页面模型"""
    
    intro = RichTextField(blank=True) # 用于在表单上方显示介绍文本
    thank_you_text = RichTextField(blank=True) # 用于在表单提交成功后显示感谢文本

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(), # 在后台显示表单提交记录
        FieldPanel('intro'), # 在后台编辑 intro 字段
        InlinePanel('form_fields', label="Form fields"), # 允许在后台添加和编辑表单字段
        FieldPanel('thank_you_text'), # 在后台编辑 thank_you_text 字段
        MultiFieldPanel([ # 用于组织电子邮件相关的设置字段
            FieldRowPanel([ # 将 from_address 和 to_address 放在同一行
                FieldPanel('from_address'), # 发件人邮箱地址
                FieldPanel('to_address'), # 收件人邮箱地址
            ]),
            FieldPanel('subject'), # 邮件主题
        ], "Email"), # 面板标题
    ]
    
    class Meta:
        verbose_name = "联系表单"
        verbose_name_plural = "联系表单"

    

