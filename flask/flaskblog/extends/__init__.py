#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from itsdangerous import URLSafeTimedSerializer
db=SQLAlchemy()  # 实例化SQLAlchemy对象
bootstrap=Bootstrap5()  # 实例化Bootstrap对象

# 实例化URLSafeTimedSerializer对象
def init_serializer(app):
    # 实例化URLSafeTimedSerializer对象
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])
