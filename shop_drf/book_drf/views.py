#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from django.http import JsonResponse
from django.views import View
from rest_framework.status import *

# Create your views here.
from books.models import BookInfo
from book_drf.Over_Basicclass.serializer import BookSerializer, BookModelSerializer

# Create your views here.
logger = logging.getLogger('book_drf')
class Books(View):

    """查询所有图书"""
    def get(self,request):
        # 1、查询所有图书对象
        books=BookInfo.objects.all().filter(is_delete=False)
        # 2、序列化：将数据结构或对象状态转换为一个可以存储或传输的格式的过程
        books_Serializer=BookSerializer(books,many=True)
        # 3、
        return JsonResponse(books_Serializer.data, safe=False)

    """新增图书保存"""
    def post(self, request):
        # 请求体获取数据
        # 验证数据
        # x-www-form-urlencoded;charset=UTF-8
        if request.POST.get('name') is not None:
            name = request.POST.get('name')
            pub_date = request.POST.get('pub_date')
            readcount = request.POST.get('readcount')
            commentcount = request.POST.get('commentcount')
            data_dict={'name':name,'pub_date':pub_date,'readcount':readcount,'commentcount':commentcount}
        else:
            # raw中前端，json请求
            data=request.body.decode()
            data_dict=json.loads(data)
        # 2、验证数据，如果存在则更新，不存在则创建
        book = BookInfo.objects.filter(name=data_dict.get('name')).first()
        if book:
            book_serializer=BookSerializer(book,data=data_dict)
        else:
            book_serializer=BookSerializer(data=data_dict)
        # 验证方法，返回True表示验证通过，False表示验证失败,
             #  根据raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        if not book_serializer.is_valid():
            return JsonResponse({"查看验证错误信息：":book_serializer.data})
        else:
            # 4、保存数据
            book_serializer.save()
            return JsonResponse(book_serializer.data)

class Book(View):

    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book=BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 返回一个对象不需要manny=True
        book_Serializer = BookSerializer(book)
        return JsonResponse(book_Serializer.data)

    """更新单一图书"""
    def put(self,request,pk):

        # 1、获取请求体数据
        data_dict=json.loads(request.body.decode())
        # 2、查询数据对象
        try:
            book = BookInfo.objects.get(id=int(pk))
        except ValueError:
            return JsonResponse({'error': 'Invalid pk'}, status=HTTP_400_BAD_REQUEST)
        except BookInfo.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 3、验证数据，要传递book这个值
        book_serializer=BookSerializer(book,data=data_dict)
        if not book_serializer.is_valid():
            return JsonResponse({"查看验证错误信息：":book_serializer.data})
        else:
            # 4、保存数据
            book_serializer.save()
            return JsonResponse(book_serializer.data)
    
    def delete(self,request,pk):
        # 1、查询数据对象
        try:
            book=BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 2、删除数据
        book.is_delete=True
        book.save()
        return JsonResponse({'msg': '删除成功'}, status=HTTP_204_NO_CONTENT)


class BookmodelView(View):
    def get(self, request):
        # 获取所有图书
        books = BookInfo.objects.all()
        # 使用 BookModelSerializer 对图书进行序列化
        books_serializer = BookModelSerializer(books, many=True)
        # 返回序列化后的图书数据
        return JsonResponse(books_serializer.data, safe=False)

    def post(self, request):
        # 使用 BookModelSerializer 对请求体中的数据进行反序列化
        serializer = BookModelSerializer(data=json.loads(request.body.decode()))
        # 如果数据有效，保存图书并返回响应
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=HTTP_201_CREATED)
        # 如果数据无效，返回错误响应
        else:
            return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)