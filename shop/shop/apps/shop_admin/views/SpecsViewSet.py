#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from goods.models import SPUSpecification, SPU
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.specs_serializer import SpecsSerializer, SPUSerializer


class SpecsView(ModelViewSet):
    # 权限指定
    permission_classes=[IsAdminUser,]

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

    """商品的规格表所有操作：增删改查"""
    # 1、要指定当前类视图使用的查询数据
    queryset = SPUSpecification.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class =SpecsSerializer
    # 3、指定分页器，会调用ModelMixin的list方法
    pagination_class =PageNum

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要写

    def simple(self,request):
        """
        获取SPU规格所关联的信息
        :param request:
        :return:
        """
        spus=SPU.objects.all()
        serializer=SPUSerializer(spus,many=True)
        return Response(serializer.data)