from django.db import models

from orders.models import OrderInfo
from shop.utils.models import BaseModel


# Create your models here.
class Payment(BaseModel):
    """支付信息"""
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="支付编号")
    timestamp = models.DateTimeField(verbose_name='支付时间')
    class Meta:
        db_table = 'tb_payment'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name