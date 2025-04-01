#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from orders.models import OrderInfo, OrderGoods
from goods.models import SKU
class OrderSkuSerializer(serializers.ModelSerializer):
    """sku商品信息"""
    class Meta:
        model = SKU
        fields = ['name','default_image']
        
        
class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    sku= OrderSkuSerializer(read_only=True)

    class Meta:
        model = OrderGoods
        fields = ['count','price','sku']


class OrderInfoSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    # skus是OrderGoods的外键related_name
    skus = OrderGoodsSerializer(many=True,read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):
    """订单状态序列化器类"""
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'status']
        read_only_fields = ['order_id', ]