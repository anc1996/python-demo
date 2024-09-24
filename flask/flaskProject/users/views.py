#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re
from flask import request

from . import users
@users.route('/string/<user_string>')
def get_user_data(user_string):
    # 为string类型
    return 'user_id: {0},type:{1}'.format(user_string,type(user_string))


@users.route('/int/<int:post_id>')
def show_post(post_id):
    # 显示具有给定 ID 的帖子，该 ID 是一个整数
    return f'int: {post_id},type:{type(post_id)}'


@users.route('/path/<path:subpath>')
def show_subpath(subpath):
    # 显示 /path/ 后面的子路径
    return f'Subpath {re.escape(subpath)}'

@users.route('/float/<float:rev>')
def show_float(rev):
    # 显示 /float/ 后面的浮点数
    return f'float: {rev},type:{type(rev)}'

@users.route('/uuid/<uuid:uuid>')
def show_uuid(uuid):
    # 显示 /uuid/ 后面的uuid
    # 例如：/uuid/123e4567-e89b-12d3-a456-426614174000
    return f'uuid: {uuid},type:{type(uuid)}'


@users.route('/articles')
def get_articles():
    # /articles?channel_id=23
    channel_id = request.args.get('channel_id')
    return 'you wanna get articles of channel {}'.format(channel_id)




@users.route('/example', methods=['GET', 'POST'])
def example():

    '''
    postman测试数据
    {
      "data": "This is raw data",
      "form_data": {
        "field1": "value1",
        "field2": "value2"
      },
      "query_params": {
        "key1": "value1",
        "key2": "value2"
      },
      "cookies": {
        "cookie_name": "cookie_value"
      },
      "headers": {
        "Content-Type": "multipart/form-data",
        "Custom-Header": "HeaderValue",
        "User-Agent": "PostmanRuntime/7.26.8",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Postman-Token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "Host": "127.0.0.1:5000",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Length": "length_of_the_data"
      },
      "method": "POST",
      "url": "http://127.0.0.1:5000/example?key1=value1&key2=value2",
      "files": {
        "file": "your_uploaded_file_name"
      }
    }
    :return:
    '''
    # 访问data属性,访问请求数据，并将其转换为字符串。
    data = request.data.decode('utf-8')
    # 访问form属性,访问表单数据，
    form_data = request.form.to_dict()
    # 访问args属性,访问查询参数
    query_params = request.args.to_dict()
    # 访问cookies属性,访问cookies
    cookies = request.cookies.to_dict()
    # 访问headers属性,访问请求头
    headers = dict(request.headers)
    # 访问method属性,访问请求方法
    method = request.method
    # 访问url属性,访问请求URL
    url = request.url
    # 访问files属性,访问上传的文件
    files = request.files.to_dict()
    response = {
        "data": data,
        "form_data": form_data,
        "query_params": query_params,
        "cookies": cookies,
        "headers": headers,
        "method": method,
        "url": url,
        "files": {key: file.filename for key, file in files.items()}  # 获取文件名
    }

    return response


