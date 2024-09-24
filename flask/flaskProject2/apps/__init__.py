#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate

from apps.user.view import user_bp
import os,sys

import settings

from flask import Flask

from extends import db


def create_app():
	# 创建Flask实例
	app = Flask(__name__,template_folder='../templates',static_folder='../static')  # 创建Flask实例
	
	# 方法一：加载配置文件
	# settings=os.path.join(os.path.dirname(__file__),'settings_file.py')
	# 方法二：
	# import settings_file
	# 读取配置信息,silent 参数设置为 True，如果没有找到配置文件，则不会报错
	# app.config.from_pyfile(settings_file, silent=True)
	
	app.config.from_object(settings.DevelopmentConfig)
	db.init_app(app)  # 初始化SQLAlchemy对象
	
	migrate = Migrate(app=app, db=db)
	# 注册蓝图对象
	app.register_blueprint(user_bp)
	# 打印所有的路由信息
	for rule in app.url_map.iter_rules():
		print(f'endpoint:{rule.endpoint},url:{rule.rule}')
		
	return app
