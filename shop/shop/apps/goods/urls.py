#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *

urlpatterns = [
    # 商品列表页
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$',ListView.as_view(),name='list'),
    # 商品热销排行
    re_path(r'^hot/(?P<category_id>\d+)/$',HotGoodsView.as_view()),
    # 商品详情
    re_path(r'^detail/(?P<sku_id>\d+)/$',DetailView.as_view(),name='detail'),
    # 商品统计
    re_path(r'^detail/visit/(?P<category_id>\d+)/$',DetailVisitView.as_view()),

]