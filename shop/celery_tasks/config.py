# Celery配置文件

# 使用redis做中间人（消息队列）缓存。
# broker_url是Celery消息代理（Message Broker）的URL。当一个任务被发送到Celery时，它首先被发送到消息代理。
broker_url='redis://:123456@127.0.0.1:6379/2'
# 结果存储
result_backend = 'redis://:123456@127.0.0.1:6379/10'
# # 存储有效期2个小时，默认1天
# result_expires = 2 * 3600
timezone = 'Asia/Shanghai'
# 存储序列化格式
result_serializer= 'json'

imports   = [     # 指定导入的任务模块,可以指定多个，方法二
    'celery_tasks.send_sms_code.tasks',
    'celery_tasks.email.tasks',
]




