#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from users.models import User
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        #  username字段增加长度限制，password字段只参与保存，不在返回给前端，增加write_only选项参数
        extra_kwargs = {
            'username': {'max_length': 20,'min_length': 5},
            'password': {'max_length': 20,'min_length': 8,'write_only': True},
        }

    # 手机验证
    def validate_mobile(self,vaule):
        if not re.match(r'^1[3-9]\d{9}$', vaule):
            raise serializers.ValidationError('手机号格式不匹配')
        return vaule

    # 邮箱验证
    def validate_email(self, value):
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', value):
            raise serializers.ValidationError('邮箱格式不匹配')
        return value


    # 保存数据
    def create(self, validated_data):
        # 获取密码
        pwd = validated_data.get('password')
        validated_data['is_staff'] = True
        # 加密密码
        user = super().create(validated_data)
        # 密码加密
        user.set_password(pwd)
        user.save()
        return user


    def update(self, instance, validated_data):
        # 获取密码
        pwd = validated_data.get('password')
        # 加密密码
        user = super().update(instance, validated_data)
        if pwd:
            user.set_password(pwd)
        user.save()
        return user