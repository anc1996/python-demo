#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission,ContentType
from rest_framework import serializers

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    #
    name=serializers.CharField(read_only=True)
    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = ContentType
        fields = "__all__"
