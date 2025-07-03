"""
Django settings for wagtailblog3 project.

由 'django-admin startproject' 使用 Django 5.1.7 生成。
"""

# 在项目中构建路径，如下所示： os.path.join（BASE_DIR， ...）
import os,sys
from django.contrib import messages

# 当前文件的目录,/xxx/xx/wagtailblog3/wagtailblog3
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_DIR)

# 项目的根目录:/xx/xx/wagtailblog3
BASE_DIR = os.path.dirname(PROJECT_DIR)

# ===== 新增：将 apps 目录添加到 Python 路径 =====
# 这样 Django 就能找到移动到 apps 目录下的应用
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))
# ===============================================

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
    'wagtailcodeblock', #  Wagtail CMS 源代码的语法高亮器块
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
    },
    'comment_rate_limit_cache': {  # 新的缓存实例，专门用于评论频率限制
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',  # 使用不同的Redis DB，例如 DB 2
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

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_collected") # 静态文件收集目录
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


# Wagtail Code Block主题
WAGTAIL_CODE_BLOCK_THEME = 'okaidia'

# 启用行号（默认就是True，这里显式写出来方便理解）
WAGTAIL_CODE_BLOCK_LINE_NUMBERS = True

# 启用“复制到剪贴板”按钮（默认也是True）
WAGTAIL_CODE_BLOCK_COPY_TO_CLIPBOARD = True

# Wagtail Code Block配置
WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('abap', 'ABAP'),
    ('abnf', 'Augmented Backus–Naur form'),
    ('actionscript', 'ActionScript'),
    ('ada', 'Ada'),
    ('antlr4', 'ANTLR4'),
    ('apacheconf', 'Apache Configuration'),
    ('apl', 'APL'),
    ('applescript', 'AppleScript'),
    ('aql', 'AQL'),
    ('arduino', 'Arduino'),
    ('arff', 'ARFF'),
    ('asciidoc', 'AsciiDoc'),
    ('asm6502', '6502 Assembly'),
    ('aspnet', 'ASP.NET (C#)'),
    ('autohotkey', 'AutoHotkey'),
    ('autoit', 'AutoIt'),
    ('bash', 'Bash + Shell'),
    ('basic', 'BASIC'),
    ('batch', 'Batch'),
    ('bison', 'Bison'),
    ('bnf', 'Backus–Naur form + Routing Backus–Naur form'),
    ('brainfuck', 'Brainfuck'),
    ('bro', 'Bro'),
    ('c', 'C'),
    ('clike', 'C-like'),
    ('cmake', 'CMake'),
    ('csharp', 'C#'),
    ('cpp', 'C++'),
    ('cil', 'CIL'),
    ('coffeescript', 'CoffeeScript'),
    ('clojure', 'Clojure'),
    ('crystal', 'Crystal'),
    ('csp', 'Content-Security-Policy'),
    ('css', 'CSS'),
    ('css-extras', 'CSS Extras'),
    ('d', 'D'),
    ('dart', 'Dart'),
    ('diff', 'Diff'),
    ('django', 'Django/Jinja2'),
    ('dns-zone-file', 'DNS Zone File'),
    ('docker', 'Docker'),
    ('ebnf', 'Extended Backus–Naur form'),
    ('eiffel', 'Eiffel'),
    ('ejs', 'EJS'),
    ('elixir', 'Elixir'),
    ('elm', 'Elm'),
    ('erb', 'ERB'),
    ('erlang', 'Erlang'),
    ('etlua', 'Embedded LUA Templating'),
    ('fsharp', 'F#'),
    ('flow', 'Flow'),
    ('fortran', 'Fortran'),
    ('ftl', 'Freemarker Template Language'),
    ('gcode', 'G-code'),
    ('gdscript', 'GDScript'),
    ('gedcom', 'GEDCOM'),
    ('gherkin', 'Gherkin'),
    ('git', 'Git'),
    ('glsl', 'GLSL'),
    ('gml', 'GameMaker Language'),
    ('go', 'Go'),
    ('graphql', 'GraphQL'),
    ('groovy', 'Groovy'),
    ('haml', 'Haml'),
    ('handlebars', 'Handlebars'),
    ('haskell', 'Haskell'),
    ('haxe', 'Haxe'),
    ('hcl', 'HCL'),
    ('http', 'HTTP'),
    ('hpkp', 'HTTP Public-Key-Pins'),
    ('hsts', 'HTTP Strict-Transport-Security'),
    ('ichigojam', 'IchigoJam'),
    ('icon', 'Icon'),
    ('inform7', 'Inform 7'),
    ('ini', 'Ini'),
    ('io', 'Io'),
    ('j', 'J'),
    ('java', 'Java'),
    ('javadoc', 'JavaDoc'),
    ('javadoclike', 'JavaDoc-like'),
    ('javascript', 'JavaScript'),
    ('javastacktrace', 'Java stack trace'),
    ('jolie', 'Jolie'),
    ('jq', 'JQ'),
    ('jsdoc', 'JSDoc'),
    ('js-extras', 'JS Extras'),
    ('js-templates', 'JS Templates'),
    ('json', 'JSON'),
    ('jsonp', 'JSONP'),
    ('json5', 'JSON5'),
    ('julia', 'Julia'),
    ('keyman', 'Keyman'),
    ('kotlin', 'Kotlin'),
    ('latex', 'LaTeX'),
    ('less', 'Less'),
    ('lilypond', 'Lilypond'),
    ('liquid', 'Liquid'),
    ('lisp', 'Lisp'),
    ('livescript', 'LiveScript'),
    ('lolcode', 'LOLCODE'),
    ('lua', 'Lua'),
    ('makefile', 'Makefile'),
    ('markdown', 'Markdown'),
    ('markup', 'Markup + HTML + XML + SVG + MathML'),
    ('markup-templating', 'Markup templating'),
    ('matlab', 'MATLAB'),
    ('mel', 'MEL'),
    ('mizar', 'Mizar'),
    ('monkey', 'Monkey'),
    ('n1ql', 'N1QL'),
    ('n4js', 'N4JS'),
    ('nand2tetris-hdl', 'Nand To Tetris HDL'),
    ('nasm', 'NASM'),
    ('nginx', 'nginx'),
    ('nim', 'Nim'),
    ('nix', 'Nix'),
    ('nsis', 'NSIS'),
    ('objectivec', 'Objective-C'),
    ('ocaml', 'OCaml'),
    ('opencl', 'OpenCL'),
    ('oz', 'Oz'),
    ('parigp', 'PARI/GP'),
    ('parser', 'Parser'),
    ('pascal', 'Pascal + Object Pascal'),
    ('pascaligo', 'Pascaligo'),
    ('pcaxis', 'PC Axis'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('phpdoc', 'PHPDoc'),
    ('php-extras', 'PHP Extras'),
    ('plsql', 'PL/SQL'),
    ('powershell', 'PowerShell'),
    ('processing', 'Processing'),
    ('prolog', 'Prolog'),
    ('properties', '.properties'),
    ('protobuf', 'Protocol Buffers'),
    ('pug', 'Pug'),
    ('puppet', 'Puppet'),
    ('pure', 'Pure'),
    ('python', 'Python'),
    ('q', 'Q (kdb+ database)'),
    ('qore', 'Qore'),
    ('r', 'R'),
    ('jsx', 'React JSX'),
    ('tsx', 'React TSX'),
    ('renpy', 'Ren\'py'),
    ('reason', 'Reason'),
    ('regex', 'Regex'),
    ('rest', 'reST (reStructuredText)'),
    ('rip', 'Rip'),
    ('roboconf', 'Roboconf'),
    ('robot-framework', 'Robot Framework'),
    ('ruby', 'Ruby'),
    ('rust', 'Rust'),
    ('sas', 'SAS'),
    ('sass', 'Sass (Sass)'),
    ('scss', 'Sass (Scss)'),
    ('scala', 'Scala'),
    ('scheme', 'Scheme'),
    ('shell-session', 'Shell Session'),
    ('smalltalk', 'Smalltalk'),
    ('smarty', 'Smarty'),
    ('solidity', 'Solidity (Ethereum)'),
    ('sparql', 'SPARQL'),
    ('splunk-spl', 'Splunk SPL'),
    ('sqf', 'SQF: Status Quo Function (Arma 3)'),
    ('sql', 'SQL'),
    ('soy', 'Soy (Closure Template)'),
    ('stylus', 'Stylus'),
    ('swift', 'Swift'),
    ('tap', 'TAP'),
    ('tcl', 'Tcl'),
    ('textile', 'Textile'),
    ('toml', 'TOML'),
    ('tt2', 'Template Toolkit 2'),
    ('twig', 'Twig'),
    ('typescript', 'TypeScript'),
    ('t4-cs', 'T4 Text Templates (C#)'),
    ('t4-vb', 'T4 Text Templates (VB)'),
    ('t4-templating', 'T4 templating'),
    ('vala', 'Vala'),
    ('vbnet', 'VB.Net'),
    ('velocity', 'Velocity'),
    ('verilog', 'Verilog'),
    ('vhdl', 'VHDL'),
    ('vim', 'vim'),
    ('visual-basic', 'Visual Basic'),
    ('wasm', 'WebAssembly'),
    ('wiki', 'Wiki markup'),
    ('xeora', 'Xeora + XeoraCube'),
    ('xojo', 'Xojo (REALbasic)'),
    ('xquery', 'XQuery'),
    ('yaml', 'YAML'),
    ('zig', 'Zig'),
)


# Wagtail Markdown配置
# wagtailblog3/settings/base.py
WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,
    "allowed_tags": [
        'div', 'span', 'p', 'a', 'img', 'pre', 'code', 'br', 'hr',
        'table', 'tr', 'th', 'td', 'thead', 'tbody', 'tfoot',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'del',
        'audio', 'video', 'source',
        # --- 添加以下三个标签 ---
        'ul', 'ol', 'li',
    ],
    "allowed_styles": [
        'color', 'background-color', 'font-family', 'font-weight',
        'text-align', 'width', 'height', 'margin', 'padding'
    ],
    "allowed_attributes": {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height', 'loading', 'class'],
        'code': ['class'],
        'pre': ['class'],
        'div': ['class', 'id'],
        'span': ['class', 'id'],
        'table': ['class', 'border', 'cellspacing', 'cellpadding'],
        'audio': ['controls', 'autoplay', 'loop', 'muted', 'src'],
        'video': ['controls', 'autoplay', 'loop', 'muted', 'width', 'height', 'src'],
        'source': ['src', 'type'],
        # --- (可选) 为 <ul> 和 <ol> 添加 class 属性支持 ---
        'ul': ['class'],
        'ol': ['class'],
    },
    "extensions": [
        'markdown.extensions.extra',
        "markdown.extensions.fenced_code",
        'markdown.extensions.toc',
        'markdown.extensions.smarty',
        'markdown.extensions.nl2br',
        "markdown.extensions.sane_lists",
        'pymdownx.arithmatex',
        'pymdownx.superfences',
        'pymdownx.details',
        'pymdownx.tabbed',
        'pymdownx.tasklist',
        'pymdownx.highlight',
    ],
    "extension_configs": {
        "pymdownx.arithmatex": {
            "generic": True
        },
        "pymdownx.highlight": {
            "linenums": True,
            "guess_lang": True,
            "pygments_style": "github-dark",
            "use_pygments": True,
            "css_class": "highlight"
        },
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "mermaid", "class": "mermaid",
                    "format": "!!python/name:pymdownx.superfences.fence_div_format"
                }
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

# ===============================================================
# Celery 异步任务队列配置
# ===============================================================

# Celery 基础配置
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Celery 消息代理和结果后端配置
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3'

# Celery 序列化配置
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

# Celery 任务执行配置
CELERY_TASK_ALWAYS_EAGER = False  # 生产环境设为False，开发时可设为True进行测试
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True

# Celery 任务路由和队列配置
CELERY_TASK_ROUTES = {
    # 邮件发送任务使用email队列
    'base.tasks.send_form_confirmation_email': {'queue': 'email'},
    'base.tasks.send_admin_notification_email': {'queue': 'email'},
    'base.tasks.send_bulk_email': {'queue': 'email'},
    # 清理任务使用maintenance队列
    'base.tasks.cleanup_email_logs': {'queue': 'maintenance'},
}

# 定义队列配置
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'direct',
        'routing_key': 'default',
    },
    'email': {
        'exchange': 'email',
        'exchange_type': 'direct',
        'routing_key': 'email',
    },
    'maintenance': {
        'exchange': 'maintenance',
        'exchange_type': 'direct',
        'routing_key': 'maintenance',
    },
}

# Celery 任务重试和超时配置
CELERY_TASK_DEFAULT_RETRY_DELAY = 60  # 默认重试延迟60秒
CELERY_TASK_MAX_RETRIES = 3  # 最大重试次数
CELERY_TASK_SOFT_TIME_LIMIT = 300  # 软时间限制（5分钟）
CELERY_TASK_TIME_LIMIT = 600  # 硬时间限制（10分钟）

# Celery 结果过期时间
CELERY_RESULT_EXPIRES = 3600  # 1小时后过期

# Celery 错误处理配置
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_IGNORE_RESULT = False

# Celery 监控配置
CELERY_SEND_TASK_EVENTS = True
CELERY_SEND_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# Celery Beat 定时任务配置（可选）
CELERY_BEAT_SCHEDULE = {
    # 每天凌晨2点清理邮件日志
    'cleanup-email-logs': {
        'task': 'base.tasks.cleanup_email_logs',
        'schedule': 60 * 60 * 24,  # 24小时
        'options': {'queue': 'maintenance'}
    },
}

# ===============================================================
# 邮件发送频率限制配置
# ===============================================================

# 启用邮件发送频率限制
EMAIL_RATE_LIMIT_ENABLED = True

# 全局邮件发送频率限制时间（秒）- 默认5分钟
EMAIL_RATE_LIMIT_SECONDS = 300

# 针对特定表单页面的个性化频率限制配置
# 格式：{表单页面ID: 限制时间（秒）}
EMAIL_RATE_LIMIT_PER_FORM = {
    # 示例：表单ID为1的页面设置为3分钟限制
    # 1: 180,
    # 表单ID为2的页面设置为10分钟限制
    # 2: 600,
}

# ===============================================================
# 邮件发送增强配置
# ===============================================================
# QQ邮箱SMTP配置（推荐配置）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = '834195283@qq.com'
EMAIL_HOST_PASSWORD =  'rahnxfdaywhgbfah'
DEFAULT_FROM_EMAIL = '834195283@qq.com'

# 表单设置
WAGTAILFORMS_CONFIRMATION_EMAIL_TEMPLATE = 'emails/form_confirmation.html'


# 邮件发送相关设置
EMAIL_TIMEOUT = 30  # 邮件发送超时时间（秒）
EMAIL_MAX_RECIPIENTS = 50  # 单封邮件最大收件人数量

# 异步邮件发送开关（可在管理后台动态控制）
ASYNC_EMAIL_ENABLED = True

# 邮件发送统计和日志配置
EMAIL_LOGGING_ENABLED = True
EMAIL_STATS_ENABLED = True

# 消息框架设置（用于表单反馈）
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# 表单邮件发送配置
FORM_EMAIL_SETTINGS = {
    'CONFIRMATION_EMAIL_ENABLED': True,
    'ADMIN_NOTIFICATION_ENABLED': True,
    'DEFAULT_PRIORITY': 'normal',
    'RETRY_ATTEMPTS': 3,
    'RETRY_DELAY': 60,
}

# ===============================================================
# 评论系统配置

# 评论频率限制设置
COMMENT_RATE_LIMIT = {
    'ENABLED': True,
    'INTERVAL_SECONDS': 60, # 1分钟
    'MAX_COMMENTS': 3,      # 1分钟内最多3条评论
    'CACHE_ALIAS': 'comment_rate_limit_cache', # 指定用于频率限制的缓存别名
}
