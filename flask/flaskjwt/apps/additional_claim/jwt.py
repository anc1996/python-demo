#!/user/bin/env python3
# -*- coding: utf-8 -*-

from extends import jwt
# 使用 additional_claims_loader，我们可以指定一个在创建 JWT 时将调用的方法。修饰的方法必须采用标识
# 我们正在为要添加到 JWT 的其他声明创建一个令牌并返回一个字典。
"""
	您可以使用additional_claims_loader()装饰器注册一个回调函数，每当创建新的 JWT 时都会调用该函数，并返回要添加到该令牌的声明字典。
	如果同时使用additional_claims_loader()和additional_claims参数，两个结果将合并在一起，并与additional_claims参数提供的数据联系起来。
"""
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
        "aud": "some_audience",
        "foo": "bar",
        "upcase_name": identity.upper(), # 假设身份是一个字符串
    }