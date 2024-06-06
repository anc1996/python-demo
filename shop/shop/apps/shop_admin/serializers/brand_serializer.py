#!/user/bin/env python3
# -*- coding: utf-8 -*-
import traceback

from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from django.conf import settings
from django.db import transaction

from goods.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """品牌序列化器类"""
    class Meta:
        model = Brand
        fields = '__all__'

    def update(self, instance, validated_data):

        file = self.context['request'].FILES.get('logo')
        if file is None:
            brand=Brand.objects.get(id=instance.id)
            validated_data['logo']=brand.logo
            brand.update(**validated_data)
            return instance
        # 3、建立fastdfs客户端
        client = Fdfs_client(settings.FASTDFS_PATH)
        with transaction.atomic():
            try:
                # 4、上传图片
                res = client.upload_by_buffer(file.read())
                # 5、判断是否上传成功
                if res['Status'] != 'Upload successed.':
                    return serializers.ValidationError({'error': '上传图片失败'})
                try:
                    ret_delete=client.delete_file(instance.logo.name)
                    print('图片删除成功:',ret_delete)
                except Exception as e:
                    print("FastDFS delete file fail, {0}, {1}".format(e, traceback.print_exc()))
                # 6、获取上传后的路径
                logo_url = res['Remote file_id'].replace('\\', '//')
                # 7、更新图片
                validated_data['logo'] = logo_url
                Brand.objects.filter(id=instance.id).update(**validated_data)
            except Exception as e:
                print(f"Failed to update brand: {e}")
                traceback.print_exc()
                raise serializers.ValidationError({'error': '更新失败'})
        return instance

