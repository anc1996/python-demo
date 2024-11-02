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
			session.pop(cookie_user_id)
		# 返回user_id为空和response对象
		return None, resp
	
	return user, None


def login_required(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		user, redirect_response = get_user_id()
		if redirect_response:
			return redirect_response
		else:
			g.user = user
		return func(*args, **kwargs)
	return decorated_function
