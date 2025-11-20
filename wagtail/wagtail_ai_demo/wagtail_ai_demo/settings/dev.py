from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wa$vqulfuq#gt@^r3@6-80*lldjm$q624f!n9r$7rkl$ns583@"

# SECURITY WARNING: define the correct hosts in production!
# 确保 ALLOWED_HOSTS 包含你的 IP 地址
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.20.2",
    "0.0.0.0",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
