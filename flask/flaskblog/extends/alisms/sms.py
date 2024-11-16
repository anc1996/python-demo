# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import time,random
from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


from settings import Config

class Sample:
    def __init__(self):
        pass

    @staticmethod
    # 生成随机六位数
    def generate_code(phone):
        # 提取手机号的最后6位数字
        last_six_digits = phone[-6:]
        # 获取当前时间戳的最后6位数字
        timestamp_last_six_digits = str(int(time.time()))[-6:]
        # 结合手机号和时间戳随机生成验证码
        code = ''.join(random.sample(last_six_digits + timestamp_last_six_digits, 6))
        return code
    
    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=Config.ALIYUN_ACCESS_KEY_ID,
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=Config.ALIYUN_ACCESS_KEY_SECRET
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)


    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='个人模板网站',
            template_code='SMS_474970945',
            phone_numbers='15775023056',
            template_param='{"code":"1234"}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_sms_with_options_async(send_sms_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
    
    @staticmethod
    def send_sms(phone):
        code = Sample.generate_code(phone)
        client = Sample.create_client()
        
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=Config.sign_name,
            template_code=Config.template_code,
            phone_numbers=phone,
            template_param=f'{{"code":"{code}"}}'
        )
        
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response=client.send_sms_with_options(send_sms_request, runtime)
            # 判断发送是否成功
            if response.body.code == 'OK':
                return True, code
            else:
                print(f"ERROR: 返回错误信息: {response.body.message}")
                return False, None
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(f"ERROR: 短信发送失败: {error}")
            return False, None

if __name__ == '__main__':
    phone_number = '15775023056'
    success, code = Sample.send_sms(phone_number)
    if success:
        print(f"短信发送成功，验证码为: {code}")
    else:
        print("短信发送失败")