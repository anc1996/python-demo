#!/basic/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


claim_bp = Blueprint('claim', __name__, url_prefix='/claim')

"""部分保护路由允许你在一个视图中同时处理已认证和未认证用户。在某些情况下，无论 JWT 是否有效，您都希望使用相同的路由 是否存在于请求中。
在这些情况下，您可以使用 jwt_required()带有optional=True参数。这将允许访问端点，无论是否随请求发送 JWT。"""

# 创建路由来验证您的用户并返回 JWT。这
# create_access_token（） 函数用于实际生成 JWT。
@claim_bp.route('/login', methods=['POST'])
def login():
	username = request.json.get('username', None)
	password = request.json.get('password', None)
	if username != 'test' or password != 'test':
		return jsonify({"msg": "用户名或密码错误"}), 401
	
	# 方式一：
	# 您可以使用 additional_claims 参数在 JWT 中添加自定义声明或覆盖默认声明。
	# additional_claims = {"aud": "some_audience", "foo": "bar"}
	# access_token = create_access_token(identity=username, additional_claims=additional_claims)
	# 创建JWT令牌
	access_token = create_access_token(identity=username)
	return jsonify({"access_token": access_token}), 200


# 使用 jwt_required 保护路由，这将踢出请求
# 不存在有效的 JWT。
# $ 返回 "access_token": "eyJ0eXAiO..."
# $ http GET :5000/protected Authorization:"Bearer eyJ0eXAiO.."
@claim_bp.route('/protected1', methods=['GET'])
@jwt_required()
def protected1():
	# 获取当前登录的用户
	current_user = get_jwt_identity()
	claims = get_jwt()
	return jsonify(logged_in_as=current_user,foo=claims['foo']), 200

# optional=True 选项，如果没有提供有效的 JWT，那么 get_jwt_identity() 将返回 None。
@claim_bp.route('/protected2', methods=['GET'])
@jwt_required(optional=True)
def protected2():
	# 获取当前登录的用户
	current_user = get_jwt_identity()
	if current_user:
		return jsonify(logged_in_as=current_user)
	else:
		return jsonify(logged_in_as="anonymous user")