#!/user/bin/env python3
# -*- coding: utf-8 -*-
from app import app


# errorhandler 装饰器：注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
@app.errorhandler(400)
def client_error(e):
    return '错误请求',400

@app.errorhandler(ZeroDivisionError)
def internal_server_error(e):
    print(ZeroDivisionError)
    return '除以0异常',500