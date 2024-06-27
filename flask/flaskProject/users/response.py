#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template,redirect,make_response,request,session

from . import users

@users.route('/hello/')
@users.route('/hello/<name>')
def hello(name=None):
    context={
        'name':name if name is not None else 'hello',
        'age':23
    }
    return render_template('index.html', **context)


@users.route('/baidu')
def baidu():
    # 重定向到百度
    return redirect('http://www.baidu.com')


@users.route('/headers1')
def headers1():

    # 方法一
    '''
    可以返回一个元组，这样的元组必须是 (response, status, headers) 的形式，且至少包含一个元素。
    status 值会覆盖状态代码， headers 可以是一个列表或字典，作为额外的消息标头值。
    :return:
    '''
    # return '状态码为 666', 666
    # return '状态码为 666', 666, [('Itcast', 'Python')]
    return '状态码为 666', 666, {'tutorial': 'Python'}

@users.route('/headers2')
def headers2():
    '''
    方法二
    使用 make_response() 方法构建响应对象
    :return:
    '''

    response = make_response('状态码为 666')
    response.status = '666'
    response.headers['tutorial'] = 'Python'
    return response

@users.route('/set_cookie')
def set_cookie():
    resp = make_response('set cookie')
    # 设置cookie
    resp.set_cookie('username', 'the username', max_age=60*60*24*7)
    return resp

@users.route('/get_cookie')
def get_cookie():
    # 获取cookie
    username = request.cookies.get('username')
    return username

@users.route('/delete_cookie')
def delete_cookie():
    resp = make_response('delete cookie')
    # 删除cookie
    resp.delete_cookie('username')
    return resp

@users.route('/set_session')
def set_session():
    # 设置session,同时需要设置SECRET_KEY，否则会报错
    session['username'] = 'python'
    return 'set session is OK '

@users.route('/get_session')
def get_session():
    # 获取session
    return 'get seesion name:{0}'.format(session.get('username'))

