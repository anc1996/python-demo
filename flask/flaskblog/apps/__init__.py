#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
import redis

from extends import db, init_serializer, cache
from apps.user.view import user_bp
from apps.article.view import article_bp
from apps.goods.view import goods_bp
from apps.home.view import home_bp
import settings
from extends.article_function import setup_global_hooks


def create_app():
	# 创建Flask实例
	app = Flask(__name__, template_folder='../templates', static_folder='../static')  # 创建Flask实例
	
	app.config.from_object(settings.DevelopmentConfig)
	# 初始化SQLAlchemy对象
	db.init_app(app)
	# 初始化flask-caching缓存对象
	cache.init_app(app=app)
	
	# 初始化bootstrap对象
	# bootstrap.init_app(app)
	migrate = Migrate(app=app, db=db)
	# 初始化URLSafeTimedSerializer对象
	app.serializer = init_serializer(app)
	
	# 初始化redis对象
	redis_client=redis.Redis(
			host=settings.Config.REDIS_HOST,
			port=settings.Config.REDIS_PORT,
			db=settings.Config.REDIS_DB,
			password=settings.Config.REDIS_PASSWORD)
	
	app.redis_client=redis_client
	
	app.config['SESSION_REDIS'] = redis_client
	# 初始化Session对象
	Session(app)
	
	# 注册全局钩子函数
	setup_global_hooks(app)
	
	# 一定要导入模型，否则无法生成数据库表
	from apps.user.model import User,UserInfo,UserAlbum
	from apps.article.model import Article,Comment,ArticleType,ArticleFile
	from apps.goods.model import Goods,UserGoodsAssociation
	# 注册蓝图对象
	app.register_blueprint(user_bp) # 注册用户蓝图
	app.register_blueprint(article_bp) # 注册文章蓝图
	app.register_blueprint(goods_bp) # 注册商品蓝图
	app.register_blueprint(home_bp) # 注册首页蓝图
	# 打印所有的路由信息
	for rule in app.url_map.iter_rules():
		print(f'endpoint:{rule.endpoint},url:{rule.rule}')
	
	return app


