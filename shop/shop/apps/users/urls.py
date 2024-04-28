#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *


urlpatterns = [
    # 用户注册，反向解析写法：reverse(users:register)
    re_path(r'^register/$', RegisterView.as_view(), name='register'),
]