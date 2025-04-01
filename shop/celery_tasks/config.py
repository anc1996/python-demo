

from shop.settings import dev_settings as settings
# Celery配置文件

# 使用redis做中间人（消息队列）缓存。
# 消息代理是 Celery 的核心组件，负责在任务的生产者和消费者之间传递任务消息。
broker_url=settings.celery_broker_url

# result_backend是 Celery 的结果存储的 URL，用于指定任务执行结果的存储位置。
# 当任务执行完成后，任务的结果会被存储到结果存储中，供后续查询或处理。
result_backend =settings.celery_result_backend

# 存储有效期2个小时，默认1天
result_expires = 2 * 3600
timezone = 'Asia/Shanghai'

# 存储序列化格式
result_serializer= 'json'

imports   = [     # 指定导入的任务模块,可以指定多个，方法二
    'celery_tasks.send_sms_code.tasks',
    'celery_tasks.email.tasks',
    'celery_tasks.static_details.tasks',
]




