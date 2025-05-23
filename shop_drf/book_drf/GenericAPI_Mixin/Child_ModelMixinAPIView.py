#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.filters import BookInfoFilter
from books.models import BookInfo


class Books(ListCreateAPIView):
    '''ListCreateAPIView继承
        GenericAPIView,CreateModelMixin,ListModelMixin'''
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    # 3、要指定当前视图使用的过滤器
    filter_backends = [DjangoFilterBackend,OrderingFilter]  # Corrected filter_backends
    filterset_class = BookInfoFilter  # Added filterset_class
    ordering_fields = ['readcount', 'commentcount', 'pub_date']  # Added ordering_fields

    
    
    # 由于ListCreateAPIView有get、post方法,不需要写
    """获取所有数据，新增数据"""


class BookView(RetrieveUpdateDestroyAPIView):
    '''RetrieveUpdateDestroyAPIView继承
        GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin'''

    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer


    # 重写DestroyModelMixin的destroy方法
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    """获取、更新、删除单一数据"""
    # 由于RetrieveUpdateDestroyAPIView有get、post、delete方法,不需要写
    
    

