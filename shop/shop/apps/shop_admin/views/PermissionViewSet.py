#!/user/bin/env python3
# -*- coding: utf-8 -*-


from django.contrib.auth.models import Permission,ContentType
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.permission_serializer import PermissionSerializer, ContentTypeSerializer


class PermissionView(ModelViewSet):

    # 权限管理
    permission_classes = [IsAdminUser,]
    # 序列化器
    serializer_class = PermissionSerializer
    # 查询集
    queryset = Permission.objects.all()
    # 分页器
    pagination_class = PageNum


    # 自己封装权限类型表操作
    def content_types(self,request):
        """
            获取权限类型
            :param request:
            :return:
        """
        # 1.获取权限类型数据
        content = ContentType.objects.all()
        # 2.验证权限类型数据
        serializer=ContentTypeSerializer(content,many=True)
        return Response(serializer.data)