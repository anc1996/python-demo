#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user

from apps.automatic_jwt.model import AUTOMATIC
from extends import db,jwt

automatic_bp=Blueprint('automatic', __name__, url_prefix='/automatic')


@automatic_bp.route("/login", methods=["POST"])
def login():
    
    # 从请求中获取用户名和密码
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # 验证用户名和密码，one_or_none()方法,确保查询最多返回一个结果时非常有用。
    automatic = AUTOMATIC.query.filter_by(username=username).one_or_none()
    if not automatic or not automatic.check_password(password):
        return jsonify("用户名或密码错误"), 401

    # 请注意，我们在此处传入了实际的 sqlalchemy 用户对象
    access_token = create_access_token(identity=automatic)
    return jsonify(access_token=access_token)


@automatic_bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # 我们现在可以通过 'current_user' 访问我们的 sqlalchemy User 对象。
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )

@automatic_bp.route("/create", methods=["GET"])
def create_automatic():
    db.create_all()
    db.session.add(AUTOMATIC(full_name="Bruce Wayne", username="batman",password='123456'))
    db.session.add(AUTOMATIC(full_name="Ann Takamaki", username="panther",password='123456'))
    db.session.add(AUTOMATIC(full_name="Jester Lavore", username="little_sapphire",password='123456'))
    db.session.commit()
    return jsonify({"message": "Users created successfully"}), 201