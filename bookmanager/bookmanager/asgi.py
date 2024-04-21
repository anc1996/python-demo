"""
ASGI config for bookmanager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# 作为你的项目的运行在 ASGI 兼容的 Web 服务器上的入口。
# 这个文件通常位于你的项目的根目录下，例如 mysite/asgi.py。
# 它用于在支持 ASGI 的 Web 服务器（如 Gunicorn、Hugging Face、Uvicorn 等）上运行你的 Django 项目。
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmanager.settings")

application = get_asgi_application()
