#!/user/bin/env python3
# -*- coding: utf-8 -*-
# celery的入口
from celery import Celery
import os

# 为celery使用django配置文件进行设置
print('DJANGO_SETTINGS_MODULE路径:',os.getenv('DJANGO_SETTINGS_MODULE'))
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.dev_settings'

# 创建celery实例，对应生产者
celery_app=Celery('producer')
# 加载配置文件的路径
celery_app.config_from_object('celery_tasks.config')

# 注册任务列表
celery_app.autodiscover_tasks(['celery_tasks.send_sms_code',])
#
## 消费者为celery，启动进程



