﻿"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import datetime
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
ALLOWED_HOSTS = ['*']

'''
在 Django 设置中配置中间件的行为。您必须至少设置以下三个设置之一：
    CORS_ALLOWED_ORIGINS
    CORS_ALLOWED_ORIGIN_REGEXES
    CORS_ALLOW_ALL_ORIGINS
'''

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:80',
    'http://192.168.20.2:80',
    "http://127.0.0.1:8050",
    "http://192.168.20.2:8050",
    "http://192.168.20.2:8111",
    "http://127.0.0.1:8111",
    "http://192.168.20.2:8051",
    "http://127.0.0.1:8051",
]

# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

# 或者，允许所有来源的跨域请求。
# CORS_ORIGIN_ALLOW_ALL = True

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

    # 导报模块
    "corsheaders",  # 跨域请求
    'haystack',  # 全文检索框架
    'rest_framework', # drf框架
    'django_filters',  # 过滤器
    'drf_yasg',  # drf-yasg(Swagger升级版)

    # 注册apps下子应用的user，用户模块
    'users',  # 用户模块
    'contents', # 首页广告模块
    'verifications', # 验证码模块
    'oauth',# oauth模块注册（第三方登录）：QQ登录、
    'areas', # 省市区三级联动模块
    'goods', # 商品模块
    'carts',# 购物车
    'orders',# 订单模块
    'payment',# 支付模块
    'django_crontab', # 定时任务
    'shop_admin',# 管理员模块
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
    # 要做CommonMiddleware之前，处理跨域资源共享（CORS）的Web应用程序中间件。
    "corsheaders.middleware.CorsMiddleware",
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
    'slave': {  # 读
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 主机
        'PORT': '4306',  # 端口号
        'USER': 'root',  # 用户名
        'PASSWORD': '123456',  # 密码
        'NAME': 'shop',  # 指定数据库
    }
}

# mysql读写分离路由，在执行数据库查询时，将用于确定使用哪个数据库的路由器列表。
DATABASE_ROUTERS = ['shop.utils.db_router.MasterSlaveDBRouter']

# Django 默认可以使用任何 cache backend 作为 session backend,
# 将 django-redis 作为 session 储存后端不用安装任何额外的 backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# redis分库缓存
CACHES = {
    # 默认的Redis配置项，采用0号Redis库。
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
    
    # 存储用户浏览记录history
    "history": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456"
        }
    },
    
    # 购物车
    "carts": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
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
    # os.path.join(BASE_DIR, 'static'),
    # 方法二
    BASE_DIR / 'static'
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# 默认主键类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 配置工程日志
LOGGING = {
    "version": 1, # 日志配置的版本
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
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue", # Debug模式为True时，才会记录日志。
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
            'backupCount': 10, # 日志文件的个数
            'formatter': 'verbose' # 详细日志
        },
    },
    "loggers": {  # 日志器
        "django": { # django的日志器
            "handlers": ['console', 'file'], # 处理方法
            "propagate": True,# 控制日志消息是否传递给父级日志器（Logger）。
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
        # 定义了一个名为verifications的日志器,监控子应用verifications
        'verifications': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为users的日志器,监控子应用users
        'users': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为oauth的日志器,监控子应用oauth
        'oauth': {
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为send_email的日志器
        'send_email': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为areas的日志器
        'areas': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为goods的日志器
        'goods': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 定义了一个名为goods的日志器
        'orders': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # payment支付日志
        'payment': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}


# 指定自定义的用户认证后端，用于多用户登录
# 默认是，Django 会使用 django.contrib.auth.backends.ModelBackend 类来认证用户。
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']

# 判断用户是否登录，指定未登录用户重定向的地址
LOGIN_URL="/login/"

# celery配置
celery_broker_url = 'redis://:123456@127.0.0.1:6379/2'

#
celery_result_backend= 'redis://:123456@127.0.0.1:6379/10'


# 容联云短信
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
accountSid = '8a216da881ad97540181ba09d9b90215'
# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
accountToken = '6202374657f446eab2da5fcbc09f0029'
# 请使用管理控制台首页的APPID或自己创建应用的APPID
appId = '8aaf070881ad8ad40181ba1b34f5025f'

# QQ登录参数
# 申请QQ登录成功后，分配给应用的appid。
QQ_CLIENT_ID = '102016086'
# 申请QQ登录成功后，分配给应用的 appkey 。
QQ_CLIENT_SECRET = 'FPM55xe8PSIuITSE'  # FPM55xe8PSIuITSE
# 成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。
QQ_REDIRECT_URI = 'http://ov-vo.cn/oauth_callback'


# QQ配置邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.qq.com' # 发邮件主机
EMAIL_PORT = 465 # 发邮件端口， smtp.qq.com，使用SSL，端口号465或587
EMAIL_HOST_USER = '834195283@qq.com' # 授权的邮箱
EMAIL_HOST_PASSWORD = 'rahnxfdaywhgbfah' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = 'shop<834195283@qq.com>' # 发件人抬头
EMAIL_USE_SSL = True # 是否使用SSL加密，qq邮箱需要使用
EMAIL_VERIFY_URL = 'http://192.168.20.2/emails/verification/' # 邮箱验证链接

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = "shop.utils.fastdfs.fdfs_storage.FastDFSStorage"
# FDFS客户端的配置文件. 用于指定FDFS客户端的配置文件路径
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')
# FastDFS相关参数
FDFS_BASE_URL = 'http://192.168.20.2:8888/'


# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'URL': 'http://192.168.20.2:9200/', # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'shop', # Elasticsearch建立的索引库的名称
    },
}



# 当添加、修改、删除数据时，自动生成索引,配置项保证了在Django运行起来后，有新的数据产生时，Haystack仍然可以让Elasticsearch实时生成新数据的索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 控制每页显示数量
HAYSTACK_SEARCH_RESULTS_PER_PAGE=20



# 支付宝支付参数
# 应用ID
ALIPAY_APPID = "9021000136698047"
# 调试
ALIPAY_DEBUG = True
# 输出调试数据
ALIPAY_VERBOSE=True
# 支付宝网关
ALIPAY_URL = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://ov-vo.cn/payment/status/'

# 定时任务
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    # * * * * *
    # 分 时 日 月 周
    # 每分钟的第1分钟执行一次generate_static_index_html函数
    ('*/10 * * * *', 'contents.crons.generate_static_index_html', '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log')),
]
# 指定中文编码格式
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

## 添加定时任务到系统中
# $ python manage.py crontab add
# 显示已激活的定时任务
# $ python manage.py crontab show
# 移除定时任务
# $ python manage.py crontab remove


# 配置收集静态文件存放的目录
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'nginx_static')



# 这里是全局配置，如果需要局部配置，可以在视图中配置
REST_FRAMEWORK = {
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # JWT认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 基本认证，此身份验证方案使用 HTTP 基本身份验证，根据用户的用户名和密码进行签名。基本身份验证通常仅适用于测试。
        'rest_framework.authentication.BasicAuthentication',
        # 会话认证，此认证方案使用Django的默认session后端进行身份验证。Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端。
        'rest_framework.authentication.SessionAuthentication',
    ],

    # 权限，可以使用该 DEFAULT_PERMISSION_CLASSES 设置全局设置默认权限策略
    'DEFAULT_PERMISSION_CLASSES': [
        #  第1种权限：API 仅供注册用户访问，则此权限适用。
        'rest_framework.permissions.IsAuthenticated',
        # 第2种权限：如果未指定，则此设置默认为允许不受限制的访问：
        # 'rest_framework.permissions.AllowAny',
        # 第3种：IsAdminUser 权限类将仅供一部分受信任的管理员访问和 user.is_staff True 在这种情况下将允许权限。
        # 'rest_framework.permissions.IsAdminUser',
        # 第4种：IsAuthenticatedOrReadOnly 权限类将允许已经通过身份验证的用户进行任何请求，而未经身份验证的用户只能进行 GET、HEAD 或 OPTIONS 请求。
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    #
    # 全局限流,用于控制客户端可以向 API 发出的请求速率。
    'DEFAULT_THROTTLE_CLASSES': [
        # 只会 AnonRateThrottle 限制未经身份验证的用户。传入请求的 IP 地址用于生成要限制的唯一密钥。
        'rest_framework.throttling.AnonRateThrottle',
        # 只会 UserRateThrottle 限制经过身份验证的用户。传入请求的用户 ID 用于生成要限制的唯一密钥。
        # 注意：未经身份验证的请求将回退到使用传入请求的 IP 地址来生成要限制的唯一密钥。
        'rest_framework.throttling.UserRateThrottle',
        # 限制用户对于每个视图的访问频次，使用ip或user id。例如：对multifunction.otherfeatures.bookview局部限流。
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    # 限流速率
    'DEFAULT_THROTTLE_RATES': {
        # 未经身份验证的用户每天可以进行 100 次请求。
        'anon': '100/day',
        # 经过身份验证的用户每天可以进行 1000 次请求。
        'user': '1000/day',
    },
    #
    # # 全局过滤
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    #
    # # 全局分页器，用的不多
    # # 第1种：此分页样式接受请求查询参数中的单个数字页码。列如：/***/?page=4
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # # 第2种：此分页样式反映了查找多个数据库记录时使用的语法。客户端包括“limit”和“offset”查询参数。该限制表示要返回的最大项目数，与其他样式中的限制相同 page_size 。偏移量表示要跳过的项目数。
    # # 例如：?limit=100&offset=400
    # # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 100,

    # 异常，默认为 REST 框架提供的标准异常处理程序：
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',

    # # 指定用于支持coreapi的Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}


# JWT认证
JWT_AUTH = {
    # JWT指定有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1), # JWT_EXPIRATION_DELTA 指明token的有效期
    # 负责控制登录或刷新后返回的响应数据。当前路径为
    'JWT_RESPONSE_PAYLOAD_HANDLER':'shop_admin.utils.jwt_response_payload_handler',
}

# 上传的配置文件
FASTDFS_PATH=os.path.join(BASE_DIR,'utils/fastdfs/client.conf')