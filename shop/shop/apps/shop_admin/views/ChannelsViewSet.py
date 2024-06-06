#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.channel_serializer import ChannelSerializer, ChannelGroupSerializer, \
    CategorySimpleSerializer


class ChannelViewSet(ModelViewSet):
    """频道管理视图集"""
    permission_classes = [IsAdminUser,]
    # 指定视图所使用的查询集
    queryset = GoodsChannel.objects.all()
    # # 指定分页器 进行分页返回
    pagination_class = PageNum
    # 指定序列化器类
    serializer_class = ChannelSerializer

class ChannelCategoriesView(ListAPIView):
    """频道对应一级分类视图"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsCategory.objects.filter(parent=None)

    # 指定序列化器类
    serializer_class = CategorySimpleSerializer

    # 注：关闭分页
    pagination_class = None

class ChannelTypesView(ListAPIView):
    """频道组视图"""
    permission_classes = [IsAdminUser,]
    # 指定视图所使用的查询集
    queryset = GoodsChannelGroup.objects.all()

    # 指定序列化器类
    serializer_class = ChannelGroupSerializer

    # 注：关闭分页
    pagination_class = None

