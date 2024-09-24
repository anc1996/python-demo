#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import fields,marshal_with,marshal,Resource


class User(object):
    # 用来模拟User模型类要返回的数据对象
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

# 用来声明序列化处理的字段，用来帮助我们将数据序列化为特定格式的字典数据，以便作为视图的返回值。
resoure_fields = {
        'user_id': fields.Integer,
        'name': fields.String,
        'age': fields.Integer
    }

'''
    marshal_with与marshal的区别：
        marshal_with是一个装饰器，用来将返回的数据序列化成json格式
        marshal是一个函数，用来将数据序列化成json格式
'''

class ResponseResource1(Resource):

    # marshal_with(fields=resoure_fields,envelope='data')是一个装饰器，用来将返回的数据序列化成json格式
        # envelope='data'表示将返回的数据对象包装在data中
    @marshal_with(resoure_fields)
    def get(self):
        # 1、创建一个User对象
        user = User(user_id=1, name='ResponseResource1', age=18)
        return user
        # 最终将user模型类返回的数据对象序列化成json格式


class ResponseResource2(Resource):
    def get(self):
        # 1、创建一个User对象
        user = User(user_id=2, name='ResponseResource2', age=19)
        # 2、序列化成json格式
        result = marshal(user, resoure_fields)
        return result
        # 最终将user模型类返回的数据对象序列化成json格式