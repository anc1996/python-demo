"""
WSGI config for shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# 设置DJANGO_SETTINGS_MODULE环境变量
# wsgi.py 是 WSGI（Web Server Gateway Interface）应用程序的入口。
# WSGI 是一个 Python 规范，用于定义 Web 服务器如何与 Web 应用程序交互。
# 在 Django 中，wsgi.py 文件负责启动 Django 应用程序，并将它暴露给 WSGI 服务器（如 Gunicorn 或 uWSGI）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings.dev_settings")
application = get_wsgi_application()
