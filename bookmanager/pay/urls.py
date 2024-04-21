#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from pay.views import order
urlpatterns = [
#index/
    # url的第一参数是:正则
    # url的第二参数是:视图函数名
    #pay/order/
    re_path(r'order/$', order)
]