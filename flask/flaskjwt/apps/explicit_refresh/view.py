#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity

explicit_refresh_bp = Blueprint('explicit_refresh', __name__, url_prefix='/explicit_refresh')


@explicit_refresh_bp.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@explicit_refresh_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@explicit_refresh_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(foo="bar")