#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path

from orders.views import OrderSettlementView, OrderCommitView, OrderSuccessView, UserOrderInfoView, OrderCommentView, \
    GoodsCommentView

urlpatterns = [
    # 结算订单
    re_path(r'^orders/settlement/$',OrderSettlementView.as_view(),name='settlement'),
    # 提交订单
    re_path(r'^orders/commit/$',OrderCommitView.as_view()),
    # 提交订单成功
    re_path(r'^orders/success/$',OrderSuccessView.as_view()),
    # 展示订单
    re_path(r'^orders/info/(?P<page_num>\d+)/$',UserOrderInfoView.as_view(),name='info'),
    # 订单商品订单
    re_path(r'^orders/comment/$',OrderCommentView.as_view(),name='goods'),
    # 展示商品评价信息
    re_path(r'^comments/(?P<sku_id>\d+)/$',GoodsCommentView.as_view(),name='comment'),
]