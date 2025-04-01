#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint,abort,signals
from extends import first_signal
error_bp = Blueprint('error', __name__,url_prefix='/error')

# 演示错误
@error_bp.route('/404')
def error_404():
    abort(404)
    return '404 返回成功'

# 这在 app 和 blueprint 对象上都可用。在应用程序上使用时，它可以处理每个请求中的错误。
# 在 Blueprint 上使用时，这可以处理 Blueprint 处理的请求中的错误。
# 要注册蓝图并影响每个请求，请使用 Blueprint.app_errorhandler（）。
@error_bp.errorhandler(404)
def page_not_found(error):
	return '404 not 报错', 404

@error_bp.route('/500')
def error_500():
	abort(500)
	return '500 返回成功'

@error_bp.errorhandler(500)
def internal_server_error(error):
	return f'500 内部服务器错误:{error}', 500

@error_bp.route('/blinker')
def error_blinker():
	# 发送信号
	first_signal.send('blinker')
	return '发送信号成功'

# got_request_exception：在请求过程中抛出异常时发送信号，异常本身会通过exception传递到订阅（监听）的函数中。
# 一般可以监听这个信号，来记录网站异常信息。


@error_bp.route('/zero_division')
def error_zero_division():
	1/0
	return '0 除法错误'

def get_error(sender, exception):
	print(f'捕获到异常：{exception}')

# 订阅信号，监听异常
signals.got_request_exception.connect(get_error)