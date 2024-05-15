from django.db import models

from goods.models import SKU
from shop.utils.models import BaseModel
from users.models import User, Address


# Create your models here.
class OrderInfo(BaseModel):
    """订单信息：一"""

    # 支付方式，以后判断用的
    PAY_METHODS_ENUM = {"CASH": 1,"ALIPAY": 2}
    # 支付选择
    PAY_METHOD_CHOICES = ((1, "货到付款"),(2, "支付宝"),)

    # 订单状态，以后判断用的
    ORDER_STATUS_ENUM = {
        "UNPAID": 1, # 未支付
        "UNSEND": 2,# 未发货
        "UNRECEIVED": 3, # 未收货
        "UNCOMMENT": 4,# 未评价
        "FINISHED": 5# 未完成
    }
    # 订单状态选项
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )

    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    user = models.ForeignKey(User,related_name='orders', on_delete=models.PROTECT, verbose_name="下单用户")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="收货地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")

    class Meta:
        db_table = "tb_order_info"
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id

class OrderGoods(BaseModel):
    """订单号的包含商品信息：多"""

    # 评论分
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )
    order = models.ForeignKey(OrderInfo, related_name='skus', on_delete=models.CASCADE, verbose_name="订单")
    # on_delete=models.PROTECT 是这个外键的一个属性，表示在删除关联的记录时，会保护这个外键关联的记录，不会被删除
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    comment = models.TextField(default="", verbose_name="评价信息")
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name='满意度评分')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价了')

    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name