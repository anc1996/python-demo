#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_caching import Cache
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS


db=SQLAlchemy()  # 实例化SQLAlchemy对象
bootstrap=Bootstrap5()  # 实例化Bootstrap对象
cache=Cache() # 实例化Cache对象
api=Api()  # 实例化Api对象
session=Session()  # 实例化Session对象
cors=CORS()  # 实例化CORS对象
migrate=Migrate()  # 实例化Migrate对象
