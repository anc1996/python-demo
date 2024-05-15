import logging
import os
from datetime import datetime

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.db import transaction

from orders.models import OrderInfo
from payment.models import Payment
from shop.utils.response_code import RETCODE
from shop.utils.views import LoginRequiredJSONMixin
from payment.utils import web_alipay, alipay_init

logger=logging.getLogger('payment')
# Create your views here.
class PaymentView(LoginRequiredJSONMixin, View):
    """对接支付宝订单支付功能"""

    def get(self, request, order_id):
        # 对接支付宝的支付订单
        """

        :param request:
        :param order_id:当前要支付的订单ID
        :return:JSON
        """
        user = request.user

        # # 校验order_id
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return HttpResponseForbidden('订单信息错误')


        alipay=alipay_init()

        # 方法一：
        # alipay_url=web_alipay(out_trade_no=str(order_id),
        #                       total_amount=str(order.total_amount),
        #                       subject=subject)

        # 响应登录支付宝连接
        # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境电脑网站支付网关：https://openapi-sandbox.dl.alipaydev.com/gateway.do? + order_string

        # 方法二：
        # 目前沙箱环境，电脑网站支付，需要跳转到：https://openapi-sandbox.dl.alipaydev.com/gateway.do? + order_string
        # 旧版
        # order_string = alipay.api_alipay_trade_page_pay(
        #     out_trade_no=order_id,
        #     total_amount=str(order.total_amount),
        #     subject= "SHOP订单%s" % order_id,
        #     return_url=settings.ALIPAY_RETURN_URL, # 可选，不填则使用默认 return url
        # )

        order_string=alipay.client_api(
            "alipay.trade.page.pay",
            biz_content={
                "out_trade_no": order_id,
                "total_amount": str(order.total_amount),
                "subject":  "SHOP订单%s" % order_id,
                "product_code": "FAST_INSTANT_TRADE_PAY"
            },
            return_url=settings.ALIPAY_RETURN_URL,  # this is optional
        )

        alipay_url = settings.ALIPAY_URL + "?" + order_string
        print(alipay_url)

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})


class PaymentStatusView(View):
    """保存订单支付状态"""

    def get(self,request):
        # 获取前端传入的请求参数
        query_dict = request.GET
        """
        charset=utf-8
        &out_trade_no=20240513203839000000006
        &method=alipay.trade.page.pay.return
        &total_amount=55281.00
        &sign=KbRQnkRX8nCzd7FHbxW4JIhJl+DIUS1tlF0meQXoiTUB2BYoigV0jtd~······
        &trade_no=2024051422001488090502967144
        &auth_app_id=9021000136698047
        &version=1.0
        &app_id=9021000136698047
        &sign_type=RSA2
        &seller_id=2088721035568010
        &timestamp=2024-05-14 23:58:06
        """
        data = query_dict.dict()
        # 获取并从请求参数中提取并移除sign
        signature = data.pop('sign')
        alipay=alipay_init()

        status=alipay.verify(data,signature=signature)
        if status:
            # 读取order_id
            order_id = data.get('out_trade_no')
            # 读取trade_no，支付宝的订单
            trade_id=data.get('trade_no')
            timestamp=datetime.strptime(data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
            with transaction.atomic():
                save_id = transaction.savepoint()
                try:
                    # 需要修改订单状态，将shop的订单和支付宝的订单保存一起
                    Payment.objects.update_or_create(order_id=order_id,trade_id=trade_id,timestamp=timestamp)
                    # 修改订单状态,由“待支付”改为“待评价”
                    OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                        status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])
                    transaction.savepoint_commit(save_id)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    logger.error(e)
                    transaction.savepoint_rollback(save_id)
                    return HttpResponseForbidden('订单：保存失败')

            # 渲染数据
            order = OrderInfo.objects.get(order_id=order_id)
            order.status_name = OrderInfo.ORDER_STATUS_CHOICES[order.status - 1][1]
            order.pay_method_name = OrderInfo.PAY_METHOD_CHOICES[order.pay_method - 1][1]
            order.sku_list = []
            order_goods = order.skus.all()
            for order_good in order_goods:
                sku = order_good.sku
                sku.count = order_good.count
                sku.amount = sku.price * sku.count
                order.sku_list.append(sku)
            # 响应结果
            context = {
                'trade_id': trade_id,
                'timestamp':timestamp,
                'order':order,
            }
            return render(request, 'pay_success.html', context)
        else:
            # 订单支付失败，重定向到我的订单
            return HttpResponseForbidden('非法请求')