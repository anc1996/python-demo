#!/basic/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from extends import jwt

basic_bp=Blueprint('basic', __name__, url_prefix='/basic')

# 创建路由来验证您的用户并返回 JWT。这
# create_access_token（） 函数用于实际生成 JWT。
@basic_bp.route('/login', methods=['POST'])
def login():
    
    username=request.json.get('username',None)
    password=request.json.get('password',None)
    if username!='test' or password!='test':
        return jsonify({"msg": "用户名或密码错误"}), 401

    # 创建JWT令牌
    access_token=create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


# 使用 jwt_required 保护路由，这将踢出请求
# 不存在有效的 JWT。
# $ 返回 "access_token": "eyJ0eXAiO..."
# $ http GET :5000/protected Authorization:"Bearer eyJ0eXAiO.."
@basic_bp.route('/verification', methods=['GET'])
@jwt_required()
def verification():
	
	# 获取当前登录的用户
	current_user = get_jwt_identity()
	return jsonify(logged_in_as=current_user), 200