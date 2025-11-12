# wagtailblog3/celery.py
import os
from celery import Celery
from django.conf import settings

"""
命令：celery -A wagtailblog3 worker -l info --concurrency=4 --pool=threads
# 停止当前的Celery进程，然后重新启动
celery -A wagtailblog3 worker --loglevel=in4fo --queues=email,default
"""

# 设置Django默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtailblog3.settings.dev')

# 创建Celery应用实例
app = Celery('wagtailblog3')

# 使用Django设置配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery配置
app.conf.update(
	# Redis作为消息代理和结果后端
	broker_url=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/2',
	result_backend=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/3',
	
	# 任务序列化设置
	task_serializer='json',
	accept_content=['json'],
	result_serializer='json',
	timezone='Asia/Shanghai',
	enable_utc=True,
	
	# 任务执行设置
	task_always_eager=False,  # 生产环境设为False，开发时可设为True进行测试
	task_eager_propagates=True,
	
	# 任务路由设置
	task_routes={
		'base.tasks.send_form_confirmation_email': {'queue': 'email'},
		'base.tasks.send_admin_notification_email': {'queue': 'email'},
	},
	
	# 工作进程设置
	worker_prefetch_multiplier=1,
	task_acks_late=True,
	
	# 任务重试设置
	task_default_retry_delay=60,  # 默认重试延迟60秒
	task_max_retries=3,  # 最大重试次数
	
	# 任务结果过期时间
	result_expires=3600,  # 1小时后过期
	
	# 错误处理
	task_reject_on_worker_lost=True,
)

# 自动发现任务
app.autodiscover_tasks()


# 调试信息
@app.task(bind=True)
def debug_task(self):
	print(f'Request: {self.request!r}')


# 健康检查任务
@app.task
def health_check():
	"""Celery健康检查任务"""
	return "Celery is working properly!"