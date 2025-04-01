#!/user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta
from pickle import FALSE
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from flask import jsonify, current_app, Blueprint

from extends import jwt

jwt_revoke_bp = Blueprint('jwt_revoke', __name__, url_prefix='/jwt_revoke')

"""
在最简单的形式中，使用此扩展没有太多需要。你用 create_access_token()来制作 JSON Web 令牌， jwt_required()来保护路由，以及 get_jwt_identity()获取受保护路由中 JWT 的身份。
"""


# 回调函数，用于检查 redis 黑名单中是否存在 JWT
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    jwt_redis_blocklist = current_app.jwt_redis_blocklist
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt_revoke_bp.route("/login", methods=["POST"])
def login():
    # 创建访问令牌
    access_token = create_access_token(identity="example_user")
    # 创建刷新令牌
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token,refresh_token=refresh_token)


# 我们在 jwt_required 中使用 'refresh=True' 选项，以仅允许刷新令牌访问此路由。
@jwt_revoke_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_revoke_bp.route("/fresh", methods=["POST"])
@jwt_required(refresh=True)
def fresh():
    identity = get_jwt_identity()
    # 如果我们在这里刷新令牌，我们已经有一段时间没有验证用户密码了，因此请将新创建的访问令牌标记为非新令牌
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


# 撤销当前用户访问 Token 的接口。将 JWT 唯一标识符 （jti） 保存在 redis 中。在存储 JWT 时，还要设置生存时间 （TTL）
# 这样在 Token 过期后会自动从 redis 中清除。
# verify_type=FALSE 表示不验证 token 类型，可以实现撤销访问令牌和刷新令牌的功能
@jwt_revoke_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=FALSE)
def logout():
    # 从当前访问的 JWT 中获取 jti
    jti = get_jwt()["jti"]
    ttype = get_jwt()["type"] # 获取 token 类型
    # 将 jti 列入黑名单
    jwt_redis_blocklist = current_app.jwt_redis_blocklist
    jwt_redis_blocklist.set(jti, "", ex=timedelta(hours=1))
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


# 列入黑名单的访问令牌将无法再访问此令牌
@jwt_revoke_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(hello="world")


# 只允许新的 JWT 使用 'fresh=True' 参数访问此路由。（最好是敏感内容）
@jwt_revoke_bp.route("/fresh-protected", methods=["GET"])
@jwt_required(fresh=True)
def fresh_protected():
    return jsonify(foo="fresh-protected")