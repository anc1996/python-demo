#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.filters import BookInfoFilter
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
    # 3、要指定当前视图使用的过滤器
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Corrected filter_backends
    filterset_class = BookInfoFilter
    ordering_fields = ['readcount', 'commentcount', 'pub_date']  # Added ordering_fields
    
    # 认证
        # BasicAuthentication，此身份验证方案使用 HTTP 基本身份验证，根据用户的用户名和密码进行签名。基本身份验证通常仅适用于测试。
        # SessionAuthentication，此认证方案使用Django的默认session后端进行身份验证。Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端。
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    # 权限，局部会覆盖全局的权限
    permission_classes = [AllowAny]  # AllowAny 设置默认为允许不受限制的访问：

    """局部视图认证和权限，全当访问 MyView 这个视图时，会优先使用这里的认证和权限设置，而不是全局设置。"""
    
    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法
    
    # 重写destroy方法,逻辑删除
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
        return instance
