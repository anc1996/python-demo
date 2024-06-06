#!/user/bin/env python3
# -*- coding: utf-8 -*-
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from django.db import transaction
import traceback

from goods.models import Brand
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.brand_serializer import BrandSerializer


class BrandViewSet(ModelViewSet):
    """频道管理视图集"""
    permission_classes = [IsAdminUser,]
    # 指定视图所使用的查询集
    queryset = Brand.objects.all()
    # # 指定分页器 进行分页返回
    pagination_class = PageNum
    # 指定序列化器类
    serializer_class = BrandSerializer


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        client = Fdfs_client(settings.FASTDFS_PATH)
        image_url = instance.logo.name
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance.delete()
                ret_delete = client.delete_file(image_url)
                print('图片删除成功:', ret_delete)
                transaction.savepoint_commit(save_id)
                return Response(status=HTTP_204_NO_CONTENT)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                print("FastDFS delete file fail, {0}, {1}".format(e, traceback.print_exc()))
                return Response(status=HTTP_400_BAD_REQUEST)