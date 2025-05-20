# wagtailblog3/settings/dev.py

from .base import *

# 安全警告：请勿在生产环境中开启调试的情况下运行！
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-k@nr)u9ylv@5(i_cdp0za#$ofi0764)9(6r9*2^30(-7cwz)h="

# 安全警告：在生产环境中定义正确的主机！
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # 邮件后端配置，将邮件输出到控制台（用于开发环境）

# JWT 配置
from datetime import timedelta

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # 访问令牌的有效期，设为1小时
	'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新令牌的有效期，设为1天
	'ROTATE_REFRESH_TOKENS': False,  # 是否在刷新访问令牌时同时更新刷新令牌
	'BLACKLIST_AFTER_ROTATION': True,  # 令牌轮换后是否将旧的刷新令牌加入黑名单
	'UPDATE_LAST_LOGIN': False,  # 是否在认证成功后更新用户的最后登录时间
	
	'ALGORITHM': 'HS256',  # JWT签名算法，HMAC-SHA256是常用的对称算法
	'SIGNING_KEY': SECRET_KEY,  # 签名密钥，使用Django的SECRET_KEY
	'VERIFYING_KEY': None,  # 验证密钥，对称算法不需要单独指定
	'AUDIENCE': None,  # 令牌的目标接收者，None表示不验证此声明
	'ISSUER': None,  # 令牌的签发者，None表示不验证此声明
	
	'AUTH_HEADER_TYPES': ('Bearer',),  # 认证头类型，使用Bearer标准格式
	'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 认证头名称，对应HTTP的Authorization头
	'USER_ID_FIELD': 'id',  # 用户模型中用于标识用户的字段名
	'USER_ID_CLAIM': 'user_id',  # JWT中存储用户ID的声明名称
	
	'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 允许的令牌类型
	'TOKEN_TYPE_CLAIM': 'token_type',  # 在JWT中标识令牌类型的声明名称
	
	'JTI_CLAIM': 'jti',  # JWT ID声明字段名，用于唯一标识令牌
	
	'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # 滑动令牌中刷新过期时间的声明字段名
	'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),  # 滑动令牌的有效期，5分钟
	'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # 滑动刷新令牌的有效期，1天
}

# ===========================================================
# 增强调试配置
# ===========================================================

# 日志配置 - 详细输出到控制台
# 添加日志配置
import os
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 引入日志配置
from wagtailblog3.logging_config import get_logging_config
LOGGING = get_logging_config()


# 从环境变量获取日志级别和模块
log_level = os.environ.get('DJANGO_LOG_LEVEL', 'WARNING')
log_module = os.environ.get('DJANGO_LOG_MODULE', '')

# 更新日志配置
if log_module:
    LOGGING = get_logging_config(modules_filter=[log_module])

# 如果指定了日志级别，更新控制台处理器
if log_level != 'WARNING':
    LOGGING['handlers']['console']['level'] = log_level

# MongoDB调试信息
MONGO_DEBUG = True  # 在MongoDB适配器中使用此设置来控制详细日志输出

try:
	from .local import *
except ImportError:
	pass