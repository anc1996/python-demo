#!/user/bin/env python3
# -*- coding: utf-8 -*-
import traceback

from fdfs_client.client import Fdfs_client
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction

from goods.models import SKU, GoodsCategory, SPU, SKUSpecification, SKUImage
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.sku_serializer import SkuSerializer, SKUCategorieSerializer, SPUSpecSerialzier


class SKUView(ModelViewSet):
    # 指定序列化器
    serializer_class =SkuSerializer
    # 指定分页器 进行分页返回
    pagination_class = PageNum
    # 权限指定
    permission_classes=[IsAdminUser,]

    # 重写get_queryset方法，判断是否传递keyword查询参数,为了搜索查询准备
    def get_queryset(self):
        # 提取keyword
        keyword=self.request.query_params.get('keyword')
        # 当获取单一数据时要keyword is None
        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name__icontains=keyword)  # 包含,忽略大小写

    # action装饰器，自定义路由
    @action(methods=['get'], detail=False)
    def categories(self, request):
        """
        获取三级分类的方法
        :param request:
        :return:
        """
        # 子节点没有id
        data = GoodsCategory.objects.filter(subs__id=None)
        serializer = SKUCategorieSerializer(data, many=True)
        return Response(serializer.data)


    def specs(self,request,pk):
        """
        获取spu_id的规格，以及规格选项信息
        :param request:
        :param pk:spu_id
        :return:
        """
        # 1、查询spu对象
        spu=SPU.objects.get(id=pk)
        # 2、查询spu所关联的规格表
        data=spu.specs.all()
        # 3、序列号返回规格信息
        serializer=SPUSpecSerialzier(data,many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        client = Fdfs_client(settings.FASTDFS_PATH)
        instance = self.get_object()

        with transaction.atomic():
            try:
                # 删除图片的数据
                SkuImage_list = SKUImage.objects.filter(sku_id=instance.id)
                for skuimage in SkuImage_list:
                    image_url=skuimage.image.name
                    group_url=image_url.replace('//', '/')
                    try:
                        ret_delete = client.delete_file(group_url)
                        print('图片删除成功:',ret_delete)
                    except Exception as e:
                        print("FastDFS delete file fail, {0}, {1}".format(e, traceback.print_exc()))
                SkuImage_list.delete()
                # 删除sku时，删除sku规格表中的数据
                SKUSpecification.objects.filter(sku_id=instance.id).delete()
                # 删除sku数据
                self.perform_destroy(instance)
            except Exception as e:
                # 如果出现异常，事务会自动回滚
                print(f"Failed to delete SKU and associated data: {e}")
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=HTTP_204_NO_CONTENT)