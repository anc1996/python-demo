#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *
urlpatterns = [
    # 普通序列化视图操作
    re_path(r'^books/$', Books.as_view()),
    re_path(r'^book/(?P<pk>\d+)/$', Book.as_view()),
]