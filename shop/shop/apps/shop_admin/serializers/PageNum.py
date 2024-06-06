#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNum(PageNumberPagination):

    #默认值与 PAGE_SIZE 设置键相同。 如果设置了，则settings.py重写 PAGE_SIZE 。
    # page_size显示<max_page_size
    page_size = 20
    # 指定查询参数的名称，该参数允许客户端根据每个请求设置页面大小。
    # 默认为“无”，表示客户端可能无法控制请求的页面大小。
    page_size_query_param = 'pagesize'
    # 指示所请求的页面大小的最大允许值。只有当 page_size_query_param 也被设置时，此属性才有效。
    max_page_size =20

    # 重写分页返回方法，按照指定的字段进行分页数据返回
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # 总数量
            'lists': data,  # 用户数据
            'page' : self.page.number, # 当前页数
            'pages' : self.page.paginator.num_pages, # 总页数
            'pagesize':self.page_size  # 后端指定的页容量
        })

