#!/user/bin/env python3
# -*- coding: utf-8 -*-

import os,redis

class Config:
	
	SECRET_KEY = 'setting1234222'  # 密钥
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flasksql'  # 数据库连接
	SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库的修改
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目的根目录
	STATIC_DIR = os.path.join(BASE_DIR, 'static')  # 静态文件的目录
	# 模板文件路径
	TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
	
	# reids配置
	REDIS_HOST = 'localhost'
	REDIS_PORT = 6379
	REDIS_DB = 4
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
		db=6,
		password=REDIS_PASSWORD)  # Redis 连接信息
	
	
class DevelopmentConfig(Config):
	ENV = 'development'  # 环境
	# 配置对象加载配置信息
	DEBUG = True  # 开启调试模式
	SQLALCHEMY_ECHO=True  # 开启SQLAlchemy的调试模式
	
class ProductionConfig(Config):
	ENV = 'production'  # 环境
	DEBUG = False  # 关闭调试模式
	SQLALCHEMY_ECHO=False  # 关闭SQLAlchemy的调试模式