#!/basic/bin/env python3
# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from itsdangerous import URLSafeTimedSerializer
from flask_caching import Cache
from flask_restful import Api


db=SQLAlchemy()  # 实例化SQLAlchemy对象
bootstrap=Bootstrap5()  # 实例化Bootstrap对象
cache=Cache() # 实例化Cache对象
api=Api()  # 实例化Api对象
session=Session()  # 实例化Session对象
cors=CORS()  # 实例化CORS对象

jwt=JWTManager()  # 实例化JWTManager对象

# 实例化URLSafeTimedSerializer对象
def init_serializer(app):
    # 实例化URLSafeTimedSerializer对象
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])
