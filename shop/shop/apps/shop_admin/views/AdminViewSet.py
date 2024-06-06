#!/user/bin/env python3
# -*- coding: utf-8 -*-


from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import Group

from shop_admin.serializers.group_serializer import GroupSerializer
from shop_admin.serializers.Admin_Serializer import AdminSerializer
from shop_admin.serializers.PageNum import PageNum
from users.models import User
class AdminView(ModelViewSet):

    # 权限管理
    permission_classes = [IsAdminUser,]
    # 序列化器
    serializer_class = AdminSerializer
    # 查询集
    # is_staff为普通管理员
    queryset =User.objects.filter(is_staff=True)
    # 分页器
    pagination_class = PageNum



    def simple(self,request):
        # 查询分组信息
        groups=Group.objects.all()
        ser=GroupSerializer(groups,many=True)
        return Response(ser.data)


