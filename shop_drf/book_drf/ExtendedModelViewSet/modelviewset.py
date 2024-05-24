#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework.viewsets import ModelViewSet

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

"""
使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
    list() 提供一组数据
    retrieve() 提供单个数据
    create() 创建数据
    update() 保存数据
    destory() 删除数据
ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。

3）ModelViewSet
继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin、
    CreateModelMixin、UpdateModelMixin、DestoryModelMixin。
"""

class Books(ModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要重写