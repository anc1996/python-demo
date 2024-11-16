#!/user/bin/env python3
# -*- coding: utf-8 -*-
from apps.automatic_jwt.model import AUTOMATIC
from extends import jwt


# 注册一个回调函数，该函数将传入的任何对象作为标识并将其转换为 JSON 可序列化格式。
# 这个时在登录时，我们将用户的 id 传入 create_access_token 函数，然后在访问受保护的路由时，
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# 注册一个回调函数，每当访问受保护的路由。这应该返回成功查找，
# 如果查找因任何原因失败（例如如果用户已从数据库中删除）。
# 通过在 create_app 函数中导入 jwt.py 文件，可以确保在 jwt.init_app(app) 之后，@jwt.user_lookup_loader 回调函数被正确注册。
# 这个是在访问被授予时，return current_user.
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return AUTOMATIC.query.filter_by(id=identity).one_or_none()
