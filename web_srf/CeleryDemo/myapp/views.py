from django.shortcuts import render
from django.http import JsonResponse


from .tasks import add, send_email_task

# Create your views here.

def index(request):
    # 调用异步任务
    """
        访问 http://127.0.0.1:8000/，你将触发 Celery 任务。
		add 任务将计算 4 + 6，结果存储在 Redis 中。
		send_email_task 模拟发送电子邮件。
    """
    result = add.delay(4, 6)
    email_result = send_email_task.delay("test@example.com")
    return JsonResponse({
        "add_task_id": result.id,
        "email_task_id": email_result.id
    })