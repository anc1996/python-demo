#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework import serializers

from goods.models import SPU, Brand, GoodsCategory


class SPUBrandsSerializer(serializers.ModelSerializer):
    """
        SPU品牌序列化器
    """
    class Meta:
        model = Brand
        fields =('id','name')

class SPUCategorysSerializer(serializers.ModelSerializer):
    """
        SPU分类序列化器
    """
    class Meta:
        model = GoodsCategory
        fields = ('id','name')

class SPUGoodsSerialzier(serializers.ModelSerializer):
    """
        SPU表序列化器
    """
    # 一级分类id
    category1_id = serializers.IntegerField()
    # 二级分类id
    category2_id = serializers.IntegerField()
    # 三级级分类id
    category3_id = serializers.IntegerField()
    # 关联的品牌id
    brand_id = serializers.IntegerField()
    # 关联的品牌，名称
    brand = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SPU
        exclude = ('category1', 'category2', 'category3')


