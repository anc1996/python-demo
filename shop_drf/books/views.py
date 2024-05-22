import json
import logging

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.exceptions import ValidationError
from rest_framework.status import *

from books.models import BookInfo

# Create your views here.
logger=logging.getLogger('books')


class BooksView(View):
    """查询所有图书"""

    '''
    192.168.20.2:8000/books/BooksView/
    '''
    def get(self,request):
        books=BookInfo.objects.all()
        book_list=[]
        # 返回图书，
        for book in books:
            if not book.is_delete:
                book_list.append({
                    'id':book.id,
                    'name':book.name,
                    'pub_date':book.pub_date,
                    'readcount':book.readcount,
                    'commentcount':book.commentcount,
                })
        # 当 safe 设置为 True 时，Django 会检查返回的数据是否是一个字典类型的数据（即 dict 对象）。
            # 如果不是字典类型的数据，Django 会抛出一个 TypeError 异常。
        # 当 safe 设置为 False 时，Django 不会对返回的数据进行安全性检查，可以直接将数据转换为 JSON 格式并返回给客户端。
        return JsonResponse(book_list,safe=False)

    """保存图书"""
    def post(self,request):
        # 1.请求体获取数据
        '''
          第2种：在body的form-data传输数据
        '''
        # post=request.POST
        '''
            第2种：在body的raw传输数据,用json传输
            {
                "name":"php入门",
                "pub_date":"2022-12-23",
                "readcount":"3222",
                "commentcount":"1233"
            }
        '''
        post=json.loads(request.body.decode())
        name=post.get('name')
        pub_date=post.get('pub_date')
        readcount=post.get('readcount')
        commentcount=post.get('commentcount')
        # 2.验证数据
        if not(all([name,pub_date])):
            return JsonResponse({'error':'如果缺少必传参数，响应错误信息，403'},status=HTTP_403_FORBIDDEN)
        # 3.保存数据
        try:
            book=BookInfo.objects.update_or_create(name=name,pub_date=pub_date,readcount=readcount,commentcount=commentcount)
        except ValidationError as e:
            logger.error(e)
            return JsonResponse({'error': str(e)}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'error': '服务器错误'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        # 4.返回结果
        context={
                    'id':book.id,
                    'name':book.name,
                    'pub_date':book.pub_date,
                    'readcount':book.readcount,
                    'commentcount':book.commentcount,
                }
        return JsonResponse(context)


class BookView(View):

    '''
    192.168.20.2:8000/books/BookView/
    '''

    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book=BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_400_BAD_REQUEST)
        context = {
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount,
            'commentcount': book.commentcount,
        }
        return JsonResponse(context)

    """更新单一图书"""
    def put(self,request,pk):

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)
        if not (all([book_dict.get('name'), book_dict.get('pub_date')])):
            return JsonResponse({'error': '如果缺少必传参数，响应错误信息，403'}, status=HTTP_400_BAD_REQUEST)
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist as e:
            logger.error(e)
            return HttpResponse(status=HTTP_404_NOT_FOUND)
        book.name=book_dict.get('name')
        book.readcount=book_dict.get('readcount')
        book.commentcount=book_dict.get('commentcount')
        book.pub_date =book_dict.get('pub_date')
        try:
            book.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'error': '服务器错误'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        context = {
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount,
            'commentcount': book.commentcount,
        }
        return JsonResponse(context)


    """删除单一图书"""
    def delete(self,reuqest,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '如果缺少必传参数，响应错误信息，404'}, status=HTTP_404_NOT_FOUND)
        if book.is_delete:
            return JsonResponse({'error': '书籍已删除'}, status=HTTP_400_BAD_REQUEST)
        book.is_delete=True
        book.save()
        return JsonResponse({})