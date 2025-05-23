﻿#!/user/bin/env python3
# -*- coding: utf-8 -*-
#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
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

class PageNumber(PageNumberPagination):
    '''/**/?page=1'''
    
    # 指定每页显示的数据条数
    page_size = 5
    # 指定获取页码的查询参数
    page_size_query_param = 'page_size'
    # 指定每页数据最大条数
    max_page_size = 10

class Books(ModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.filter(is_delete=False)
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    # 还有个全局DjangoFilterBackend在settings
    # 该 OrderingFilter 类支持简单的查询参数控制的结果排序。
    filter_backends = [filters.OrderingFilter, filters.SearchFilter,DjangoFilterBackend]
    # 自定过滤字段
    '''book_drf/OtherFeatures/?name=红楼梦'''
    filterset_fields  = ['name'] # 过滤字段
    search_fields = ['name', 'id'] # 搜索字段
    # 局部视图认证和权限，

    # 认证
        # BasicAuthentication，此身份验证方案使用 HTTP 基本身份验证，根据用户的用户名和密码进行签名。基本身份验证通常仅适用于测试。
        # SessionAuthentication，此认证方案使用Django的默认session后端进行身份验证。Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端。
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    # 权限，局部会覆盖全局的权限
    permission_classes = [AllowAny]  # AllowAny 设置默认为允许不受限制的访问：

    # 局部视图，用户限流。
    throttle_classes = [CustomAnonRateThrottle,CustomUserRateThrottle]

    # 指定分页器
    pagination_class = PageNumber

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要重写
    
    # 重写destroy方法
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
        return instance