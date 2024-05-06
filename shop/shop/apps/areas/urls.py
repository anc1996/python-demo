#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *

urlpatterns = [
    # 提供省市区页面
    re_path(r'^areas/$', AreasView.as_view(), name='area'),
]