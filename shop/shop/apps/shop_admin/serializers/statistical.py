#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from goods.models import GoodsVisitCount


class GoodsVisitCountSerializer(serializers.ModelSerializer):
    # 指定返回分类名称
    # StringRelatedField: 用于序列化关联对象的__str__方法返回值
    category=serializers.StringRelatedField(read_only=True,help_text='商品分类')
    
    
    class Meta:
        model=GoodsVisitCount
        fields=('count','category')

