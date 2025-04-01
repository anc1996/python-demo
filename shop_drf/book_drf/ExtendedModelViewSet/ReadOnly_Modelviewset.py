#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.filters import BookInfoFilter
from books.models import BookInfo



"""

ReadOnlyModelViewSet
    继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin。
"""

class Books(ReadOnlyModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    # 3、要指定当前视图使用的过滤器
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Corrected filter_backends
    filterset_class = BookInfoFilter
    ordering_fields = ['readcount', 'commentcount', 'pub_date']  # Added ordering_fields
    
    # 由于ModelViewSet只继承ModelMixin的2个类list、retrieve方法,不需要重写