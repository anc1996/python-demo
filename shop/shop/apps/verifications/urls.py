#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *

urlpatterns = [
    # 首页广告，反向解析写法：IndexView.register
    # \w 匹配任何字母、数字或下划线。- 匹配短横线。+ 表示匹配前面的字符（字母、数字、下划线或短横线）一次或多次。
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',ImageCodeView.as_view(),name='image_codes'),
    # 短信验证码
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/',SMSCodeView.as_view(),name='sms_codes'),
]