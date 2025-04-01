#!/user/bin/env python3
# -*- coding: utf-8 -*-
# celery的入口
from celery import Celery
import os

# 为celery使用django配置文件进行设置，目前（email，）模块需要
if not os.getenv('DJANGO_SETTINGS_MODULE'): # 使用 os.getenv 检查当前环境变量中是否已经定义了 DJANGO_SETTINGS_MODULE。
    # 如果未设置，则将其设置为 'shop.settings.dev_settings'，确保 Celery 在任务中能找到 Django 的配置。
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.dev_settings'

# 创建celery实例，对应生产者
celery_app=Celery('producer')
# 加载配置文件的路径
celery_app.config_from_object('celery_tasks.config')

# # 注册任务列表，方法二
# celery_app.autodiscover_tasks([     # 指定导入的任务模块,可以指定多个，方法二
#     'celery_tasks.send_sms_code',
#     'celery_tasks.email',
#     'celery_tasks.static_details',
# ])
#
## 消费者为celery，启动进程



