#!/user/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import Group, Permission




# 1、ModelSerializer可以根据model所指定模型类自动序列化器字段
# 2、ModelSerializer实现了create和update方法
# 3、ModelSerializer的Meta类中指定model和fields
# 4、ModeSerializer指定了unique的唯一值选项,自动生成唯一值判断方法
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = Permission
        fields = '__all__'