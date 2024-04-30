# 定义任务
from celery_tasks.send_sms_code.ronglian_sms_sdk.SendMessage import CCP
from celery_tasks.send_sms_code import constants
from celery_tasks.main import celery_app

# 使用装饰器异步任务，保证celery识别任务
# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
@celery_app.task(bind=True,name='ccp_send_sms_code',retry_backoff=2,max_retries=4)
def ccp_send_sms_code(self,mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param self:
    :param mobile:手机号
    :param sms_code:短信验证码
    :return:成功 0；失败 -1
    """

    # 10.发送短信验证码
    # 单例类发送短信验证码，过期时间5分钟，测试的短信模板编号为1
    # CCP().send_template_sms('15775023011', ['1134', 5], '1')
    if constants.SMS_CODE_REDIS_EXPIRES < 60:
        expire = 1
    else:
        expire = constants.SMS_CODE_REDIS_EXPIRES // 60
    # send_ret = CCP().send_template_sms(mobile, [sms_code, expire], constants.SEND_SMS_TEMPLATE_ID)
    try:
        send_ret=CCP().send_template_sms(mobile, [sms_code, expire], constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        # 触发错误重试：最多3次
        raise self.retry(exec=e,max=2)
    return send_ret