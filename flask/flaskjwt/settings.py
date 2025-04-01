#!/basic/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta

import redis
import os

class Config:
	
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flaskjwt'  # 数据库连接
	SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库的修改
	SECRET_KEY = '1sdfarweffabdfadFwerwEFCSCDWEWEZP'  # 密钥
	
	# reids配置
	REDIS_HOST = 'localhost'
	REDIS_PORT = 6379
	REDIS_DB = 6
	REDIS_PASSWORD = '123456'
	
	# flask-caching缓存配置
	CACHE_TYPE = 'redis'  # 缓存类型
	CACHE_REDIS_HOST = 'localhost'  # redis主机
	CACHE_REDIS_PORT = 6379  # redis端口
	CACHE_REDIS_DB = 7  # redis数据库
	CACHE_REDIS_PASSWORD = '123456'  # redis密码
	CACHE_DEFAULT_TIMEOUT = 300  # 缓存默认过期时间
	
	# session配置
	SESSION_TYPE = 'redis'  # session类型
	SESSION_KEY_PREFIX = 'session:'  # session的key前缀
	SESSION_USE_SIGNER = True  # 是否使用签名
	SESSION_PERMANENT = False  # 是否长期有效
	SESSION_REDIS = redis.Redis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		db=5,
		password=REDIS_PASSWORD)  # Redis 连接信息
	
	# 项目路径
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目路径
	# 静态文件路径
	STATIC_DIR = os.path.join(BASE_DIR, 'static')
	# 模板文件路径
	TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
	
	#  jwt,用于生成token
	JWT_SECRET_KEY='123456'
	
	# JWT_TOKEN_LOCATION是一个列表，指示从请求中提取JWT的位置。
	# 默认情况下，它将从JSON中提取JWT，但也可以从查询字符串，头文件或cookie中提取JWT。
	"""
		headers: 从请求头中提取JWT
		cookies: 从cookie中提取JWT
		json: 从json中提取JWT
		query_string: 从查询字符串中提取JWT
	"""
	JWT_TOKEN_LOCATION=["headers", "cookies", "json", "query_string"]
	
	# 如果为真，则只允许发送包含您的JWT的Cookie，通过https。在生产环境中，应始终将其设置为True
	JWT_COOKIE_SECURE=False
	
	# JWT_ACCESS_TOKEN_EXPIRES指定访问令牌的过期时间。这可以是整数秒，也可以是datetime.timedelta。,默认为15分钟
	JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
	# JWT_REFRESH_TOKEN_EXPIRES指定刷新令牌的过期时间。这可以是整数秒，也可以是datetime.timedelta。,默认为30天
	JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
	JWT_REDIS_DB=8 # redis数据库
	

	

class DevelopmentConfig(Config):
	ENV = 'development'  # 环境
	# 配置对象加载配置信息
	DEBUG = True  # 开启调试模式
	SQLALCHEMY_ECHO = True  # 开启SQLAlchemy的调试模式
	

class ProductionConfig(Config):
	ENV = 'production'  # 环境
	DEBUG = False  # 关闭调试模式
	SQLALCHEMY_ECHO = False  # 关闭SQLAlchemy的调试模式
