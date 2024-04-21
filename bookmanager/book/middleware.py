#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse

'''
中间件的作用: 每次请求和相应的时候都会调用
中间件的使用: 我们可以判断每次请求中是否携带了cookie中某些信息
可以自己编写中间件，范例
def simple_middleware(get_response):
    # 一次性配置和初始化。
    def middleware(request):
        # 对于每个请求在视图（以及后续中间件）被调用之前执行的代码。
        response = get_response(request)
        # 对于每个请求/响应在视图被调用之后执行的代码。
        return response
    return middleware
'''

def simple_middleware1(get_response):
    # 一次性配置和初始化。
    print('这里是中间件1第一次配置、加载和初始化的地方')
    def middleware(request):
        # 对于每个请求在视图（以及后续中间件）被调用之前执行的代码。
        username = request.COOKIES.get('username')
        if username is None:
            print('username is None')
            # return HttpResponse('哥们,你没有登陆哎')
        print('这里是 simple_middleware请求前,上面执行代码')
        response = get_response(request)
        print('这里就 simple_middleware响应后/请求后')
        # 对于每个请求/响应在视图被调用之后执行的代码。
        return response
    return middleware

def simple_middleware2(get_response):
    print('这里是中间件2第一次配置、加载和初始化的地方')
    def middleware(request):
        print('before request simple_middleware2')
        response=get_response(request)
        print('after request/response simple_middleware2')
        return response
    return middleware