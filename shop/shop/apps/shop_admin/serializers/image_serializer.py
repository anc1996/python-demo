#!/user/bin/env python3
# -*- coding: utf-8 -*-
from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from django.conf import settings
import traceback


from celery_tasks.static_details.tasks import get_detail_html
from goods.models import SKUImage, SKU


class ImagesSerializer(serializers.ModelSerializer):

    """
        SKU图片的序列化器
    """

    class Meta:
        model = SKUImage
        fields = "__all__"

    def create(self, validated_data):
        # self.context['request'] 获取请求对象
        file= self.context['request'].FILES.get('image')
        # 3、建立fastdfs客户端
        client = Fdfs_client(settings.FASTDFS_PATH)
        # 4、上传图片
        res=client.upload_by_buffer(file.read())
        # 5、判断是否上传成功
        if res['Status'] != 'Upload successed.':
            return serializers.ValidationError({'error':'上传图片失败'})
        # 6、获取上传后的路径
        group_url = res['Remote file_id']
        image_url=group_url.replace('\\','//')
        # 8、保存图片
        # validated_data['sku']是个对象
        img = SKUImage.objects.create(sku=validated_data['sku'], image=image_url)
        SKU.objects.filter(id=img.sku.id).update(default_image=image_url)
        # 异步生成详情页静态页面
        get_detail_html.delay(sku_id=img.sku.id)
        return img

    def update(self, instance, validated_data):
        # 3、建立fastdfs客户端
        client = Fdfs_client(settings.FASTDFS_PATH)
        file = self.context['request'].FILES.get('image')
        # 4、上传图片
        res = client.upload_by_buffer(file.read())
        # 5、判断是否上传成功
        if res['Status'] != 'Upload successed.':
            return serializers.ValidationError({'error': '上传图片失败'})
        try:
            ret_delete=client.delete_file(instance.image.name)
            print('图片删除成功:',ret_delete)
        except Exception as e:
            print("FastDFS delete file fail, {0}, {1}".format(e, traceback.print_exc()))
        # 6、获取上传后的路径
        group_url = res['Remote file_id']
        image_url = group_url.replace('\\', '//')
        # 8、更新图片
        instance.image=image_url
        instance.save()
        # 9.更新sku表默认的图片
        SKU.objects.filter(id=instance.sku.id).update(default_image=image_url)
        # 异步生成详情页静态页面
        get_detail_html.delay(sku_id=instance.sku.id)
        return instance




class SkuSerializer(serializers.ModelSerializer):
    """
        SKU的序列化器
    """
    class Meta:
        model = SKU
        fields = ('id', 'name')
