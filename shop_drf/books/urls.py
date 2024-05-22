#!/user/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from .views import *
urlpatterns = [
    # 对多个书操作
    re_path(r'^BooksView/$', BooksView.as_view()),
    # 对单一书操作
    re_path(r'^BookView/(?P<pk>\d+)/$', BookView.as_view()),
]
