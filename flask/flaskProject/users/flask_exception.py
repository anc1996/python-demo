#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import request

from werkzeug.exceptions import abort

from . import users

@users.route('/channel')
def get_channel():
    channel_id=request.args.get('channel_id')
    if channel_id is None:
        # abort: 用于处理错误，接受一个 HTTP 状态码或一个 Response 对象
        abort(400)
    return '获取文章列表:{0}'.format(channel_id)


@users.route('/chuyi')
def chuyi():
    1/0
    return '除以0'
