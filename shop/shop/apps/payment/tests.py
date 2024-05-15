from django.test import TestCase
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
logger=logging.getLogger('orders')


if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """

    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url ='https://openapi-sandbox.dl.alipaydev.com/gateway.do'
    alipay_client_config.app_id = "9021000136698047"
    alipay_client_config.app_private_key = 'MIIEowIBAAKCAQEAh1oEnyKD1PSi1lsGz4wyjbtqtTqUtEEXqMcNpBMCzmsJgPBFCCHSyhikB8hEk/cnvvXc5rqG4Y7mcrorGEbntPzATNdOqZgXJAEc8yCDY08PHrhNhBwUBUzIR/uUp8s+rHUZCeua5H5uIA5hTKw+16C0f9+OI9DgTc9n7YNYU0MxdRcWHLIr51/ugl4JfK5NUPKpdonMDiVcj3rpISGnoc5Y8zEpQ/m+HEn1tAvD0cQvU+rtnhp4ry7i1IDX1Z+8z62YLzcKrdfO+/cmETTKFTNJrRzYpPokN4Y9Eu0yIoRWiF9JpYnM6lFRXhrpU++2VMQdh1AY9xOjapUUehLABwIDAQABAoIBAHDU+O9UDYQ0X57ECTxxih8e8oibiiVt8fQv4844TumWzzhek52A3MC+o9cc+xZCPi7xtLHfItvbjX5sdcpqKXR2EzS7dAbrE7de+iwvmXfrCxa3217bLVFxvbBMKJNsWhXYFARyFRCP2Ov+MNyC5mxIus+ypEJ1ONeEpAWarcHSEObyJ1YOwZrQvdMHrN0yiRbV40R+0QPntjXZflPoYNhCy7zwagWjQFbg7MLfo7iA6bUOnTuhPUbfXfMReKzwfa7CFQWlMEjXEFR8VtHr30/RWveyFTJpXpTdoLOXAIfTEjwjW6jKVHh8fx+O1M57PjZgzAhKHVdFU/B1l2Bji1ECgYEA4SbUskureWmDb0oVwQPGFb3rEQCuJB0c8McFBOTTy5s+0S8c/G7qNvBQz4qMLGBAdomwt1DYKjUh2BViVnvGiaOD/1E5qZM3d4kgktJWkK7kHf74Vml7bDGH92Ba2R0DFCXuQ9oLcTnOJJI8uUKahapFA/Sm856zUvlf4AeSuhkCgYEAmeV1++vzTeJzNVvEAzFyU0xtu1IvPmxLYqvTr8aoqFooQUmxrMJnuETkIogTMR+TULMPKYW+iFYuxqZ5eN9WS0s9ahqgvIddGXF+si4aifWnjjCZnyo8B8eO+hOujRO208ZjGOvzx1oB/SyXubnd/mv7psxWc8/hS3/rNkP0zx8CgYBiUf2x+n9gHqaJ09VaG1bGKdBb9WsWVCxOLOrRL0gZ8qpk2OkUhy76XMk9SGhb/JBJ82jbNI+hJuCnpvbxg024z1IWDZdbqPEg3x39X6LzvZvaSXyS569BGQQiD868XwH4K3Q35yD2CeMubznbQO2Pj0JiLtU1L8lpY4LtpwD5CQKBgB565+dBUCr40sCasDPBs1b0KDeVi23dnQCp73885WKSmK51ng8NYeWJH3YHZWWxT0gIbtRWfOobx5/okN5zvW+kM0G0jGlKlhHX/LPllbQFR25OCd8QSltwFs1I4KVoZimDfVUORnYRSZuPHW3XdjRRxsG+btD5NzHw3/EbfH0ZAoGBALKjxGjV1o1XMa6Mc1f5tq2Y7RRGitJT5OdwojAvvAsELoKislqKAx0Eu+T4/dO41y+uhro0hh0GG0c6d/ztRKDJ84QGgBkEIgNc5asGY86rDHR8VA/II7xIsRamqMDzzyT0ymmL+6SS/88dDHfpXR6B0iHmKn/T2aesWISRsdCj'
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgiZtvPzvoAFDaKFBKG168O98s/NE1iL58DStHzMV3+RGbAa5NdIgEiFq/+TxieMbyn8KGhKrEdlxyQJDuogsYmbhaf6kHCQYsJbEVjVSMXlhc3/gR8gUFaUsow739u1t86BkytmuiXkisSD5Md6WXPR+bA7UsGGduDt2Saj21yPn5znkSpSrguN9oLnOyyISMcE2FPyw2IVRMKoES4VvU7R+wbSOk8IT4pymqmAdnCPXMc/UtjELeebgIz5X4Cc1sBF8ObqzfV9Aw7Zzubs+gxs1aWQYQX14tzkjKMGjz5Lc7KRZrBdfXwOsw4aW/qo/aSARxYPt2rUGn7g8M22joQIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)