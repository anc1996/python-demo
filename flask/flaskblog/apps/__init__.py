#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_migrate import Migrate
import redis
from logging.config import dictConfig
import settings
from apps.news.view import news_bp

from extends import db, init_serializer, cache, api, session, cors
from apps.user.view import user_bp
from apps.article.view import article_bp
from apps.goods.view import goods_bp
from apps.home.view import home_bp
from extends.article_function import setup_global_hooks


def create_app():
	# 创建Flask实例
	
	app = Flask(__name__, template_folder='../templates', static_folder='../static')  # 创建Flask实例
	
	app.config.from_object(settings.DevelopmentConfig)
	db.init_app(app=app) # 初始化SQLAlchemy对象
	cache.init_app(app=app) # 初始化flask-caching缓存对象
	api.init_app(app=app) # 初始化flask-restful对象
	migrate = Migrate(app=app, db=db)
	# bootstrap.init_app(app) # 初始化bootstrap对象
	session.init_app(app=app)  # 初始化Session对象
	cors.init_app(app=app,supports_credentials=True) # 初始化Flask-CORS对象,supports_credentials=True表示支持跨域请求
	
	app.serializer = init_serializer(app=app) # 初始化URLSafeTimedSerializer对象
	
	# 初始化redis对象
	redis_client=redis.Redis(
			host=settings.Config.REDIS_HOST,
			port=settings.Config.REDIS_PORT,
			db=settings.Config.REDIS_DB,
			password=settings.Config.REDIS_PASSWORD)
	app.redis_client=redis_client
	
	
	# 注册全局钩子函数
	setup_global_hooks(app)
	
	# 配置日志信息
	dictConfig(settings.DevelopmentConfig.LOGGING_CONFIG)
	logger = logging.getLogger('root')
	logger.info('Flask application started')
	logger.debug('debug message')
	logger.error('error message')
	logger.warning('warning message')
	
	# 一定要导入模型，否则无法生成数据库表
	from apps.user.model import User,UserInfo,UserAlbum
	from apps.article.model import Article,Comment,ArticleType,ArticleFile
	from apps.goods.model import Goods,UserGoodsAssociation
	from apps.news.model import News,NewsType
	# 注册蓝图对象
	app.register_blueprint(user_bp) # 注册用户蓝图
	app.register_blueprint(article_bp) # 注册文章蓝图
	app.register_blueprint(goods_bp) # 注册商品蓝图
	app.register_blueprint(home_bp) # 注册首页蓝图
	app.register_blueprint(news_bp) # 注册文章蓝图
	
	# 打印所有的url
	# print(app.url_map)
	
	return app


