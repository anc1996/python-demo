#!/user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime,timezone,timedelta

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies, \
	jwt_required

implict_refresh_bp = Blueprint('implict_refresh', __name__, url_prefix='/implict_refresh')

"""实现一种自动刷新访问令牌的机制，同时结合了 Flask 的生命周期钩子（after_request）来优化用户体验。
"""


"""自动刷新令牌的实现"""
# 使用 'after_request' 回调，我们刷新 30 以内的任何 Token
# 过期分钟数。更改 timedeltas 以匹配您的应用程序的需求。
# flask,after_request:在每次请求之后调用的函数，无论是否发生异常。
@implict_refresh_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        # 如果 Token 在 30 分钟内过期，则刷新 Token
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            # 刷新 Token
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        response.headers['X-Custom-Header'] = 'implict_refresh from Blueprint'
        return response
    except (RuntimeError, KeyError):
        # 没有有效 JWT 的情况。只需返回原始响应
        return response

"""
    实现基本的登录功能，生成访问令牌。
    通过 set_access_cookies 将令牌存储在客户端的 Cookie 中。
"""
@implict_refresh_bp.route("/login", methods=["POST"])
def login():
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity="example_user")
    set_access_cookies(response, access_token)
    return response


@implict_refresh_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    # unset_jwt_cookies() 删除包含访问或刷新 JWT 的 cookie。
    unset_jwt_cookies(response)
    return response



"""受保护的路由，只有有效的 JWT 才能访问。使用 @jwt_required() 验证令牌有效性和身份。"""
@implict_refresh_bp.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")