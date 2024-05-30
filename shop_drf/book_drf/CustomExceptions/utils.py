#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.db import DatabaseError

def exception_handler(exc, context):
    # 返回应用于任何给定异常的响应。如果没有提供自定义处理程序，则使用默认处理程序。
    response = drf_exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is not None:
        response.data['status_code'] = response.status_code

    return response