import json
import logging
from django.http.multipartparser import MultiPartParser
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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
          第1种：在body的form-data传输数据
          
          第2种：在body的raw传输数据,用json传输
            {
                "name":"php入门",
                "pub_date":"2022-12-23",
                "readcount":"3222",
                "commentcount":"1233"
            }
        '''
        if request.POST.get('name') is not None:
            post=request.POST # 这种：form-data
        else:
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
            # 使用 name 字段作为查找条件
            book, created = BookInfo.objects.update_or_create(
                name=name,  # 根据 name 字段查找记录
                defaults={
                    'pub_date': pub_date,
                    'readcount': readcount,
                    'commentcount': commentcount
                }
            )
        except IntegrityError as e:
            logger.error(f"数据库唯一性约束错误: {e}")
            return JsonResponse({'error': '书籍名称已存在，无法创建'}, status=HTTP_409_CONFLICT)
        except Exception as e:
            logger.error(f"保存书籍时发生错误: {e}")
            return JsonResponse({'error': '服务器错误'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 4.返回结果
        
        context={
                    'id':book.id,
                    'name':book.name,
                    'pub_date':book.pub_date,
                    'readcount':book.readcount,
                    'commentcount':book.commentcount,
                    'created':'已创建' if created else '已更新'
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
        
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        
        try:
            if request.content_type.startswith('multipart/form-data'):
                # 处理 form-data 数据
                # 使用 MultiPartParser 手动解析
                parser = MultiPartParser(request.META, request, request.upload_handlers)
                data, files = parser.parse()
                # 将 QueryDict 转换为普通字典
                data = data.dict()
            elif request.content_type == 'application/json':
                # 处理 JSON 数据
                data = json.loads(request.body.decode())
            else:
                return JsonResponse({'error': '不支持的内容类型'}, status=HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=HTTP_400_BAD_REQUEST)
        
        # 3. 更新书籍字段
        update_fields = ['name', 'pub_date', 'readcount', 'commentcount']
        for field in update_fields:
            if field in data:
                setattr(book, field, data[field]) # setattr() 函数对应函数 getattr()，用于设置属性值，该属性不一定是存在的。
        
        try:
            # 4. 保存更新
            book.save()
        except ValidationError as e:
            logger.error(f"数据验证失败: {e}")
            return JsonResponse({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"保存书籍时发生错误: {e}")
            return JsonResponse({'error': '服务器错误'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 5. 返回更新后的书籍信息
        context = {
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount,
            'commentcount': book.commentcount,
        }
        return JsonResponse(context,status=HTTP_200_OK)


    """删除单一图书"""
    def delete(self,reuqest,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=HTTP_400_BAD_REQUEST)
        
        if book.is_delete:
            return JsonResponse({'error': '书籍已删除'}, status=HTTP_400_BAD_REQUEST)
        book.is_delete=True
        book.save()
        return JsonResponse({'error': '删除成功'}, status=HTTP_200_OK)