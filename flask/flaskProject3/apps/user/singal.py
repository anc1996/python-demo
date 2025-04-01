#!/user/bin/env python3
# -*- coding: utf-8 -*-
from extends import space
from flask import request
login_space=space.signal('登录信号')  # 创建一个信号对象


# 定义信号处理函数
def login_sigal(sender):
	# 获取ip地址
	ip=request.remote_addr
	# 获取请求的url
	url=request.url
	# 获取请求的方法
	method=request.method
	print(f'接收到登录信号，发送者是{sender},ip地址是{ip},请求的url是{url},请求的方法是{method}')
	
# 监听信号
login_space.connect(login_sigal)  # 连接信号和处理函数

