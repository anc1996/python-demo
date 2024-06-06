#!/user/bin/env python3
# -*- coding: utf-8 -*-
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import *
from django.conf import settings
from rest_framework import serializers

from goods.models import SPU, Brand, GoodsCategory
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.spu_serializer import SPUGoodsSerialzier, SPUBrandsSerializer, SPUCategorysSerializer


class SPUGoodsView(ModelViewSet):
    """
        {
            "counts": "商品SPU总数量",
            "lists": [
                {
                    "id": "商品SPU ID",
                    "name": "SPU名称",
                    "brand": "品牌名称",
                    "brand_id": "品牌id",
                    "category1_id": "一级分类id",
                    "category2_id": "二级分类id",
                    "category3_id": "三级分类id",
                    "sales": "SPU商品销量",
                    "comments": "SPU商品评论量",
                    "desc_detail": "商品详情",
                    "desc_pack": "商品包装",
                    "desc_service": "售后服务"
                },
                ...
           ],
           "page": "页码",
           "pages": "总页数",
           "pagesize": "页容量"
        }
    """

    # 指定序列化器
    serializer_class = SPUGoodsSerialzier
    # 指定分页器 进行分页返回
    pagination_class = PageNum
    # 权限指定
    permission_classes = [IsAdminUser,]
    # 指定视图所使用的查询集
    queryset = SPU.objects.all()

    def brand(self,request):
        # 1、查询所有品牌
        data=Brand.objects.all()
        # 2、序列化返回
        serializer=SPUBrandsSerializer(data,many=True)
        # 3、返回响应
        return Response(serializer.data)

    def channel(self,request):
        """
        查询一级分类
        :param request:
        :return:
        """
        # 1、查询所有频道
        data=GoodsCategory.objects.filter(parent=None)
        # 2、序列化返回
        serializer=SPUCategorysSerializer(data,many=True)
        # 3、返回响应
        return Response(serializer.data)


    def SecondChannel(self,request,pk):
        """
            查询二级分类和三级分类
            :param request:
            :return:
        """
        data=GoodsCategory.objects.filter(parent_id=pk)
        serializer=SPUCategorysSerializer(data,many=True)
        return Response(serializer.data)

    def image(self,request):
        """
            spu编辑里-插入图片
            :param request:
            :return:
        """
        # 1、获取图片
        data=request.data.get('image')
        # 2、验证图片
        if data is None:
            return Response(status=HTTP_400_BAD_REQUEST)
        # 3、上传图片
        client = Fdfs_client(settings.FASTDFS_PATH)
        res=client.upload_by_buffer(data.read())
        # 4 、判断上传路径
        if res['Status'] != 'Upload successed.':
            return serializers.ValidationError({'error': '上传图片失败'})
        # 5、保存图片路径
        image_url=res['Remote file_id'].replace('\\', '//')
        # 6、返回响应
        return Response({
            'img_url':settings.FDFS_BASE_URL+image_url
        },status=HTTP_201_CREATED)