#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path

from .views import *
urlpatterns = [
    # 全后端不分离模式，返回的是html页面
    re_path(r'^index1/$',Index1View.as_view()),
    # 全后端分离模式，返回的是json数据
    re_path(r'^index2/$',Index2View.as_view()),
    # 登录
    re_path(r'^login/$',LoginView.as_view()),
    # 获取图书按钮
    re_path(r'^(?P<pk>\d+)/$',BookView.as_view()),

]
