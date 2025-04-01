#!/user/bin/env python3
# -*- coding: utf-8 -*-
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def send_email_task(email):
    # 模拟发送电子邮件的逻辑
    print(f"Sending email to {email}")
    return f"Email sent to {email}"