#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from book_drf.Over_Basicclass.serializer import BookSerializer
from books.models import BookInfo

class CustomAnonRateThrottle(AnonRateThrottle):
    rate = '10/day'  # 未认证用户每天限流 10 次

class CustomUserRateThrottle(UserRateThrottle):
    rate = '100/day'  # 认证用户每天限流 100 次



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

    # 局部视图认证和权限，

    # 认证
        # BasicAuthentication，此身份验证方案使用 HTTP 基本身份验证，根据用户的用户名和密码进行签名。基本身份验证通常仅适用于测试。
        # SessionAuthentication，此认证方案使用Django的默认session后端进行身份验证。Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端。
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    # 权限，局部会覆盖全局的权限
    permission_classes = [AllowAny]  # AllowAny 设置默认为允许不受限制的访问：

    # 局部视图，用户限流。
    throttle_classes = [CustomAnonRateThrottle,CustomUserRateThrottle]

    # 自定过滤字段
    '''book_drf/OtherFeatures/?name=红楼梦'''
    filterset_fields  = ['name', 'readcount']

    # 还有个全局DjangoFilterBackend在settings
    # 该 OrderingFilter 类支持简单的查询参数控制的结果排序。
    filter_backends = [filters.OrderingFilter]

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要重写


class BookView(ModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 局部视图认证和权限，

    # 认证
        # BasicAuthentication，此身份验证方案使用 HTTP 基本身份验证，根据用户的用户名和密码进行签名。基本身份验证通常仅适用于测试。
        # SessionAuthentication，此认证方案使用Django的默认session后端进行身份验证。Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端。
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    # 权限，局部会覆盖全局的权限
    permission_classes = [AllowAny]  # AllowAny 设置默认为允许不受限制的访问：

    # 方法二：throttle_scope 属性时，才会应用此限流器。
    throttle_scope = 'bookview'

    # 自定过滤字段，该 SearchFilter 类支持基于简单单查询参数的搜索，并且基于 Django 管理员的搜索功能。
    # 该 OrderingFilter 类支持简单的查询参数控制的结果排序。
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]

    # 指定搜索的字段
    '''http://**/?search=三国演义&ordering=-name'''
    search_fields = ['name', 'commentcount']
    ordering_fields = ['name', 'readcount','readcount']
    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要重写


