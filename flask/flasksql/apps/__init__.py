#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask

from config import db,settings,cache,api,migrate
from apps.appliances.view import appliance_bp
from apps.graphysql.graphys import graphsql_bp

def create_app():
	# 创建Flask实例
	
	app = Flask(__name__)  # 创建Flask实例
	app.config.from_object(settings.DevelopmentConfig)
	app.template_folder=app.config['TEMPLATE_DIR']
	app.static_folder=app.config['STATIC_DIR']
	
	# 初始化SQLAlchemy对象
	db.init_app(app)
	cache.init_app(app=app)  # 初始化flask-caching缓存对象
	api.init_app(app=app)  # 初始化flask-restful对象
	migrate.init_app(app=app, db=db) # 初始化flask-migrate对象

	
	# 一定要导入模型，否则无法生成数据库表
	from apps.appliances.model import Appliance,Part
	with app.app_context():
		db.metadata.create_all(bind=db.engine, tables=[Appliance.__table__, Part.__table__])
	
	# 注册蓝图对象
	app.register_blueprint(blueprint=appliance_bp)
	app.register_blueprint(blueprint=graphsql_bp)
	
	return app