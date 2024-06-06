#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from goods.models import SPUSpecification, SPU


class SpecsSerializer(serializers.ModelSerializer):
    """
        商品SPU规格的序列化器
    """
    # 添加：指定关联外键返回数据形式
    spu=serializers.StringRelatedField(read_only=True)
    # 添加：指定关联外键返回数据形式
    spu_id=serializers.IntegerField()

    class Meta:
        # 指定序列化器类对应的模型类
        model=SPUSpecification
        # 指定序列化器类序列化所有字段
        fields="__all__"


class SPUSerializer(serializers.ModelSerializer):
    """
        spu序列号器
    """
    class Meta:
        model=SPU
        # fields="__all__"
        fields=('id','name')