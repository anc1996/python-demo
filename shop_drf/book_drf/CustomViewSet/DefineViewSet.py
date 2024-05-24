#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import *
from book_drf.Over_Basicclass.serializer import BookSerializer, BookModelSerializer
from books.models import BookInfo

"""
以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。
action装饰器可以接收两个参数：
    methods: 该action支持的请求方式，列表传递
    detail: 表示是action中要处理的是否是视图资源的对象（即是否通过url路径获取主键）
            True 表示使用通过URL获取的主键对应的数据对象
            False 表示不使用URL获取主键
"""

class Books(GenericViewSet):
    """获取所有图书"""
    """获取所有图书"""
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)

    #  2、要指定当前视图使用的序列化器，通过重写父类的gget_serializer_class方法返回应该用于序列化器的类。
    # 才能使父类执行get_serializer函数这个serializer_class = self.get_serializer_class()内部定义的赋值
    def get_serializer_class(self):
        if self.action=='searchall':
            return BookSerializer
        else:
            return BookModelSerializer

    # 自定义方法名，代替get方法,在urls路由匹配对应方法名
    @action(methods=['get'],detail=False)
    # detail 参数指定该动作是否需要指定主键（primary key）参数。
    def searchall(self, request):
        print('serchall函数方法名：', self.action)  # action属性提取的是方法名,这里显示是searchall
        # 1、查询所有图书对象
        # 返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回queryset属性，可以重写
        books = self.get_queryset()
        # 2、返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。
        # 使用指定序列化器，获取序列化对象
        bookserializer = self.get_serializer(books, many=True) # 调用get_serializer_class的函数
        return Response(bookserializer.data)

    """创建新的图书"""
    @action(methods=['post'],detail=False)
    def createone(self, request):
        # 请求体获取数据
        data_dict = request.data
        # 2、验证数据
        bookserializer = self.get_serializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True)  # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)

    # 获取单一图书
    @action(methods=['get'], detail=True)
    def getone(self, request, pk):
        try:
            # get_object(self) 返回详情视图所需的模型类数据对象，
            # 默认使用lookup_field参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        bookserializer = self.get_serializer(book)
        return Response(bookserializer.data)

    """更新单一图书"""
    @action(methods=['put'], detail=True)
    def refresh(self, request, pk):
        # 1、获取数据
        book_dict = request.data
        # 2、验证数据库是否有数据
        try:
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=HTTP_404_NOT_FOUND)
        # 3、验证数据
        bookserializer =self.get_serializer(book, data=request.data)
        bookserializer.is_valid(raise_exception=True)
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return Response(bookserializer.data)

    # 删除数据
    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        try:
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '数据库已存在'}, status=HTTP_404_NOT_FOUND)
        book.delete()
        return Response({'ok': '删除成功'}, status=200)