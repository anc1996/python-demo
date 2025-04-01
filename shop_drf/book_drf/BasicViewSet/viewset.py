#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from rest_framework.status import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

logger=logging.getLogger('BasicViewSet')

"""
使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：并且要在路由设置方法对应的操作。
    list() 提供一组数据 get
    retrieve() 提供单个数据 get
    create() 创建数据 post
    update() 保存数据 put
    destory() 删除数据 delete
ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。
ViewSet 继承自 APIView。你可以使用任何标准属性，如 permission_classes, authentication_classes 以便控制视图集上的 API 策略。，
提供了身份认证、权限校验、流量管理等。
在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。
"""


class Books(ViewSet):

    """获取所有图书"""
    def list(self, request):
        """# 自定义方法名，代替get方法,在urls路由匹配对应方法名"""
        # 1、查询所有图书对象
        print('这个是django view类原来request.data数据返回的内容:',request.query_params)
        books = BookInfo.objects.filter(is_delete=False)
        bookSerializer = BookSerializer(books, many=True)
        return Response(bookSerializer.data)

    """保存图书"""
    def create(self, request):
        """自定义方法名，代替post方法,在urls路由匹配对应方法名"""
        # 1、请求体获取数据
        data_dict = request.data
        # 2、验证数据，将字典转成模型对象
        bookserializer = BookSerializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True)
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)

    """获取单一图书"""
    def retrieve(self, request, pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        bookserializer = BookSerializer(book)
        return Response(bookserializer.data)

    """更新单一图书"""
    def update(self, request, pk):
        # 1、获取数据
        book_dict = request.data
        # 2、验证数据库是否有数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 3、验证数据
        bookserializer = BookSerializer(book, data=book_dict)
        bookserializer.is_valid(raise_exception=True)
        # 4、更新数据
        bookserializer.save()
        # 5、返回结果
        return Response(bookserializer.data)

    """删除单一数据"""
    def destroy(self,request,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error('当前数据不存在')
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        book.is_delete = True
        book.save()
        return Response({'msg':'删除成功'},status=HTTP_204_NO_CONTENT)