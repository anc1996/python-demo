#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import *

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.filters import BookInfoFilter
from books.models import BookInfo

logger=logging.getLogger('BasicAPIView')
class Books(GenericAPIView):

    """
        GenericAPIView扩展了REST框架的 APIView 类，为标准list和detail view 添加了通常需要的行为。
        支持定义的属性：
        列表视图与详情视图通用：
            queryset - 用于从视图返回对象的查询结果集。通常，你必须设置此属性或者重写 get_queryset() 方法
            serializer_class - 用于验证和反序列化输入以及用于序列化输出的Serializer类。 通常，你必须设置此属性或者重写get_serializer_class() 方法。
        列表视图使用：
            pagination_class - 当分页列出结果时应使用的分页类。。默认值与 DEFAULT_PAGINATION_CLASS 设置的值相同
            filter_backends - 用于过滤查询集的过滤器后端类的列表。默认值与DEFAULT_FILTER_BACKENDS 设置的值相同。
        详情页视图使用：
            lookup_field - 用于执行各个model实例的对象查找的model字段。默认为 'pk'。 请注意，在使用超链接API时，如果需要使用自定义的值，你需要确保在API视图和序列化类都设置查找字段。
            lookup_url_kwarg - 应用于对象查找的URL关键字参数。它的 URL conf 应该包括一个与这个值相对应的关键字参数。如果取消设置，默认情况下使用与 lookup_field相同的值。
    """
    
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    # 3、要指定当前视图使用的过滤器
    filter_backends = [DjangoFilterBackend,OrderingFilter]  # Corrected filter_backends
    filterset_class = BookInfoFilter  # Added filterset_class
    ordering_fields = ['readcount', 'commentcount', 'pub_date']  # Added ordering_fields
    
    
    def get(self,request):
        """/book_drf/Gapibooks/"""
        # 1、获取查询集中的所有数据
        filtered_queryset=self.filter_queryset(self.get_queryset())
        # 2、分页
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            # 4. 序列化分页后的数据
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response()方法返回一个分页响应，包含序列化数据和分页信息。
            return self.get_paginated_response(serializer.data)
        serializer=self.get_serializer(page,many=True)
        return Response(serializer.data)

    """新增保存图书"""
    def post(self, request):
        
        # 1、请求体获取数据
        data_dict=request.data
        if not data_dict:
            return Response({'error':'数据为空'},status=HTTP_400_BAD_REQUEST)
        
        book=BookInfo.objects.filter(name=data_dict.get('name')).first()
        # 2、验证数据
        if book:
            book_serializer=BookSerializer(book,data=data_dict)
        else:
            book_serializer=BookSerializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        book_serializer.is_valid(raise_exception=True) # 验证方法
        # 3、保存数据
        book_serializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(book_serializer.data)


class BookView(GenericAPIView):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    
    
    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            # get_object(self) 返回详情视图所需的模型类数据对象，
            # 默认使用lookup_field参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。
                # get_object(self)中self.lookup_field获取了pk值
            book =self.get_object() # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        #  返回一个序列化器的实例。
        book_serializer = self.get_serializer(book)
        return Response(book_serializer.data)

    """更新单一图书"""

    def put(self, request, pk):
        # 1、获取数据
        book_dict=request.data
        
        # 2、验证数据库是否有数据
        try:
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        
        # 3、验证数据
        book_serializer = BookSerializer(book,data=book_dict)
        book_serializer.is_valid()
        # 4、更新数据
        book_serializer.save()
        # 6、返回结果
        return Response(book_serializer.data)

    def delete(self,request,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        book.delete()
        return Response({'msg':'删除成功'},status=HTTP_204_NO_CONTENT)