#!/user/bin/env python3
# -*- coding: utf-8 -*-
# apps/home/view.py
from flask import Blueprint, render_template, jsonify,g

from extends import cache
from extends.login_verify import get_user_id

home_bp = Blueprint('home', __name__)

@home_bp.app_template_filter('cdecode')
def content_decode(content):
	content=content.decode('utf-8')
	return content

# 全局变量



@home_bp.route('/get_categories', methods=['GET'])
def get_categories():
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	# 将 ArticleType 实例转换为可序列化格式
	serializable_categories = []
	for category_dict in second_level_categories:
		for first_level, second_levels in category_dict.items():
			serializable_dict = {
				'first_level': {
					'id': first_level.id,
					'type_name': first_level.type_name
				},
				'second_levels': [
					{
						'id': second_level.id,
						'type_name': second_level.type_name
					} for second_level in second_levels
				]
			}
			serializable_categories.append(serializable_dict)
	
	return jsonify(serializable_categories)

@home_bp.route('/', methods=['GET'], endpoint='index')
@cache.cached(timeout=3600)
def index():
	user, redirect_response = get_user_id()
	# 获取二级分类
	second_level_categories = g.second_level_categories
	# 如果用户存在，渲染带有用户信息的模板
	if user:
		userinfo = user.userinfo
		return render_template('index.html', user=user,userinfo=userinfo,second_level_categories=second_level_categories)
	
	# 如果用户不存在，渲染默认模板
	return render_template('index.html',second_level_categories=second_level_categories)


@home_bp.route('/base1')
def base1():
	return render_template('base1.html')