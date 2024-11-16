#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import session, request, redirect, url_for, make_response,current_app,g
from functools import wraps


from apps.user.model import User
from extends.minio_bucket import flask_bucket


def get_user_id():
	
	# 如果session中没有user_id，再从cookie中获取
	singed_user_id = request.cookies.get('user_id')
	
	# 解密cookie中的user_id
	try:
		cookie_user_id = current_app.serializer.loads(singed_user_id).get('user_id')
	except Exception as e:
		# 如果解密失败，可能是cookie被篡改或过期
		print(f"Error decoding cookie: {e}")
		cookie_user_id = None
	
	if not cookie_user_id:
		# 如果cookie_user_id不存在，直接返回
		resp=make_response(redirect(url_for('user.login')))
		resp.delete_cookie('user_id')
		return None, resp
	
	# 从session中获取user_id，session[user.id] = user.username
	username = session.get(cookie_user_id)
	
	# 如果cookie_user_id和username都存在，且不一致，重定向到登录页
	user = User.query.filter_by(id=cookie_user_id).first()
	# session的username和数据库中的username不一致，重定向到登录页
	if username and user.username != username:
		# 删除cookie中的user_id
		resp = make_response(redirect(url_for('user.login')))
		resp.delete_cookie('user_id')
		# 删除session中的user_id
		if cookie_user_id in session:
			session.pop(cookie_user_id, default=None)
		# 返回user_id为空和response对象
		return None, resp
	
	return user, None


# 定义一个装饰器函数，用于检查用户是否已登录
def login_required(func):
	# 使用 wraps 装饰器来保留被装饰函数的元数据
	@wraps(func)
	def decorated_function(*args, **kwargs):
		# 调用 get_user_id 函数来获取用户信息和重定向响应
		user, redirect_response = get_user_id()
		
		# 如果 get_user_id 返回了重定向响应，则直接返回该响应
		if redirect_response:
			return redirect_response
		else:
			# 如果用户已登录，将用户信息存储在全局变量 g 中
			g.user = user
		
		# 调用被装饰的函数，并传递所有参数
		return func(*args, **kwargs)
	
	# 返回装饰后的函数
	return decorated_function
