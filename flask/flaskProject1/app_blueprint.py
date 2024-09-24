#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask

import settings


def create_app():
	app = Flask(__name__) # 创建Flask实例
	app.config.from_object(settings) # 从settings.py中加载配置信息