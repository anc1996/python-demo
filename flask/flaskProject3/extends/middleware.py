#!/user/bin/env python3
# -*- coding: utf-8 -*-

class LoggingMiddleware:
    """
    一个简单的日志中间件，用于记录请求的 URL。
    """

    def __init__(self, app):
        self.app = app  # 被包装的 WSGI 应用

    def __call__(self, environ, start_response):
        # 请求处理前
        # environ 是一个包含 CGI 环境变量的字典, start_response 是一个接受状态码和响应头的函数
        # __call__ 方法是 WSGI 应用的入口点
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')
        print(f"[Middleware] {method} request to {path}")

        # 调用被包装的 WSGI 应用
        return self.app(environ, start_response)