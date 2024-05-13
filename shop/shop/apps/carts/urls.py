#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path,include
from .views import *
urlpatterns = [
    # 购物车管理
    re_path(r'^carts/$',CartsView.as_view(),name='info'),
    # 全选购物车
    re_path(r'^carts/selection/$',CartsSelectAllView.as_view()),
    # 展示购物车
    re_path(r'^carts/simple/$',CartsSimpleView.as_view()),
]