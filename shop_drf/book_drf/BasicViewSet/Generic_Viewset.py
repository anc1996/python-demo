#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from rest_framework.status import *
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

logger=logging.getLogger('BasicViewSet')
class Books(GenericViewSet):

    """
        使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
            list() 提供一组数据
            retrieve() 提供单个数据
            create() 创建数据
            update() 保存数据
            destory() 删除数据
        因为 GenericViewSet 类继承自 GenericAPIView，
        并提供了 get_object， get_queryset 方法和其他通用视图基本行为的默认配置，但默认情况不包括任何操作。
    """
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    def list(self,request):
        # 1、获取查询集中的所有数据
        books=self.get_queryset()
        # 2、使用指定序列化器，获取序列化对象
        books_serializer=self.get_serializer(books,many=True)
        return Response(books_serializer.data)

    """新增保存图书"""
    def create(self, request):
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

    """获取单一图书"""
    def retrieve(self,request,pk):
        # 1、查询数据对象
        try:
            book =self.get_object() # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        #  返回一个序列化器的实例。
        book_serializer = self.get_serializer(book)
        return Response(book_serializer.data)

    """更新单一图书"""
    def update(self, request, pk):
        # 1、获取数据
        book_dict=request.data
        # 2、验证数据库是否有数据
        try:
            # 从查询集获取指定的单一数据对象
            book = self.get_object()
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 3、验证数据
        book_serializer = BookSerializer(book,data=book_dict)
        book_serializer.is_valid()
        # 4、更新数据
        book_serializer.save()
        # 5、返回结果
        return Response(book_serializer.data)

    def destroy(self, request, pk):
        try:
            # 从查询集获取指定的单一数据对象
            book = self.get_object()
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        book.delete()
        return Response({'msg':'删除成功'},status=HTTP_204_NO_CONTENT)