#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os.path


class Config:
	SECRET_KEY='setting1234222' # 密钥
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@localhost:3306/flaskProject2' # 数据库连接
	SQLALCHEMY_TRACK_MODIFICATIONS=False  # 是否追踪数据库的修改
	BASE_DIR=os.path.dirname(os.path.abspath(__file__))  # 项目的根目录
	STATIC_DIR=os.path.join(BASE_DIR,'static')  # 静态文件的目录
	UPLOAD_DIR=os.path.join(STATIC_DIR,'upload')  # 上传文件的目录
	
	# wtfrom Recaptcha 配置
	RECAPTCHA_PUBLIC_KEY = '6LfoEnEqAAAAAGN_0o8s1AOuYFubBizM9qojptuO'
	RECAPTCHA_PRIVATE_KEY = '6LfoEnEqAAAAAM4mnXWFiDyAZmT_pm9PIyoIxbYt'
	RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
	RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
	
	# 图形验证码长度
	IMAGE_CODE_LENGTH=4
	
class DevelopmentConfig(Config):
	ENV = 'development'  # 环境
	# 配置对象加载配置信息
	DEBUG = True  # 开启调试模式
	SQLALCHEMY_ECHO=True  # 开启SQLAlchemy的调试模式
	
class ProductionConfig(Config):
	ENV = 'production'  # 环境
	DEBUG = False  # 关闭调试模式
	SQLALCHEMY_ECHO=False  # 关闭SQLAlchemy的调试模式