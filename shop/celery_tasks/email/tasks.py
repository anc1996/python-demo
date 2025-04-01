from django.core.mail import send_mail
import logging
from celery_tasks.main import celery_app
from django.core.mail import EmailMultiAlternatives,EmailMessage

from shop.settings import dev_settings as settings

# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限

# 创建日志输出器
logger=logging.getLogger('send_email')

@celery_app.task(bind=True,name='send_verify_email',retry_backoff=3,max_retries=4) # name给任务起别名
def send_verify_email(self,to_email,verify_url):
    """
    定义发送验证邮件
    :param to_email: 收件人
    :param verify_url: 激活链接
    :return:None
    """

    """
    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):
    send_mail方法参数：
        在大多数情况里，你可以使用 django.core.mail.send_mail() 来发送邮件。
        参数 subject, message, from_email 和 recipient_list 是必须的。
        subject: 标题，一个字符串,
        message: 正文一个字符串，
        from_email ：发件人。字符串。如果为 None ，Django 将使用 DEFAULT_FROM_EMAIL 设置的值。
        recipient_list:收件人列表。 一个字符串列表，每项都是一个邮箱地址。recipient_list 中的每个成员都可以在邮件的 "收件人:" 中看到其他的收件人。
        fail_silently: 一个布尔值。若为 False， send_mail() 会在发生错误时抛出 smtplib.SMTPException 。可在 smtplib 文档找到一系列可能的异常，它们都是 SMTPException 的子类。
        auth_user: 可选的用户名，用于验证登陆 SMTP 服务器。 若未提供，Django 会使用 EMAIL_HOST_USER 指定的值。
        auth_password: 可选的密码，用于验证登陆 SMTP 服务器。若未提供， Django 会使用 EMAIL_HOST_PASSWORD 指定的值。
        connection: 可选参数，发送邮件使用的后端。若未指定，则使用默认的后端。查询 邮件后端 文档获取更多细节。
        html_message:富文本（html）。 若提供了 html_message，会使邮件成为 multipart/alternative 的实例， message 的内容类型则是 text/plain ，并且 html_message 的内容类型是 text/html 。
        返回值会是成功发送的信息的数量（只能是 0 或 1 ，因为同时只能发送一条消息）。
    """

    subject = "shop邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用shop。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    # 由于django进程和celery进程相互独立,抛错如下，因此在celery启动进程配置，到main.py配置
    """
       引发意外：InproperlyConfigured（'请求的设置EMAIL_FROM，但未配置设置。在访问设置之前，
       您必须定义环境变量 DJANGO_SETTINGS_MODULE 或调用 settings.configure（）
   """
    try:
        # EmailMultiAlternatives：Django 提供的高级邮件发送类，支持更复杂的邮件配置，比如同时发送纯文本和 HTML 格式的邮件，还可以添加附件。
        # mail=EmailMultiAlternatives(subject=subject, body=html_message, from_email=settings.EMAIL_FROM, to=[to_email])
        # mail.content_subtype='html'
        # mail.send()
        
        # send_mail ：一个简单快捷的邮件发送方法，用于发送基础邮件。支持纯文本或带 HTML 的邮件内容。
        send_mail(subject=subject,message='',from_email=settings.EMAIL_FROM,recipient_list=[to_email],html_message=html_message)
    except Exception as e:
        # 触发错误重试：最多3次
        logger.error(f"发送邮件失败: {str(e)}")
        raise self.retry(exec=e,max=3) # 重试执行当前函数，最多重试3次。
