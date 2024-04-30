# Celery配置文件

# 使用redis做中间人（消息队列）缓存。
# broker_url是Celery消息代理（Message Broker）的URL。当一个任务被发送到Celery时，它首先被发送到消息代理。
broker_url='redis://:123456@127.0.0.1:6379/2'


timezone = 'Asia/Shanghai'




