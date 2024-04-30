﻿"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# Django 项目的配置文件。
# 开发环境
from pathlib import Path
import os,sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# __file__表示当前Python文件的位置。这个代码片段表示获取当前文件的父目录的绝对路径。
# resolve()方法使路径绝对，解决所有的符号链接的方式，也将其规范化(例如将斜杠变为反斜杠) Windows)。
# Path(__file__).resolve()返回一个Path对象，表示当前文件的绝对路径。例如：返回：PosixPath('/****/settings.py')
# Path(__file__).parent.parent返回当前文件的父目录。# PosixPath('/home/source/Django/bookmanager')
# parent属性是Path对象的一个属性，它返回一个Path对象，表示父目录。
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR路径:',BASE_DIR)
# os.path.dirname 是 Python 的一个内置函数，用于获取指定文件或目录的父目录的路径。
print('BASE_DIR的dirname路径:',os.path.dirname(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qh&^i+&!u(4$x8f#v9^dw2a^bq_ugjvybeb9i$6rutyi0802zh"

# 安全警告:不要在生产环境中打开调试开关运行!
DEBUG = True

# 允许以哪个主机的形式访问后端
# 默认情况下，ALLOWED_HOSTS 是一个空列表，表示不允许外网任何主机访问后端。
ALLOWED_HOSTS = ['*',]



# 查看导包路径
print('查看导包路径sys:',sys.path) # 包含'/root/anaconda3/envs/shop/lib/python3.9/site-packages'
# 追加导包路径指向apps,即shop/apps
'''BASE_DIR=/***/shop/shop'''
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
# sys列表第一个元素就是apps路径
print('sys[0]:',sys.path[0])


# Application definition
# 安装的应用程序列表。每个应用程序都是一个 Python 包，它包含一些特定功能的代码。
INSTALLED_APPS = [
    # 管理员应用
    "django.contrib.admin",
    # 认证应用
    "django.contrib.auth",
    # 将这些模型与特定的内容类型关联起来，以便可以在应用程序中使用它们。
    "django.contrib.contenttypes",
    # 启用Django的会话（session）功能
    "django.contrib.sessions",
    #一个用于处理用户会话的应用程序。
    "django.contrib.messages",
    #一个用于处理静态文件的的应用程序。
    "django.contrib.staticfiles",

    # 注册apps下子应用的user，用户模块
    'users',  # 用户模块
    'contents', # 首页广告模块
    'verifications', # 验证码模块
]


#Django用户模型类是通过全局配置项 AUTH_USER_MODEL 决定的
# 指定自定义用户的模型类  值的语法：AUTH_USER_MODEL = "myapp.MyUser"
AUTH_USER_MODEL = "users.User"



# 中间件是位于服务器和客户端之间的一个代码模块，它可以对请求和响应进行处理。伴随触发的事件，中间件会执行一些操作。
# 在Django中，中间件通常用于处理请求和响应、拦截请求和响应等。
'''
注意：中间件的顺序很重要，因为它们按照从上到下的顺序执行。在请求视图被处理后，中间件按照从下到上的顺序执行。
可以自己编写中间件，范例在middleware.py文件中
'''
MIDDLEWARE = [
    # 用于防止跨站脚本攻击（XSS）、跨站请求伪造（CSRF）等安全问题。
    "django.middleware.security.SecurityMiddleware",
    # 用于处理请求和响应的会话。
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 用于处理一些通用的请求处理，例如处理请求头、请求方法等。
    "django.middleware.common.CommonMiddleware",
    # 这是因为Django框架在处理POST请求时，会检测CSRF令牌。如果没有检测到CSRF令牌，它会返回一个403 Forbidden错误。
    # "django.middleware.csrf.CsrfViewMiddleware",
    #  认证中间件，用于处理用户认证。
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 消息中间件，用于处理用户消息。
    "django.contrib.messages.middleware.MessageMiddleware",
    # X-Frame-Options中间件，用于防止点击劫持。
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF 工程url的配置入口
# 项目的 URL 配置。Django 将使用它来查找 URL 映射。
# 可以修改，默认不修改
ROOT_URLCONF = "shop.urls"


# 告诉模板路径
TEMPLATES = [
    # jinja2模板，次序不能变动，否则报错，先jinja2后，django模板
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [BASE_DIR / 'templates'],  # 配置模板文件加载路径
        "APP_DIRS": True,  # Jinja2 引擎会在安装的应用程序的 jinja2 子目录中查找模板。
        "OPTIONS": {
            # 'environment':'jinja2.Environment',  # 默认为 'jinja2.Environment'。
            "environment": "shop.utils.jinja2_env.jinja2_environment",  # 一定要设置，指向一个返回 Jinja2 环境的可调用对象。
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    # Django模板，若注释因为这个admin子应用需要
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 模板路径
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # 用于在模板中添加debug对象。
                "django.template.context_processors.debug",
                # 用于在模板中添加request对象。
                "django.template.context_processors.request",
                # 用于在模板中添加auth对象。
                "django.contrib.auth.context_processors.auth",
                # 用于在模板中添加messages对象。
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 定义WSGI_APPLICATION变量，其值为shop.wsgi.application
WSGI_APPLICATION = "shop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'HOST': '127.0.0.1',  # 主机
        'PORT': '3306',  # 端口号
        'USER': 'shop',  # 用户名
        'PASSWORD': '123456',  # 密码
        'NAME': 'shop',  # 指定数据库
    },
}

# Django 默认可以使用任何 cache backend 作为 session backend,
# 将 django-redis 作为 session 储存后端不用安装任何额外的 backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# redis分库缓存
CACHES = {
    "default": {
        # 缓存后端
        "BACKEND": "django_redis.cache.RedisCache",
        # 缓存地址
        "LOCATION": "redis://127.0.0.1:6379/0",
        # 缓存配置
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456"
        }
    },
    # session缓存
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456"
        }
    },
    # 存储验证码VerifyCode
    "VerifyCode": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456"
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# 配置Django中的密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        # 这个验证器会检查用户密码是否与用户的其他属性（如用户名、邮箱等）相似。如果相似，则可能会存在安全风险，因此会拒绝保存这个密码。
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # 检查用户密码的长度是否符合要求。Django默认要求密码长度至少为8个字符。
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # 检查用户密码是否是常见的弱密码。
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # 检查用户密码是否全部由数字组成。
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# 语言和时区设置
LANGUAGE_CODE = "zh-hans"
# 语言代码
TIME_ZONE = "Asia/Shanghai"
# 时区，当 USE_I18N 为 True 时，Django 会将国际化支持（如多语言URL和静态文件翻译）启用
USE_I18N = True
# 控制 Django 是否使用本地时间
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_URL访问静态文件的URL前缀
# 就是我们访问资源http://ip:port/static/后面的路径
STATIC_URL = "static/"
STATICFILES_DIRS = [
    # 方法一
    os.path.join(BASE_DIR, 'static'),
    # 方法二
    # BASE_DIR / 'static'
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# 默认主键类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 配置工程日志
LOGGING = {
    "version": 1, #
    "disable_existing_loggers": False, # 不禁用已经存在的日志记录器
    "formatters": {
        "verbose": {
            # 它描述了每个日志行要输出的细节。
            # {levelname}：日志级别，例如 DEBUG、INFO、WARNING、ERROR 和 CRITICAL。
            # {asctime}：日志时间，格式为 YYYY-MM-DD HH:MM:SS,fff，其中 fff 是毫秒。
            # {module}：模块名，即日志消息所在的模块。
            # {lineno}：行号，即日志消息所在的行号。
            # {process:d}：进程号，整数类型。
            # {thread:d}：线程号，整数类型。
            # {message}：日志消息，即日志记录的内容。
            "format": "日志级别:{levelname},日志时间:{asctime},模块名:{module},lineno:{lineno}-进程号:{process:d}-线程号:{thread:d},日志消息:{message}",
            # 样式
            "style": "{",
        },
        # simple，输出日志级别名称（如 DEBUG）和日志信息。
        "simple": {
            "format": "日志级别:{levelname},日志时间:{asctime},模块名:{module},lineno:{lineno},日志消息:{message}",
            "style": "{",
        },
    },
    "filters": {  # 对日志进行过滤
        # Debug模式为True时，才会记录日志。
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": { # 日志处理方法
        "console": { # 向终端中输出日志
            "level": "INFO", # 有多种处理方式等级，如DEBUG、INFO、WARNING、ERROR、CRITICAL
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/shop.log'),   # 日志文件的位置，
            'maxBytes': 300 * 1024 * 1024, # 日志文件的最大大小,这里设置为300M
            # 保留的日志文件的个数，若满的话新建一个文件
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    "loggers": {  # 日志器
        "django": {# django的日志器
            "handlers": ['console', 'file'], # 处理方法
            "propagate": True,# 是否传递给父日志器
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
        # 定义了一个名为verifications的日志器,监控子应用verifications
        'verifications': {
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        # 定义了一个名为users的日志器,监控子应用users
        'users': {
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        # 定义了一个名为carts的日志器
        'carts': {
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
    },
}