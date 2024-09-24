#!/user/bin/env python3
# -*- coding: utf-8 -*-
from crypt import methods

from flask import Blueprint, render_template, request, redirect, url_for
import re
from apps.user.model import User

users = []

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


        # 查找用户
        user = next((user for user in users if user.username == username), None)

        if not user:
            return render_template('user/login.html', msg='用户未注册')

        # 验证密码
        if user.password != password:
            return render_template('user/login.html', msg='密码错误')

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
		# 判断手机号是否为空
		if not phone and re.match(r'^1[3-9]\d{9}$', phone):
			return render_template('user/register.html', msg='手机号格式不正确')
		# 判断用户是否已经注册
		if any(user.username == username for user in users):
			return render_template('user/register.html', msg='用户已注册')
		user = User(username, password, phone)
		users.append(user)
		return redirect(url_for('user.profile'))
	return render_template('user/register.html')



@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
	print(url_for('user.register')) # 反向解析：/user/register
	return render_template('user/show.html', users=users)


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
	return 'logout page'

@user_bp.route('/delete', methods=['GET'],endpoint='delete')
def delete_user():
	# 获取参数
	username = request.args.get('username')
	# 查找user对象是否存在
	for user in users:
		if user.username == username:
			users.remove(user)
			return redirect(url_for('user.profile'))
	else:
		return '删除失败'


@user_bp.route('/update', methods=['GET', 'POST'],endpoint='update')
def update_user():
	if request.method == 'POST':
		# 获取post提交的数据
		username = request.form.get('username')
		password = request.form.get('password')
		phone = request.form.get('phone')
		# 查找user对象是否存在
		for user in users:
			if user.username == username:
				user.password = password
				user.phone = phone
				return redirect(url_for('user.profile'))
		else:
			return '更新失败'
	# 获取get提交的数据
	username = request.args.get('username')
	# 查找user对象是否存在
	for user in users:
		if user.username == username:
			return render_template('user/update.html', user=user)
	else:
		return '数据库没有当前数据'