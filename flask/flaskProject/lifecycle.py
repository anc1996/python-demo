#!/user/bin/env python3
# -*- coding: utf-8 -*-
from app import app,g


from flask import current_app

# 在每一次请求之前调用，这时候已经有请求了，可能在这个方法里面做请求的校验
# 如果请求的校验不成功，可以直接在此方法中进行响应，直接return之后那么就不会执行视图函数
# current_app:应用上下文对象，它是一个LocalProxy对象，可以获取应用上下文对象中的属性。
@app.before_request
def before_request():
    """
    利用before_request请求钩子，在进入所有视图前先尝试判断用户身份
    :return:
    """
    # TODO 此处利用鉴权机制（如cookie、session、jwt等）鉴别用户身份信息
    # if 已登录用户，用户有身份信息
    g.user_id = 123
    g.user_name = 'itcast'
    # else 未登录用户，用户无身份信息
    # g.user_id = None
    print("before_request")
    # if 请求不符合条件:
    #     return "laowang"


# after_request函数会在视图函数执行后执行，前提是视图函数没有出现异常。它的主要作用是对视图函数的返回值进行处理或者修改
@app.after_request
def after_request(response):
    print("after_request")
    response.headers["Content-Type"] = "application/json"
    return response


# teardown_request函数的参数response是一个响应对象，它包含了服务器返回给客户端的响应内容。

# teardown_request函数必须返回None，否则会抛出一个TypeError异常。
# teardown_request函数则会在视图函数执行后执行，无论视图函数是否出现异常。
# 它的主要作用是进行一些清理工作，例如关闭数据库连接、释放资源等。
@app.teardown_request
def teardown_request(response):
    print("teardown_request")

