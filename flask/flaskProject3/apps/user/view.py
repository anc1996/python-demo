#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from crypt import methods
from datetime import datetime, timedelta
from io import BytesIO

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, session, make_response
import re

from werkzeug.utils import secure_filename

from apps.user.form import UserForm
from apps.user.model import User
from sqlalchemy import or_
from extends import db
from extends.verify_code import generate_image


# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	
	if request.method == 'POST':
		# 获取post提交的数据
		username = request.form.get('username')
		password = request.form.get('password')
		# 判断用户名和密码是否为空
		if not all([username, password]):
			return render_template('user/login.html', msg='用户名和密码不能为空')
		# 查找用户且没有被逻辑删除
		user = User.query.filter_by(username = username, is_deleted = False).first()
		# 判断用户是否存在且密码是否正确
		if not user or not user.check_password(password):
			return render_template('user/login.html', msg='用户名或密码错误')
		# 登录成功，跳转到个人资料页
		return redirect(url_for('user.profile'))
	
	return render_template('user/login.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
	
	if request.method == 'POST':
		# 获取post提交的数据
		username = request.form.get('username')
		password = request.form.get('password')
		repassword = request.form.get('repassword')
		
		# 判断用户名和密码是否为空
		if not all([username, password, repassword]):
			return render_template('user/register.html', msg='用户名和密码不能为空')
		# 判断两次密码是否一致
		if password != repassword:
			return render_template('user/register.html', msg='两次密码不一致')
		
		phone = request.form.get('phone')
		# 判断手机号是否为空且格式是否正确
		if not phone and re.match(r'^1[3-9]\d{9}$', phone):
			return render_template('user/register.html', msg='手机号格式不正确')
		email = request.form.get('email')
		# 判断邮箱是否为空且格式是否正确
		if not email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
			return render_template('user/register.html', msg='邮箱格式不正确')
		
		# 判断用户是否已经注册
		# if any(user.username == username for user in users):
		# 	return render_template('user/register.html', msg='用户已注册')
		# 第一步：创建user对象
		user = User()
		user.username = username
		user.password = password
		user.phone = phone
		user.email = email
		# 第二步：将user对象添加到数据库
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('user.profile'))
	
	return render_template('user/register.html')


@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
	
	
	print(url_for('user.register'))  # 反向解析：/user/register
	# 从数据库中查询未删除的用户
	users = User.query.filter(User.is_deleted == False).all()
	return render_template('user/profile.html', users=users)


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
	return 'logout page'

@user_bp.route('/delete', methods=['GET'],endpoint='delete')
def delete_user():
	# 获取参数
	id = request.args.get('id')
	# 查找user对象是否存在
	user = User.query.filter_by(id = id, is_deleted = False).first()
	if user:
		user.is_deleted = True
		# 真正删除
		# db.session.delete(user)
		db.session.commit()
		return redirect(url_for('user.profile'))
	else:
		return '数据库没有当前数据'


@user_bp.route('/update', methods=['GET', 'POST'],endpoint='update')
def update_user():
	if request.method == 'POST':
		# 获取post提交的数据
		id= request.form.get('id')
		username = request.form.get('username')
		password = request.form.get('password')
		phone = request.form.get('phone')
		email= request.form.get('email')
		# 查找user对象是否存在
		user = User.query.filter(User.id == id, User.is_deleted == False).first()
		if user:
			user.password = password
			user.phone = phone
			user.email = email
			db.session.commit()
			return redirect(url_for('user.profile'))
		else:
			return '更新失败'
	# 获取get提交的数据
	id = request.args.get('id')
	user = User.query.filter_by(id = id, is_deleted = False).first()
	if user:
		return render_template('user/update.html', user=user)
	else:
		return '数据库没有当前数据'


@user_bp.route('/search_user', methods=['GET'], endpoint='search_user')
def search_user():
	search_content = request.args.get('search')
	
	if not search_content:
		return render_template('user/search.html', users=[])
	
	users = User.query.filter(
		or_(
			User.username.like(f'%{search_content}%'),
			User.phone.like(f'%{search_content}%'),
			User.email.like(f'%{search_content}%')
		),
		User.is_deleted == False
	).all()
	
	# Convert users to a list of dictionaries
	users = [{
		'id': user.id,
		'username': user.username,
		'phone': user.phone,
		'email': user.email,
		'register_time': user.register_time.strftime('%Y-%m-%d %H:%M:%S') if user.register_time else None
	} for user in users]
	
	return jsonify(users)


@user_bp.route('/', methods=['GET', 'POST'])
def hello_world():
	# 创建表单对象
	uform = UserForm()
	if uform.validate_on_submit():
		# 这些数据是UserForm验证通过后的数据
		username = uform.username.data
		password = uform.password.data
		phone = uform.phone.data
		icon = uform.icon.data
		filename = secure_filename(icon.filename)
		# icon.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
		return '提交成功！'
	
	return render_template('user/user.html', uform=uform)


@user_bp.route('/image_code',methods=['GET'])
def image_code():
	# 检查是否有之前的验证码session，如果有则删除
	if 'image_code' in session:
		session.pop('image_code')
	# 生成验证码
	image,code = generate_image(current_app.config['IMAGE_CODE_LENGTH'])
	# 将验证码图片转换为二进制
	buffer=BytesIO() # BytesIO对象用于在内存中存储二进制数据
	image.save(buffer,'JPEG')
	buffer_bytes=buffer.getvalue()
	
	# 将验证码保存到session中
	session['image_code'] = {
		'code':code,
		# 设置验证码的过期时间为5分钟
		'expiration':(datetime.now()+timedelta(minutes=5)).timestamp()
	}
	
	# 将验证码图片返回给客户端
	response=make_response(buffer_bytes)
	response.headers['Content-Type'] = 'image/jpeg'
	return response

