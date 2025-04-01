#!/user/bin/env python3
# -*- coding: utf-8 -*-
import traceback

from django.db import transaction
from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from celery_tasks.static_details.tasks import get_detail_html
from goods.models import SKUImage, SKU
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.image_serializer import ImagesSerializer, SkuSerializer

"""
    使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
    list() 提供一组数据
    retrieve() 提供单个数据
    create() 创建数据
    update() 保存数据
    destory() 删除数据
    ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。
    
    3）ModelViewSet
    继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin、
        CreateModelMixin、UpdateModelMixin、DestoryModelMixin。
"""
class ImagesView(ModelViewSet):
    # 权限指定
    permission_classes=[IsAdminUser,]
    """SKU图片的所有操作：增删改查"""

    # 1、要指定当前类视图使用的查询数据
    queryset = SKUImage.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = ImagesSerializer
    # 3、指定分页器，会调用ModelMixin的list方法
    pagination_class = PageNum

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要写
    
    

    def simple(self,request):
        """
            获取商品sku的信息
        :param request:
        :return:
        """
        skus=SKU.objects.all()
        serializer = SkuSerializer(skus, many=True)
        return Response(serializer.data)

    # 重写destroy方法
    def perform_destroy(self, instance):
        client = Fdfs_client(settings.FASTDFS_PATH)
        image_url = instance.image.name
        group_url = image_url.replace('//', '/')
        try:
            with transaction.atomic():
                instance.delete()
                ret_delete = client.delete_file(group_url)
                print('图片删除成功:', ret_delete)
        except Exception as e:
            print("删除失败: {0}, {1}".format(e, traceback.print_exc()))
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_204_NO_CONTENT)