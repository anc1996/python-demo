from django.test import TestCase

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from django.conf import settings
from alipay import AliPay, AliPayConfig

logger=logging.getLogger('payment')


def web_alipay(out_trade_no,total_amount,subject):
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    # 我自己的私钥，而公钥放到支付宝网页的。
    app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ali_keys/app_private_key.pem"),
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ali_keys/alipay_public_key.pem"),

    f = open("".join(app_private_key_path), "r")
    app_private_key = f.read()
    f = open("".join(alipay_public_key_path), "r")
    alipay_public_key = f.read()

    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = settings.ALIPAY_URL
    alipay_client_config.app_id = settings.ALIPAY_APPID
    alipay_client_config.app_private_key = app_private_key
    alipay_client_config.alipay_public_key = alipay_public_key

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，
    定义DefaultAlipayClient对象后，alipay_client_config不得修改，
    如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = out_trade_no
    model.total_amount = total_amount
    model.subject = subject
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)
    return response

def alipay_init():
    # 我自己的私钥，而公钥放到支付宝网页的。
    app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ali_keys/app_private_key.pem"),
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ali_keys/alipay_public_key.pem"),

    f = open("".join(app_private_key_path), "r")
    app_private_key = f.read()
    f = open("".join(alipay_public_key_path), "r")
    alipay_public_key = f.read()

    # 创建对接支付宝的接口sdk，得到登录页的地址
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        # 应用私钥
        app_private_key_string=app_private_key,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=settings.ALIPAY_DEBUG,  # 默认 False
        verbose=settings.ALIPAY_VERBOSE,# 默认 False
        config=AliPayConfig(timeout=15)  # 可选，请求超时时间
    )

    return alipay