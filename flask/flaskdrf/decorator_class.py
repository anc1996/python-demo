#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource
def decorator1(func):
    def inner(*args, **kwargs):
        print('running decorator1')
        return func(*args, **kwargs)
    return inner

def decorator2(func):
    def inner(*args, **kwargs):
        print('running decorator2')
        return func(*args, **kwargs)
    return inner


class DemoResource1(Resource):

    method_decorators = [decorator1,decorator2]

    def get(self):
        return {'msg': 'DemoResource get view'}

    def post(self):
        return {'msg': 'DemoResource post view'}



class DemoResource2(Resource):
    method_decorators = {
        # 要按顺序写装饰器
        'get':[decorator1, decorator2],
        'post':[decorator1]
    }
    '''
        类似
        @decorator2
        @decorator1
        def get(self):
           。。。。。
       decorator2(decorator1(get))->inner
    '''

    def get(self):
        return {'msg': 'DemoResource2 get view'}

    def post(self):
        return {'msg': 'DemoResource2 post view'}

    def put(self):
        return {'msg': 'DemoResource2 put view'}