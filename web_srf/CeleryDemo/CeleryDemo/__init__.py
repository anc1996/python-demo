from __future__ import absolute_import, unicode_literals

# 在 CeleryDemo/__init__.py 中，确保 Celery 应用在 Django 启动时加载：
from .celery import app as celery_app

__all__ = ('celery_app',)