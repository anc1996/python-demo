import logging,random
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from verifications.libs.ronglian_sms_sdk.SendMessage import CCP # 原来的发送短信验证码的单例类
from celery_tasks.send_sms_code.tasks import ccp_send_sms_code # 新的发送短信验证码的异步任务
from . import constants
from .libs.captcha.captcha import captcha
from shop.utils.response_code import *
# Create your views here.


# 创建日志输出器
logger=logging.getLogger('verifications')

class ImageCodeView(View):
    """图形验证码"""
    def get(self,request,uuid):
        """
        :param request:
        :param uuid:通用唯一识别码，用于唯一标识该图形验证码属于哪个用户的
        :return:image/jpg
        """

        '''实现主体业务逻辑：生成图形验证码，保持，并响应'''
        # 1.生成图形验证码
        text,image=captcha.generate_captcha()
        # """2.保存图形验证"""
        redis_conn=get_redis_connection('VerifyCode')
        # setnx(self, name: KeyT, value: EncodableT) -> ResponseT:
        # SETEX key seconds value
        # SETEX 命令将键 key 的值设置为 value,并将键 key 的生存时间设置为 seconds 秒钟。uuid：text（图形验证码）
        redis_conn.setex('img_%s' % uuid , constants.IMAGE_CODE_REDIS_EXPIRES,text)
        # 3.响应图形验证码
        return HttpResponse(image,content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""
    def get(self,request,mobile):
        """
        :param request:
        :param mobile:手机号
        :return:JSON
        """
        # 1.接受参数
        image_code_client=request.GET.get('image_code') # 接收客户端图形验证码
        uuid=request.GET.get('uuid') # 接收客户端uuid
        # 2.校验参数
        if not all([image_code_client,uuid]):
            return HttpResponseForbidden('缺少参数')

        # 3.创建连接redis对象
        redis_conn=get_redis_connection('VerifyCode')

        """先判断发送短信验证码是否频繁"""
        # 4.提取发送验证码的标记，send_flag=1表示频繁发送短信验证码
        send_flag=redis_conn.get('send_flag_%s'% mobile)
        if send_flag:
            return JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信验证码频繁'})

        # 5.提取图形验证码
        image_code_server=redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图形验证码已失效'})
        print('image_code_server：',type(image_code_server))

        # 6.删除图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 7.对比图形验证码
        image_code_server=image_code_server.decode()# 将 btyes 转成字符串类型
        if image_code_client.lower()!=image_code_server.lower(): # 验证码转小写
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码错误'})

        # 8.生成短信验证码,随机6位数
        sms_code='%04d' % random.randint(0,9999)
        logger.info('mobile号:%s,sms_code短信验证码:%s'% (mobile,sms_code)) # 手动输出日志，导出验证码

        # 9.保存短信验证码，有效事件300秒
        pl=redis_conn.pipeline()  # 创建redis管道，将多个命令添加到队列中
        pl.setex('sms_%s' % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        """避免频繁发送短信验证码"""
        pl.setex('send_flag_%s'% mobile,constants.SEND_SMS_CODE_INTERVAL,1) # 同时保存发送验证码的标记，60s内是否重复发送的标记
        pl.execute() # 执行

        # 10.发送短信验证码，设置2分钟过期
        # 用celery异步执行，生成者和消费模式，避免堵塞
        ret=ccp_send_sms_code.delay(mobile, sms_code) # 千万不要忘记写delay，异步任务
        # 响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信短信验证码成功'})

