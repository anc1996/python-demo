#!/user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta

from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from extends import jwt
from flask import jsonify, current_app, Blueprint

jwt_revoke_bp = Blueprint('jwt_revoke', __name__, url_prefix='/jwt_revoke')
jwt_redis_blocklist = current_app.jwt_redis_blocklist

# 回调函数，用于检查 redis 黑名单中是否存在 JWT
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt_revoke_bp.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)

# 撤销当前用户访问 Token 的接口。将 JWT 唯一标识符 （jti） 保存在 redis 中。在存储 JWT 时，还要设置生存时间 （TTL）
# 这样在 Token 过期后会自动从 redis 中清除。
@jwt_revoke_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=timedelta(hours=1))
    return jsonify(msg="Access token revoked")


# 列入黑名单的访问令牌将无法再访问此令牌
@jwt_revoke_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(hello="world")