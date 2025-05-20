"""
wagtaildata 项目的 Django 设置。

由 'django-admin startproject' 使用 Django 5.1.7 生成。

有关此文件的更多信息，请参见
https://docs.djangoproject.com/en/5.1/topics/settings/

完整的设置列表及其值，请参见
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# 构建项目内的路径，如: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# 快速启动开发设置 - 不适合生产环境
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# 应用定义
INSTALLED_APPS = [
    "home",
    "search",
    "blog",  # 添加blog应用
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",  # 添加Django存储后端
    "django_redis",  # 添加Redis缓存支持
]

# 中间件配置
MIDDLEWARE = [
    'blog.middleware.DisableProxyMiddleware',  # 处理代理中间件
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# URL配置
ROOT_URLCONF = "wagtaildata.urls"

# 模板配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # 使用Django内置的模板引擎
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),  # 指定项目级别模板文件的搜索路径
        ],
        "APP_DIRS": True,  # 允许Django在每个已安装应用的templates子目录中查找模板
        "OPTIONS": {
            "context_processors": [  # 上下文处理器列表，用于向模板添加额外的变量
                "django.template.context_processors.debug",  # 添加debug变量，表示是否处于调试模式
                "django.template.context_processors.request",  # 将request对象添加到模板上下文
                "django.contrib.auth.context_processors.auth",  # 添加与认证系统相关的变量，如当前用户
                "django.contrib.messages.context_processors.messages",  # 添加消息框架的变量
            ],
        },
    },
]

# WSGI配置
WSGI_APPLICATION = "wagtaildata.wsgi.application"


# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wagtaildata',
        'USER': 'wagtaildata',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_general_ci',
            'unix_socket': '/tmp/mysql.sock',
        }
    }
}

# 其他数据库配置
# MongoDB配置
import pymongo

MONGO_DB = {
    'NAME': 'wagtaildata-mongo',
    'HOST': 'localhost',
    'PORT': 27017,
}

# 创建MongoDB连接
mongo_client = pymongo.MongoClient(
    host=MONGO_DB['HOST'],
    port=MONGO_DB['PORT']
)
mongo_db = mongo_client[MONGO_DB['NAME']]

# Redis缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "PASSWORD": "123456"
        }
    }
}

# 为不同类型的数据选择不同的存储方式
# 1. 基本模型数据 -> MySQL (通过Django ORM)
# 2. 大型内容数据 -> MongoDB (通过utils.py中的函数)
# 3. 缓存数据 -> Redis (通过Django缓存框架)
# 4. 媒体文件 -> MinIO (通过Django存储框架)

# 密码验证
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # 检查密码与用户的属性（如用户名、名字、邮箱等）是否相似，避免使用容易猜测的密码
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # 检查密码是否达到最小长度要求（默认为8个字符）
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # 检查密码是否是常见密码（如'password'、'123456'等），避免使用容易猜测的密码
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # 检查密码是否仅包含数字，避免使用纯数字密码
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# 国际化设置
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# 设置语言代码，改为中文简体
LANGUAGE_CODE = "zh-hans"  # 原为 "en-us"，现改为中文简体

# 设置时区，改为上海（北京）时区
TIME_ZONE = "Asia/Shanghai"  # 原为 "UTC"，现改为中国标准时间

# 启用Django的翻译系统
USE_I18N = True  # 如果设置为False，Django将不会翻译任何内容

# 启用时区支持，让Django存储所有日期时间为UTC，并在需要时转换为TIME_ZONE设置的时区
USE_TZ = True  # 建议在跨时区应用中保持为True

# 静态文件（CSS、JavaScript、图像）
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATICFILES_FINDERS = [
    # 在文件系统中查找静态文件的查找器，使用STATICFILES_DIRS中指定的路径
    "django.contrib.staticfiles.finders.FileSystemFinder",
    # 在已安装应用的static目录中查找静态文件的查找器
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    # 指定项目级静态文件目录，这里指向项目根目录下的static文件夹
    # 在开发过程中，Django会从这个目录中提供静态文件
    os.path.join(PROJECT_DIR, "static"),
]

# Elasticsearch自动更新配置
WAGTAILSEARCH_HITS_MAX_AGE = 14  # 搜索结果缓存的天数

# MinIO存储配置
AWS_STORAGE_BUCKET_NAME = 'wagtail-blog-media' # MinIO存储桶名称
AWS_S3_ENDPOINT_URL = 'http://192.168.20.2:9000'  # MinIO服务器地址
AWS_ACCESS_KEY_ID = 'admin'  # MinIO访问密钥
AWS_SECRET_ACCESS_KEY = '12345678'  # MinIO秘密密钥
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400', # 缓存控制
}
AWS_QUERYSTRING_AUTH = False # 禁用查询字符串身份验证
AWS_S3_FILE_OVERWRITE = False # 不覆盖同名文件
AWS_DEFAULT_ACL = 'public-read' # 设置默认ACL为公开读取
AWS_S3_VERIFY = False  # 本地开发不验证SSL

# 额外设置，解决上传问题
AWS_S3_REGION_NAME = 'zh-CN'  # 使用MinIO服务器的区域
AWS_S3_ADDRESSING_STYLE = 'path'  # 使用路径样式寻址
AWS_S3_SIGNATURE_VERSION = 's3v4'  # 使用S3v4签名版本

# 确保S3客户端不使用代理
AWS_S3_USE_SSL = True  # 或False，取决于你的MinIO配置
AWS_S3_PROXY = None  # 明确禁用代理
AWS_S3_CONFIG = {
    'proxies': {
        'http': None, # 禁用HTTP代理
        'https': None, # 禁用HTTPS代理
    },
}

# 使用自定义S3存储类
DEFAULT_FILE_STORAGE = 'blog.utils.CustomS3Boto3Storage'

# 确保Wagtail使用相同的存储类
WAGTAILIMAGES_STORAGE = DEFAULT_FILE_STORAGE # Wagtail图像存储
WAGTAILDOCS_STORAGE = DEFAULT_FILE_STORAGE # Wagtail文档存储

# 缓存设置 - 使用Redis作为缓存后端
CACHE_MIDDLEWARE_SECONDS = 3600  # 页面缓存时间（秒）

STATIC_ROOT = os.path.join(BASE_DIR, "static") # 静态文件收集目录
STATIC_URL = "/static/" # 静态文件URL前缀

MEDIA_ROOT = os.path.join(BASE_DIR, "media") # 媒体文件存储目录
MEDIA_URL = "/media/"  # Django会通过存储后端解析实际URL

# 更新STORAGES配置
STORAGES = {
    'default': {
        'BACKEND': 'blog.utils.CustomS3Boto3Storage',
        'OPTIONS': {
            'bucket_name': AWS_STORAGE_BUCKET_NAME, # 存储桶名称
            'access_key': AWS_ACCESS_KEY_ID, # 访问密钥
            'secret_key': AWS_SECRET_ACCESS_KEY, # 秘密密钥
            'endpoint_url': AWS_S3_ENDPOINT_URL, # MinIO服务器地址
            'verify': AWS_S3_VERIFY, # 是否验证SSL
            'region_name': AWS_S3_REGION_NAME, # 区域名称
        },
    },
    'staticfiles': {
        # 使用Django的ManifestStaticFilesStorage来处理静态文件版本控制
        'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    },
}

# Django 默认为每个表单设置最多 1000 个字段，但特别复杂的页面模型
# 可以在 Wagtail 的页面编辑器中超过此限制。
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# Wagtail设置
WAGTAIL_SITE_NAME = "wagtaildata"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
# 数据库搜索（默认）
# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.search.backends.database',
#     }
# }

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'blog.search_backend.HybridSearchBackend',
    }
}

# 当启用Elasticsearch时，使用以下配置替换上面的默认配置
# WAGTAILSEARCH_BACKENDS = {
#     'default': {  # 默认搜索后端的配置
#         'BACKEND': 'wagtail.search.backends.elasticsearch7',  # 使用Elasticsearch 7作为搜索引擎后端
#         'URLS': ['http://127.0.0.1:9200'],  # Elasticsearch服务器的URL地址
#         'INDEX': 'wagtaildata',  # Elasticsearch中索引的名称
#         'TIMEOUT': 5,  # 连接Elasticsearch的超时时间（秒）
#         'OPTIONS': {
#             'verify_certs': False,  # 不验证SSL证书（开发环境使用，生产环境应设为True）
#             'max_retries': 2,  # 连接失败时的最大重试次数
#         },
#         'INDEX_SETTINGS': {  # 索引的具体设置
#             'settings': {
#                 'index': {
#                     'query': {
#                         'default_field': '_all'  # 设置搜索时默认搜索所有字段
#                     }
#                 },
#                 'analysis': {  # 分析器设置
#                     'analyzer': {
#                         'default': {  # 默认分析器配置
#                             'type': 'custom',  # 使用自定义类型
#                             'tokenizer': 'standard',  # 使用标准分词器
#                             'filter': ['lowercase', 'asciifolding']  # 过滤器：转小写和ASCII折叠（去除重音符号）
#                         }
#                     }
#                 }
#             },
#             'mappings': {  # 字段映射配置
#                 'properties': {
#                     'pk': {'type': 'keyword', 'store': True},  # 主键字段，keyword类型，存储原始值
#                     'path': {'type': 'keyword', 'store': True},  # 路径字段，keyword类型，存储原始值
#                     'depth': {'type': 'integer', 'store': True}  # 深度字段，整数类型，存储原始值
#                 }
#             }
#         }
#     }
# }

# Wagtail富文本编辑器设置
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        # 使用Draftail富文本编辑器
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                'h2', 'h3', 'h4', 'h5', 'h6', # 标题
                'bold', 'italic', 'strikethrough', 'code', # 文本样式：加粗、斜体、删除线、代码
                'ol', 'ul', 'hr',# 有序列表、无序列表、水平线
                'link', 'document-link', 'image',# 链接、文档链接、图片
                'embed', # 嵌入
                'blockquote', 'code-block', 'math-formula', 'markdown',# 引用、代码块、数学公式、Markdown
            ]
        }
    },
}

# 启用博客草稿和版本控制
WAGTAIL_WORKFLOW_ENABLED = True

LOGGING = {
    'version': 1,                         # 日志配置版本，目前只有版本1可用
    'disable_existing_loggers': False,    # 是否禁用已存在的日志器，设置为False保留其他日志器的配置
    'handlers': {                         # 定义日志处理器
        'console': {                      # 控制台日志处理器
            'class': 'logging.StreamHandler',  # 使用StreamHandler将日志输出到控制台
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/search.log'),
        },
    },
    'loggers': {                          # 定义日志记录器
        # 'django': {                       # Django框架的日志记录器
        #     'handlers': ['console'],      # 使用控制台处理器
        #     'level': 'INFO',              # 只记录INFO及更高级别的日志
        # },
        # 'botocore': {                     # AWS SDK的日志记录器，用于S3/MinIO操作调试
        #     'handlers': ['console'],      # 使用控制台处理器
        #     'level': 'DEBUG',             # 记录所有DEBUG及更高级别的日志，便于调试存储问题
        # },
        'blog.search_backend': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'blog.utils': {                   # 博客工具模块的日志记录器
            'handlers': ['console'],      # 使用控制台处理器
            'level': 'DEBUG',             # 记录所有DEBUG及更高级别的日志，便于调试博客功能
        },
        'blog.search': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 在 Wagtail 管理后端中引用完整 URL 时使用的基本 URL -
# 例如，在通知电子邮件中。不要包含“/admin”或尾部斜杠
WAGTAILADMIN_BASE_URL = "http://example.com"

# 文档库中文档允许的文件扩展名。
# 可以省略此选项以允许所有文件，但请注意，这可能会带来安全风险
# 如果允许不受信任的用户上传文件 -
# 查看 https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']
