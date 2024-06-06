#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


class SpecSerializer(serializers.ModelSerializer):
    """
        获取规格信息序列化器
    """
    class Meta:
        model = SPUSpecification
        fields = ('id','name')

class OptionSerializer(serializers.ModelSerializer):
    """
        商品规格表序列化器
    """
    # 返回规格名称
    spec=serializers.StringRelatedField(read_only=True)
    # 返回规格id
    spec_id=serializers.IntegerField()
    class Meta:
        # 指定序列化器对应的模型
        model = SpecificationOption
        fields = "__all__"

    # def create(self, validated_data):
    #     """
    #         重写create方法
    #     """
    #     # 1、获取规格名称
    #     name = validated_data['name']
    #     # 2、获取规格表对象
    #     option = SpecificationOption.objects.create(name=name)
    #     return option
    #
    # def update(self, instance, validated_data):
    #     """
    #         重写update方法
    #     """
    #     # 1、获取规格名称
    #     name = validated_data['name']
    #     # 2、更新规格名称
    #     instance.name = name
    #     instance.save()
    #     return instance