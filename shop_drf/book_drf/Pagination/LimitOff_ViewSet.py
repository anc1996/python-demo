#!/user/bin/env python3
# -*- coding: utf-8 -*-
#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.pagination import LimitOffsetPagination
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

class LimitOff(LimitOffsetPagination):
    '''
        这种分页样式反映了查找多个数据库记录时使用的语法。客户端包括“limit”和“offset”查询参数。
            limit指示在数据库要返回的项目的最大数目，这相当于其他样式中的 page_size。
            offset指示在数据库查询相对于完整的未分页项的起始位置。
        例如：/**/?limit=100&offset=500
            limit=100：指定每页返回 100 条记录。
            offset=500：跳过前 500 条记录，从第 501 条记录开始返回。
    '''
    # default_limit：指示在客户端未在查询参数中提供限制时使用的限制。默认为与 PAGE_SIZE 设置键相同的值。
    default_limit = 4

    # limit_query_param,指示“limit”查询参数的名称。默认为 'limit'。
    limit_query_param='limit'
    # offset_query_param 指示“offset”查询参数的名称。默认为 'offset'。
    offset_query_param='offset'
    # max_limit：指示所请求的页面大小的最大允许值。
    max_limit= 8

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


    # 指定分页器
    pagination_class = LimitOff

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要重写
