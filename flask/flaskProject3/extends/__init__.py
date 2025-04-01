#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from blinker import Namespace

db=SQLAlchemy()  # 实例化SQLAlchemy对象
space=Namespace()  # 实例化blinker,

# 1. 创建信号
# 用于在应用中发送信号，以便在应用的不同部分之间进行通信
first_signal=space.signal('发送一个信号')  # 创建一个信号对象

# 2，定义信号处理函数
def handle_signal(sender):
	print(f'接收到信号，发送者是{sender}')
# 3. 连接信号和处理函数
first_signal.connect(handle_signal)  # 连接信号和处理函数

# # 4. 发送信号，这里用于app通信
# first_signal.send('发送者')  # 发送信号