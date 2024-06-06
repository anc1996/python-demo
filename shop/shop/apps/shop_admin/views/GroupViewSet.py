#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group,Permission
from rest_framework.response import Response

from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.group_serializer import GroupSerializer,PermissionSerializer

class GroupView(ModelViewSet):

    # 权限管理
    permission_classes = [IsAdminUser,]
    # 序列化器
    serializer_class =GroupSerializer
    # 查询集
    queryset =Group.objects.all()
    # 分页器
    pagination_class = PageNum



    def simple(self,request):
        # 查询所有权限数据
        pers=Permission.objects.all()
        ser=PermissionSerializer(pers,many=True)
        return Response(ser.data)
