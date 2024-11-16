#!/basic/bin/env python3
# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_migrate import Migrate
import redis
from logging.config import dictConfig
import settings

from apps.basic.view import basic_bp
from extends import db, cache, api, session, cors, init_serializer, jwt


def create_app():
	# 创建Flask实例
	
	app = Flask(__name__, template_folder='../templates', static_folder='../static')  # 创建Flask实例
	
	app.config.from_object(settings.DevelopmentConfig)
	db.init_app(app=app)  # 初始化SQLAlchemy对象
	cache.init_app(app=app)  # 初始化flask-caching缓存对象
	api.init_app(app=app)  # 初始化flask-restful对象
	migrate = Migrate(app=app, db=db)
	# bootstrap.init_app(app) # 初始化bootstrap对象
	session.init_app(app=app)  # 初始化Session对象
	cors.init_app(app=app, supports_credentials=True)  # 初始化Flask-CORS对象,supports_credentials=True表示支持跨域请求
	jwt.init_app(app=app)  # 初始化JWTManager对象
	
	
	app.serializer = init_serializer(app=app)  # 初始化URLSafeTimedSerializer对象
	
	# 初始化redis对象
	redis_client = redis.Redis(
		host=settings.Config.REDIS_HOST,
		port=settings.Config.REDIS_PORT,
		db=settings.Config.REDIS_DB,
		password=settings.Config.REDIS_PASSWORD)
	app.redis_client = redis_client
	
	# 一定要导入模型，否则无法生成数据库表
	
	# 注册蓝图对象
	app.register_blueprint(basic_bp) # 注册用户蓝图对象
	
	return app


