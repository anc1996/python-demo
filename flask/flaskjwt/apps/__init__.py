#!/basic/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate
import redis
import settings
from apps.additional_claim.view import claim_bp

from apps.automatic_jwt.view import automatic_bp
from apps.basic.view import basic_bp
from apps.implict_refresh.view import implict_refresh_bp
from apps.jwt_revoking_redis.view import jwt_revoke_bp
from apps.locations.view import locations_bp
from apps.explicit_refresh.view import explicit_refresh_bp
from extends import db, cache, api, session, cors, init_serializer,jwt


def create_app():
	# 创建Flask实例
	
	app = Flask(__name__, template_folder='../templates', static_folder='../static')  # 创建Flask实例
	
	app.config.from_object(settings.DevelopmentConfig)
	db.init_app(app=app)  # 初始化SQLAlchemy对象
	cache.init_app(app=app)  # 初始化flask-caching缓存对象
	api.init_app(app=app)  # 初始化flask-restful对象
	migrate = Migrate(app=app, db=db)
	
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
	
	# 设置我们的 redis 连接以存储列入黑名单的 Token。
	# 您可能希望将 redis 实例配置为将数据持久保存到磁盘，以便重新启动不会导致应用程序忘记 JWT 已被撤销。
	jwt_redis_blocklist = redis.StrictRedis(
		host=settings.Config.REDIS_HOST,
		port=settings.Config.REDIS_PORT,
		db=settings.Config.JWT_REDIS_DB,
		password=settings.Config.REDIS_PASSWORD,
		decode_responses=True)  # decode_responses=True 返回的数据是str类型
	
	app.jwt_redis_blocklist = jwt_redis_blocklist
	
	
	
	# 一定要导入模型，否则无法生成数据库表
	from apps.automatic_jwt.model import AUTOMATIC
	
	# 注册蓝图对象
	# 方式一：基础jwt，注册basic蓝图对象
	# app.register_blueprint(basic_bp)
	
	# 方式二：注册automatic蓝图对象
	# app.register_blueprint(automatic_bp)
	# # 导入 jwt.py 文件，确保 @jwt.user_lookup_loader 回调函数被注册
	# import apps.automatic_jwt.jwt
	
	#  方式二：注册claim蓝图对象
	# app.register_blueprint(claim_bp)
	# import apps.additional_claim.jwt
	
	# 方式三：locations蓝图对象
	app.register_blueprint(locations_bp)
	
	# implict_refresh 刷新令牌
	app.register_blueprint(implict_refresh_bp)
	
	# explicit_refresh 刷新令牌
	app.register_blueprint(explicit_refresh_bp)
	
	# 注册蓝图对象
	app.register_blueprint(jwt_revoke_bp)
	
	return app


