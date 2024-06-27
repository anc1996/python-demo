#!/user/bin/env python3
# -*- coding: utf-8 -*-
from app import app

@app.errorhandler(400)
def client_error(e):
    return '错误请求',400

@app.errorhandler(ZeroDivisionError)
def internal_server_error(e):
    print(ZeroDivisionError)
    return '除以0异常',500