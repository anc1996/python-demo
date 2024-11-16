#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required

locations_bp = Blueprint('locations', __name__, url_prefix='/locations')

@locations_bp.route("/login_without_cookies", methods=["POST"])
def login_without_cookies():
	# 创建访问令牌
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)


@locations_bp.route("/login_with_cookies", methods=["POST"])
def login_with_cookies():
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity="example_user")
	# 修改 Flask Response 以设置包含访问 JWT 的 cookie。
    # 如果 ''JWT_CSRF_IN_COOKIES'' 是 ''True'' ，则同时设置相应的 CSRF cookie
    # （参见 ：ref：'配置选项'）
    set_access_cookies(response, access_token)
    return response


@locations_bp.route("/logout_with_cookies", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    # 修改 Flask 响应以删除包含访问或刷新 JWT 的 cookie。
    # 如果适用，还会删除相应的 CSRF Cookie。
    unset_jwt_cookies(response)
    return response


@locations_bp.route("/protected", methods=["GET", "POST"])
@jwt_required()
def protected():
	# 从JWT中获取用户身份
    return jsonify(foo="bar")

# 只能从cookies中提取JWT
@locations_bp.route("/only_cookies", methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
def only_cookies():
    return jsonify(foo="qux")

# 仅从headers中提取JWT
@locations_bp.route("/only_headers", methods=["GET", "POST"])
# location参数指定从哪里提取JWT,默认是从json中提取JWT,这里指定从headers中提取JWT
@jwt_required(locations=["headers"])
def only_headers():
	# 从请求头中获取JWT
    return jsonify(foo="baz")


# 仅从查询字符串中提取JWT
@locations_bp.route("/only_query_string", methods=["GET", "POST"])
@jwt_required(locations=["query_string"])
def only_query_string():
    return jsonify(foo="quux")

# 仅从json中提取JWT
@locations_bp.route("/only_json_body", methods=["POST"])
@jwt_required(locations=["json"])
def only_json_body():
    return jsonify(foo="corge")