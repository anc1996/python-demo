#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
import settings
from apps.error.view import error_bp
from apps.person.view import person_bp
from apps.railway.view import railway_bp
from apps.students.view import student_bp

from extends import db,middleware
from apps.user.view import user_bp
from apps.user.user_select_view import user_select_bp


def create_app():
	# 创建Flask实例
	app = Flask(__name__, template_folder='../templates', static_folder='../static')  # 创建Flask实例
	
	app.config.from_object(settings.DevelopmentConfig)
	# 初始化SQLAlchemy对象
	db.init_app(app)
	
	migrate = Migrate(app=app, db=db)
	from apps.user.model import User
	from apps.students.model import Student,StudentInfo,StudentAddress
	from apps.railway.model import Passenger,Train,passenger_ticket
	from apps.person.model import Person
	
	# 注册蓝图对象
	app.register_blueprint(user_bp) # 注册用户蓝图
	app.register_blueprint(user_select_bp) # 注册用户查询蓝图
	app.register_blueprint(student_bp)# 注册学生蓝图
	app.register_blueprint(railway_bp) # 注册角色蓝图
	app.register_blueprint(person_bp) # 注册人员蓝图,这个是学习flask的类视图
	app.register_blueprint(error_bp) # 注册错误蓝图
	
	# 打印所有的路由信息
	for rule in app.url_map.iter_rules():
		print(f'endpoint:{rule.endpoint},url:{rule.rule}')
		
	# 中间件
	app.wsgi_app=middleware.LoggingMiddleware(app.wsgi_app)
	
	return app
