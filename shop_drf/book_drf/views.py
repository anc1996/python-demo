#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.status import HTTP_400_BAD_REQUEST

# Create your views here.
from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.
class Books(View):

    """查询所有图书"""
    def get(self,request):
        # 1、查询所有图书对象
        books=BookInfo.objects.all().filter(is_delete=False)
        # 2、序列化：将数据结构或对象状态转换为一个可以存储或传输的格式的过程
        books_Serializer=BookSerializer(books,many=True)
        # 3、
        return JsonResponse(books_Serializer.data, safe=False)

    """保存图书"""

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
            # 前端json请求
            data=request.body.decode()
            data_dict=json.loads(data)
        # 2、验证数据
        bookserializer=BookSerializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True) # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return JsonResponse(bookserializer.data)

class Book(View):

    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book=BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_400_BAD_REQUEST)
        # 返回一个对象不需要manny=True
        book_Serializer = BookSerializer(book)
        return JsonResponse(book_Serializer.data)