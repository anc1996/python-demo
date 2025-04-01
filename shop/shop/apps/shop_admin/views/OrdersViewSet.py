#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.status import *

from orders.models import OrderInfo
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.order_serializer import OrderInfoSerializer, OrderStatusSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    """
        订单管理
    """
    # 指定序列化器
    serializer_class = OrderInfoSerializer
    # 指定页
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser,]


    # 指定查询集
    def get_queryset(self):
        """指定查询集"""
        keyword = self.request.query_params.get('keyword')
        if not keyword:
            return OrderInfo.objects.all()
        return OrderInfo.objects.filter(order_id__icontains=keyword)


    @action(methods=['put'],detail=True)
    def status(self,request,pk):
        """
        修改订单状态
        :param request:
        :param pk:订单编号
        :return:
        """
        # 获取订单对象
        order = self.get_object()
        # 获取状态
        status = request.data.get('status')
        if status not in OrderInfo.ORDER_STATUS_ENUM.values():
            return Response({'error':'参数有误'},status=HTTP_400_BAD_REQUEST)
        # 修改订单状态
        serializer = OrderStatusSerializer(instance=order,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'order_id': order.order_id,
            'status': order.status
        })

