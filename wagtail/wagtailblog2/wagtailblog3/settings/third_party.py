#!/user/bin/env python3
# -*- coding: utf-8 -*-


"""
第三方服务配置文件,
包含 REST Framework、CORS 等第三方集成配置
"""




# ==========================================================
# Django REST Framework 配置
# ==========================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 使用JWT令牌认证
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # 默认权限：认证用户可读写，匿名用户只读
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # 使用分页页码
    'PAGE_SIZE': 10,  # 每页显示10条记录
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # 默认使用JSON渲染器
    ),
}


# ==========================================================
# CORS 跨域配置 (依赖django-cors-headers包)
# ==========================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Vue.js 开发服务器
    "http://0.0.0.0:8080",  # 本地IP访问
]

CORS_ALLOW_METHODS = [  # 允许的HTTP请求方法
    'DELETE',  # 删除资源
    'GET',     # 获取资源
    'OPTIONS', # 预检请求
    'PATCH',   # 部分更新资源
    'POST',    # 创建资源
    'PUT',     # 完全更新资源
]

CORS_ALLOW_HEADERS = [  # 允许的HTTP请求头
    'accept',          # 指定客户端能够接收的内容类型
    'accept-encoding', # 指定客户端能够理解的编码方式
    'authorization',   # 包含身份验证信息
    'content-type',    # 指定请求体的媒体类型
    'dnt',            # Do Not Track请求头
    'origin',         # 指示请求来自哪个站点
    'user-agent',     # 客户端应用类型
    'x-csrftoken',    # CSRF防护令牌
    'x-requested-with', # 用于标识AJAX请求
]


# ==========================================================
# Swagger API 文档配置
# ==========================================================
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}