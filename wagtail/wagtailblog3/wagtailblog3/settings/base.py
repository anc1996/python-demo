"""
Django settings for wagtailblog3 project.

由 'django-admin startproject' 使用 Django 5.1.7 生成。
"""

# 在项目中构建路径，如下所示： os.path.join（BASE_DIR， ...）
import os

# 当前文件的目录,/xxx/xx/wagtailblog3/wagtailblog3
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_DIR)

# 项目的根目录:/xx/xx/wagtailblog3
BASE_DIR = os.path.dirname(PROJECT_DIR)

# 应用定义
# 应用定义
INSTALLED_APPS = [
    "home",  # 首页应用
    "search",  # 搜索应用
    "blog",  # 添加博客应用
    "comments", # 添加评论系统
    "archive",  # 添加归档应用
    "base", # 添加基础应用
    "portfolio", # 添加作品集应用
    
    # 第三方应用
    "storages",  # 添加 Django Storages
    
    "wagtailmarkdown",
    "wagtailmedia",
    "rest_framework",  # Django REST Framework
    "rest_framework_simplejwt",  # JWT 认证
    "drf_yasg",  # API 文档生成
    "corsheaders",  # 如果需要跨域支持
    "wagtail_modeladmin", # Wagtail ModelAdmin,模块允许您将项目中的任何模型添加到 Wagtail 管理界面
    
    "wagtail.contrib.forms",  # Wagtail 表单贡献模块
    "wagtail.contrib.redirects",  # Wagtail 重定向贡献模块
    "wagtail.contrib.table_block",  # Wagtail 表格块模块
    "wagtail.contrib.search_promotions",  # 添加搜索推广功能
    "wagtail.contrib.settings",  #保存所有网页通用设置的模型
    "wagtail.embeds",  # Wagtail 嵌入内容模块
    "wagtail.sites",  # Wagtail 站点管理模块
    "wagtail.users",  # Wagtail 用户管理模块
    "wagtail.snippets",  # Wagtail 代码片段模块
    "wagtail.documents",  # Wagtail 文档管理模块
    "wagtail.images",  # Wagtail 图片管理模块
    "wagtail.search",  # Wagtail 搜索模块
    "wagtail.admin",  # Wagtail 管理后台模块
    "wagtail",  # Wagtail 核心模块
    "modelcluster",  # Django 模型集群模块
    "taggit",  # Django 标签模块
    "django.contrib.admin",  # Django 管理后台模块
    "django.contrib.auth",  # Django 认证模块
    "django.contrib.contenttypes",  # Django 内容类型模块
    "django.contrib.sessions",  # Django 会话模块
    "django.contrib.messages",  # Django 消息模块
    "django.contrib.staticfiles",  # Django 静态文件模块
]

MIDDLEWARE = [
    'blog.middleware.PageViewMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",  # 处理会话数据，确保每个请求都有会话功能
    "django.middleware.common.CommonMiddleware",  # 处理常见的HTTP功能，如URL重写、主机验证等
    "django.middleware.csrf.CsrfViewMiddleware",  # 提供CSRF保护，防止跨站请求伪造攻击
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 将用户与请求关联，提供request.user对象
    "django.contrib.messages.middleware.MessageMiddleware",  # 启用基于cookie或会话的消息系统
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # 防止点击劫持攻击，添加X-Frame-Options头
    "django.middleware.security.SecurityMiddleware",  # 提供多种安全增强，如HTTPS重定向、XSS保护等
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",  # 处理Wagtail中设置的URL重定向规则
]
ROOT_URLCONF = "wagtailblog3.urls" # 项目的 URL 配置模块

# 模板
TEMPLATES = [  # Django 模板系统配置列表，可配置多个模板引擎
    {  # 主模板引擎配置（通常只配置一个）
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # 使用 Django 内置的模板引擎
        "DIRS": [  # 模板搜索目录列表，Django 会按顺序在这些目录中查找模板
            os.path.join(PROJECT_DIR, "templates"),  # 项目级模板目录，通常放置全站通用模板
        ],
        "APP_DIRS": True,  # 设为 True 时会自动在每个已安装应用的 templates 子目录中查找模板
        "OPTIONS": {  # 模板引擎的附加选项
            "context_processors": [  # 上下文处理器，用于向所有模板添加变量
                "django.template.context_processors.debug",  # 添加 debug 和 sql_queries 变量
                "django.template.context_processors.request",  # 将当前的 request 对象添加到上下文，所以你在模板中可以直接使用 {{ request }}。
                "django.contrib.auth.context_processors.auth",  # 添加 user 变量（当前登录用户）
                "django.contrib.messages.context_processors.messages",  # 添加 messages 变量（消息框架）
                
                "wagtail.contrib.settings.context_processors.settings",# 告诉 Django 模板引擎：“嘿，每次渲染模板的时候，请调用 Wagtail 的这个上下文处理器，把网站的全局设置取出来，放到一个叫做 settings 的变量里，让我在模板里可以直接用。”
            ],
        },
    },
]

"""
wagtail.contrib.settings ：提供的一个上下文处理器。
    1、定义一些网站级别的配置项（例如，社交媒体链接、联系电话、网站名称等），这些配置项不属于某个特定的页面，而是应用于整个网站。
    2、通过 @register_setting 装饰器和继承 BaseGenericSetting 来创建这样的设置模型（就像你创建的 NavigationSettings）。
    
wagtail.contrib.settings.context_processors.settings 的作用：
    在每次渲染模板之前，它会去数据库中查找你通过 wagtail.contrib.settings 定义的所有全局设置（比如 NavigationSettings）。
    然后，它会将这些设置对象打包到一个名为 settings 的变量中，并添加到模板的上下文中。
    这个 settings 变量是一个特殊的结构，你可以通过 settings.app_label.SettingModelName.field_name 的方式来访问具体的设置值。
        例如，你创建的 NavigationSettings 模型在 base 应用中，所以你在模板中可以通过 settings.base.NavigationSettings.linkedin_url 来访问 LinkedIn URL。
"""

# WSGI应用程序
WSGI_APPLICATION = "wagtailblog3.wsgi.application"

# 数据库
# ==========================================================
# MinIO存储配置
AWS_STORAGE_BUCKET_NAME = 'wagtail-softblog-media'
AWS_S3_ENDPOINT_URL = 'http://192.168.20.2:9000'
AWS_ACCESS_KEY_ID = 'admin'
AWS_SECRET_ACCESS_KEY = '12345678'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_VERIFY = False

# MongoDB 配置
MONGO_DB = {
    'NAME': 'wagtailblog',
    'HOST': 'localhost',
    'PORT': 27017,
}

# Redis 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': '123456'
        }
    }
}

# MySQL 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wagtailsoftblog',
        'USER': 'wagtailsoftblog',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_general_ci',
        }
    }
}

# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'  # 使用您的Redis密码
REDIS_DB = 1  # 使用DB 1用于计数器
# ===============================================================

# 密码验证
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [  # 定义密码验证器列表，用于检查用户输入密码的强度和质量
    {
        # 检查密码是否与用户属性过于相似（如用户名、邮箱等），防止使用容易被猜测的相关信息作密码
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # 验证密码长度是否达到最小要求（默认至少8个字符），可通过OPTIONS参数自定义长度
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # 检查是否使用了常见密码（如"password"、"123456"等），基于内置的常见密码列表
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # 检查密码是否仅包含数字，禁止纯数字密码，提高安全性
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 国际化
# https://docs.djangoproject.com/en/5.1/topics/i18n/
# 语言代码，设置为中文简体
LANGUAGE_CODE = "zh-hans"  # 英文为 "en-us"，更改为中文简体

# 时区设置，修改为中国时区
TIME_ZONE = "Asia/Shanghai"  # 默认为 "UTC"，更改为中国时区

# 是否启用 Django 的翻译系统
USE_I18N = True  # True 表示启用国际化功能

# 是否使用时区感知的日期时间
USE_TZ = True  # True 表示数据库存储 UTC 时间，在展示时根据 TIME_ZONE 转换

# 静态文件 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATICFILES_FINDERS = [
    # Django 默认的静态文件查找器
    "django.contrib.staticfiles.finders.FileSystemFinder",
    # Django 默认的应用目录查找器
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# 这个配置定义了静态文件应用在启用 FileSystemFinder 查找器时将穿越的额外位置，
# 例如，如果你使用 collectstatic 或 findstatic 管理命令或使用静态文件服务视图。
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"), # 项目级静态文件目录
]

STATIC_ROOT = os.path.join(BASE_DIR, "static") # 静态文件收集目录
STATIC_URL = "/static/" # 静态文件的 URL 前缀

MEDIA_ROOT = os.path.join(BASE_DIR, "media") # 媒体文件存储目录
MEDIA_URL = "/media/" # 媒体文件的 URL 前缀

# 默认存储设置，以及更新后的静态文件存储。
# 参见 https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "wagtailblog3.storage_backends.MinioMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    "images": {
        "BACKEND": "wagtailblog3.storage_backends.MinioImageStorage",
    },
    "original_images": {
        "BACKEND": "wagtailblog3.storage_backends.MinioOriginalImageStorage",
    },
    "documents": {
        "BACKEND": "wagtailblog3.storage_backends.MinioDocumentStorage",
    },
    # 添加媒体文件存储后端
    "wagtailmedia": {
        "BACKEND": "wagtailblog3.storage_backends.MinioMediaStorage",
    },
}


# Wagtail 自定义模型配置，admin对后台内容进行编辑
WAGTAILDOCS_DOCUMENT_MODEL = 'blog.BlogDocument' # 自定义文档模型
WAGTAILIMAGES_IMAGE_MODEL = 'blog.BlogImage' # 自定义图片模型

# Django 默认将每个表单的最大字段数设置为 1000，但特别复杂的页面模型
# 可能会在 Wagtail 的页面编辑器中超出此限制。
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# Wagtail 设置
WAGTAIL_SITE_NAME = "wagtailblog3"

# 搜索
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtailblog3.search.CustomSearchBackend',
    }
}

# 在 Wagtail 管理后端中引用完整 URL 时使用的基本 URL -
# 例如，在通知电子邮件中。 不要包含 '/admin' 或尾部斜杠
WAGTAILADMIN_BASE_URL = "http://example.com"



# 文档库中允许的文件扩展名。
# 可以省略此项以允许所有文件，但请注意，如果允许不受信任的用户上传文件，
# 参见 https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip','md']


# Wagtail Markdown配置
WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,  # 禁用自动下载Font Awesome图标库
    "allowed_tags": [  # Markdown中允许使用的HTML标签白名单
        'div', 'span', 'p', 'a', 'img', 'pre', 'code', 'br', 'hr',
        'table', 'tr', 'th', 'td', 'thead', 'tbody', 'tfoot',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'del',
        'audio', 'video', 'source'  # 允许音视频标签
    ],
    "allowed_styles": [  # 允许在HTML标签中使用的CSS样式属性
        'color', 'background-color', 'font-family', 'font-weight',
        'text-align', 'width', 'height', 'margin', 'padding'
    ],
    "allowed_attributes": {  # 各HTML标签允许的属性列表
        'a': ['href', 'title', 'target', 'rel'],  # 链接标签属性
        'img': ['src', 'alt', 'title', 'width', 'height', 'loading', 'class'],  # 图片标签属性
        'code': ['class'],  # 代码标签属性
        'pre': ['class'],  # 预格式化文本属性
        'div': ['class', 'id'],  # div容器属性
        'span': ['class', 'id'],  # 行内容器属性
        'table': ['class', 'border', 'cellspacing', 'cellpadding'],  # 表格属性
        'audio': ['controls', 'autoplay', 'loop', 'muted', 'src'],  # 音频标签属性
        'video': ['controls', 'autoplay', 'loop', 'muted', 'width', 'height', 'src'],  # 视频标签属性
        'source': ['src', 'type']  # 媒体源标签属性
    },
    "extensions": [  # 启用的Markdown扩展
        'markdown.extensions.extra',  # 包含表格、围栏代码块等扩展功能
        'markdown.extensions.codehilite',  # 代码高亮
        'markdown.extensions.toc',  # 目录生成
        'markdown.extensions.smarty',  # 智能标点转换
        'markdown.extensions.nl2br',  # 自动将换行符转为<br>标签
        'pymdownx.arithmatex',  # 数学公式支持
        'pymdownx.superfences',  # 增强的围栏代码块
        'pymdownx.details',  # 可折叠详情块
        'pymdownx.tabbed',  # 选项卡内容
        'pymdownx.tasklist',  # 任务列表
        'pymdownx.highlight',  # 代码高亮增强
    ],
    "extension_configs": {  # 扩展的具体配置选项
        "pymdownx.arithmatex": {
            "generic": True  # 使用通用MathJax配置
        },
        # 增强代码高亮配置
        "pymdownx.highlight": {
            "linenums": True,  # 显示代码行号
            "guess_lang": True,  # 自动猜测代码语言
            "pygments_style": "github-dark",  # 使用GitHub暗色主题风格
            "use_pygments": True,  # 启用Pygments引擎
            "css_class": "highlight"  # CSS类名
        },
        "pymdownx.superfences": {
            "custom_fences": [  # 自定义围栏代码块
                {
                    "name": "mermaid", "class": "mermaid",
                    "format": "!!python/name:pymdownx.superfences.fence_div_format"
                }  # 添加Mermaid图表支持
            ]
        }
    }
}


# Wagtail Media配置
WAGTAILMEDIA = {
    "MEDIA_MODEL": "wagtailmedia.Media",  # 使用的媒体模型类
    "AUDIO_EXTENSIONS": [  # 允许上传的音频文件扩展名
        "aac", "aiff", "flac", "m4a", "m4b", "mp3", "ogg", "wav",
    ],
    "VIDEO_EXTENSIONS": [  # 允许上传的视频文件扩展名
        "avi", "h264", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg", "ogv", "webm",
    ],
}

# 添加 REST Framework 配置
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

# 跨域设置 (依赖django-cors-headers包)
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

# Swagger API文档设置
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {  # 安全定义
        'Bearer': {  # JWT Bearer认证
            'type': 'apiKey',  # API密钥类型
            'name': 'Authorization',  # 使用的请求头名称
            'in': 'header'  # 在HTTP头中传递
        }
    }
}