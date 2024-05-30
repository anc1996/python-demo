#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

"""
五个扩展类（配合GenericAPIview使用继承object）,他们需要结合GenericAPIView使用
    CreateModelMixin：保存数据
    ListModelMixin：获取多个数据对象
    UpdateModelMixin：更新数据
    DestroyModelMixin：删除数据
    RetrieveModelMixin：获取单一数据
"""

logger=logging.getLogger('GenericAPI_Mixin')
class Books(GenericAPIView,CreateModelMixin,ListModelMixin):

    """
    GenericAPIView扩展了REST框架的 APIView 类，为标准list和detail view 添加了通常需要的行为。
    支持定义的属性：
    列表视图与详情视图通用：
        queryset 用于从视图返回对象的查询结果集。通常，你必须设置此属性或者重写 get_queryset() 方法
        serializer_class 用于验证和反序列化输入以及用于序列化输出的Serializer类。 通常，你必须设置此属性或者重写get_serializer_class() 方法。
    列表视图使用：
        pagination_class 当分页列出结果时应使用的分页类。。默认值与 DEFAULT_PAGINATION_CLASS 设置的值相同
        filter_backends 用于过滤查询集的过滤器后端类的列表。默认值与DEFAULT_FILTER_BACKENDS 设置的值相同。
    详情页视图使用：
        lookup_field - 用于执行各个model实例的对象查找的model字段。默认为 'pk'。 请注意，在使用超链接API时，如果需要使用自定义的值，你需要确保在API视图和序列化类都设置查找字段。
        lookup_url_kwarg - 应用于对象查找的URL关键字参数。它的 URL conf 应该包括一个与这个值相对应的关键字参数。如果取消设置，默认情况下使用与 lookup_field相同的值。
    """
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    def get(self,request):
        """/book_drf/modelmixinview/"""
        # 由于ListModelMixin提供一个 .list(request, *args, **kwargs) 方法，该方法实现列出查询集。
        return self.list(request)

    """新增保存图书"""
    def post(self, request):
        """/book_drf/modelmixinview/,请求体如下：raw 格式json,或者form-data
        {
            "name":"鼠标",
            "pub_date":"2019-11-16",
            "readcount":"3271",
            "commentcount":"733"
        }
        """
        # 提供一种 .create(request, *args, **kwargs) 方法，用于实现创建和保存新的模型实例。
        return self.create(request)


class BookView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer


    """查询单一数据"""
    def get(self,request,pk):
        # RetrieveModelMixin提供一种 .retrieve(request, *args, **kwargs) 方法，用于实现在响应中返回现有模型实例。
        return self.retrieve(request,pk)

    """更新单一图书"""
    def put(self, request, pk):
        """
        {
            "name":"天然",
            "pub_date":"2019-11-16",
            "readcount":"3271",
            "commentcount":"733"
        }
        """
        # UpdateModelMixin提供一种 .update(request, *args, **kwargs) 方法，用于实现更新和保存现有模型实例。
        return self.update(request,pk)


    def delete(self,request,pk):
        # DestroyModelMixin提供 .destroy(request, *args, **kwargs) 一种方法，用于实现对现有模型实例的删除。
        return self.destroy(request,pk)