#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re

from flask_restful import Resource,inputs
from flask_restful.reqparse import RequestParser


def mobile(mobile_str):
    """
    检验手机号格式
        :param mobile_str: str 被检验字符串
        :return: mobile_str
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError('{} is not a valid mobile'.format(mobile_str))

class RequestParserResource(Resource):

    def get(self):
        # /users/request?name=hello&age=18&phone=13355554444&phone=13355554445&email=173@qq.com
        # 1、创建一个RequestParser对象,用来帮助我们检验和转换请求数据。
        parser = RequestParser()
        # 2、添加需要验证的参数。这个方法需要三个参数：参数的名称，传递参数的方式，以及验证参数的函数或类型
        '''
        add_argument(args, type=None, required=False, help=None, default=None, location=None, store_missing=True, trim=False, nullable=True, ignore=False,)
            args: 从请求中提取参数
            type: 参数的类型
            help: 参数检验错误时返回的错误描述信息
            required: 是否必须提供参数，默认为True,若异常，则返回400。
            action: 参数的动作。
                  append：表示将参数的值添加到一个列表中
                  store：表示保留第一个,默认值
        '''
        parser.add_argument('name', type=str, help='name error', required=True)
        parser.add_argument('age', type=inputs.int_range(0,200), help='age error', required=False)
        parser.add_argument('email', type=inputs.regex(r'^[a-zA-Z0-9_]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
                            help='email error', required=False, action='append')
        parser.add_argument('phone', type=mobile, help='phone error', required=False, action='append')
        # 3、开始数据验证。如果验证通过，这个方法将返回一个包含验证后数据的字典；如果验证不通过，这个方法将抛出一个异常
        request_dict=parser.parse_args()
        # 4、获取验证后的数据
        name=request_dict.get('name')
        age=request_dict.get('age', None)
        phone=request_dict['phone']     # list
        email=request_dict['email']
        context={'name':name,'age':age,'phone':phone,'email':email}
        return context

    def post(self):
        #  1、创建一个RequestParser对象
        parser = RequestParser()

        # 2、添加需要验证的参数。这个方法需要三个参数：参数的名称，传递参数的方式，以及验证参数的函数或类型
        # location: 从哪个位置获取参数
        #仅在 POST 正文中查看
        # parser.add_argument('name', type=int, location='form', help='name not in form', required=False)
        # 仅在查询字符串中查找
        parser.add_argument('PageSize', type=int, location='args',help='PageSize not in args', required=False)
        # 从请求标头
        parser.add_argument('User-Agent', location='headers', help='User-Agent not in headers', required=False)
        # # From http cookies
        parser.add_argument('session_id', location='cookies', help='session_id not in cookies', required=False)
        # From json
        parser.add_argument('user_id', location='json', help='user_id not in json', required=False)
        # From file uploads
        # parser.add_argument('picture', location='files')
        # 也可指明多个位置
        parser.add_argument('session_string', type=str, location=['cookies','headers'],help='name error', required=False)

        # 3、开始数据验证。如果验证通过，这个方法将返回一个包含验证后数据的字典；如果验证不通过，这个方法将抛出一个异常
        request_dict=parser.parse_args()

        # 4、获取验证后的数据
        name=request_dict.get('name')
        PageSize=request_dict.get('PageSize')
        User_Agent=request_dict.get('User-Agent')
        session_id=request_dict.get('session_id')
        user_id=request_dict.get('user_id')
        # picture=request_dict.get('picture')

        context={'name':name,'PageSize':PageSize,'User-Agent':User_Agent,'session_id':session_id,'user_id':user_id}
        return {'post':context}


