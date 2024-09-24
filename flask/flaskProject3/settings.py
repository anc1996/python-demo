#!/user/bin/env python3
# -*- coding: utf-8 -*-
class Config:
	SECRET_KEY='setting1234222' # 密钥
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@localhost:3306/flaskProject2' # 数据库连接
	SQLALCHEMY_TRACK_MODIFICATIONS=False  # 是否追踪数据库的修改

class DevelopmentConfig(Config):
	ENV = 'development'  # 环境
	# 配置对象加载配置信息
	DEBUG = True  # 开启调试模式
	SQLALCHEMY_ECHO=True  # 开启SQLAlchemy的调试模式
	
class ProductionConfig(Config):
	ENV = 'production'  # 环境
	DEBUG = False  # 关闭调试模式
	SQLALCHEMY_ECHO=False  # 关闭SQLAlchemy的调试模式