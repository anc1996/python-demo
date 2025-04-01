#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

logger=logging.getLogger('BasicAPIView')
class Books(APIView):

    """
    APIView是REST framework提供的所有视图的基类，继承自Django的View父类。

    APIView与View的不同之处在于：
        1、被传入到处理方法的请求不会是Django的HttpRequest类的实例，而是REST framework的Request类的实例。
        2、处理方法可以返回REST framework的Response，而不是 Django 的 HttpRequest。
            视图会管理内容协议，给响应设置正确的渲染器。
        3、任何APIException异常都会被捕获，并且传递给合适的响应。
        4、进入的请求将会经过认证，合适的权限和（或）节流检查会在请求被派发到处理方法之前运行。
    支持定义的属性：
        1、authentication_classes 列表或元祖，身份认证类
        2、permissoin_classes 列表或元祖，权限检查类
        3、throttle_classes 列表或元祖，流量控制类
    """

    def get(self,request):
        # 1、查询所有图书对象
        # request.query_params 任何 HTTP 方法类型都可能包含查询参数，而不仅仅是 GET 请求。而这里类似 request.GET 同义词。
        # /book_drf/apibooks?a=233&b=333&c=332123
        print('这个是django view原来的request.data数据返回内容:',request.query_params) #  <QueryDict: {'a': ['233'], 'b': ['333'], 'c': ['332123']}>
        books=BookInfo.objects.filter(is_delete=False)
        bookserializer=BookSerializer(books,many=True)
        # Response(data) ：响应的序列化数据。
        return Response(bookserializer.data)

    """保存图书"""

    def post(self, request):
        # 1、请求体获取数据

        '''例如：post请求：raw ，要json格式，也可以用form-data格式。
        {
            "name":"算法导论",
            "pub_date":"1999-01-13",
            "readcount":"3771",
            "commentcount":"1733"
        }
        '''
        # 这个request.data是APIView的，返回是为响应准备的序列化处理后的数据；
                #  1、 它包括所有解析的内容，包括文件和非文件输入。
                # 2、它支持REST框架的灵活请求解析，而不仅仅是支持表单数据。
                # 3、它支持解析除 POST 之外的 HTTP 方法的内容，这意味着您可以访问 PUT 和 PATCH 请求的内容。
        data_dict=request.data
        # 2、验证数据
        bookserializer=BookSerializer(data=data_dict) # data_dict的字典数据序列化为一个名为BookSerializer的对象
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True) # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)


class BookView(APIView):

    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error(BookInfo.DoesNotExist)
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        book_serializer = BookSerializer(book)
        return Response(book_serializer.data)

    """更新单一图书"""
    def put(self, request, pk):
        # 1、获取数据
        book_dict=request.data
        # 2、验证数据库是否有数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            logger.error(BookInfo.DoesNotExist)
            return Response({'error':'当前数据不存在'},status=HTTP_404_NOT_FOUND)
        # 3、验证数据
        bookserializer = BookSerializer(book,data=book_dict)
        bookserializer.is_valid()
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return Response(bookserializer.data)


    def delete(self,request,pk):
        # 1、查询数据
        try:
            book=BookInfo.objects.get(pk=1)
        except BookInfo.DoesNotExist:
            logger.error(BookInfo.DoesNotExist)
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        book.is_delete=True
        book.save()
        return Response({'msg':'删除成功'},status=HTTP_204_NO_CONTENT)

