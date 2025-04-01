#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity

explicit_refresh_bp = Blueprint('explicit_refresh', __name__, url_prefix='/explicit_refresh')

"""
    flask-jwt-extended 提供了精细的访问控制机制，其中包括对访问令牌的新鲜度（Freshness）和刷新机制的支持。
        访问令牌（Access Token）：
            用于用户认证，包含用户身份信息（identity）。
            有效期较短，适合频繁的 API 请求。
        刷新令牌（Refresh Token）：
            用于获取新的访问令牌。
            有效期较长，通常只用于重新生成访问令牌。
"""

@explicit_refresh_bp.route("/login", methods=["POST"])
def login():
    # 创建一个访问令牌
    access_token = create_access_token(identity="example_user")
    # 创建一个刷新令牌
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# 我们在 jwt_required 中使用 'refresh=True' 选项，以仅允许刷新令牌访问此路由。
@explicit_refresh_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@explicit_refresh_bp.route("/fresh",methods=["POST"])
@jwt_required(refresh=True)
def fresh():
    identity = get_jwt_identity()
   # 如果我们在这里刷新令牌，我们已经有一段时间没有验证用户密码了，因此请将新创建的访问令牌标记为非新令牌
    """
        1、Fresh 访问令牌：当用户通过提供用户名和密码进行身份验证时，服务器会生成一个“fresh”访问令牌。这个 fresh 访问令牌可以访问所有路由，
                包括那些需要高安全级别的敏感操作（如更改电子邮件地址、修改密码等）。
        2、非 Fresh 访问令牌：随着时间的推移，fresh 访问令牌会过期或被视为不再 fresh。此时，
                用户仍然可以使用这个访问令牌访问大部分非敏感的路由，但无法再访问那些需要 fresh 访问令牌的敏感路由。
        3、重新验证：如果用户需要执行某些敏感操作（如更改电子邮件地址），他们必须重新验证其身份（通常是通过再次输入用户名和密码），以获取一个新的 fresh 访问令牌。
    """
    access_token = create_access_token(identity=identity, fresh=False)
    # create_access_token(identity, fresh=datetime.timedelta(minutes=15))
    return jsonify(access_token=access_token)


# 只允许新的 JWT 使用 'fresh=True' 参数访问此路由。
@explicit_refresh_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(foo="bar")

# 只允许新的 JWT 使用 'fresh=True' 参数访问此路由。（最好是敏感内容）
@explicit_refresh_bp.route("/fresh-protected", methods=["GET"])
@jwt_required(fresh=True)
def fresh_protected():
    return jsonify(foo="fresh-protected")