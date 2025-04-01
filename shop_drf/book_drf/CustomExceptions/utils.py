#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.db import DatabaseError
from rest_framework.exceptions import (
    APIException,
    ParseError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    Throttled,
    ValidationError,
)


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
    
    # 如果 response 不是 None，则对其进行修改
    if response is not None:
        custom_error_messages = {
            ParseError: "请求正文格式错误或不可读.",
            AuthenticationFailed: "无法对用户进行身份验证。",
            NotAuthenticated: "未提供身份验证凭证。",
            PermissionDenied: "您没有执行此操作的权限。",
            NotFound: "未找到请求的资源.",
            MethodNotAllowed: "此终端节点不允许使用使用的 HTTP 方法。",
            NotAcceptable: "请求的内容类型不可接受。",
            Throttled: "您发出的请求太多。请稍后重试。",
            ValidationError: "您的请求存在验证错误。",
            DatabaseError: "数据库内部错误",
        }
        # 根据异常类型获取自定义消息
        exception_type = type(exc)
        custom_message = custom_error_messages.get(exception_type, str(exc))
        
        # 在此处补充自定义的异常处理
        response.data = {
            "status_code": response.status_code,
            "error": custom_message,
            "details": response.data,
        }
    
    return response