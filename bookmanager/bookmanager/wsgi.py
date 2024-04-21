"""
WSGI config for bookmanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
# 作为你的项目的运行在 WSGI 兼容的Web服务器上的入口。
#  WSGI.py 是 Django 的旧版本的入口文件，它遵循 Python 的 WSGI (Web Server Gateway Interface) 规范。
#  这个文件通常位于你的项目的根目录下，例如 mysite/wsgi.py。
#  它用于在支持 WSGI 的 Web 服务器（如 Apache、Nginx、uWSGI 等）上运行你的 Django 项目。
#  要使用 WSGI.py 部署项目，你需要确保你的 Web 服务器支持 WSGI 协议，并配置正确
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmanager.settings")

application = get_wsgi_application()
