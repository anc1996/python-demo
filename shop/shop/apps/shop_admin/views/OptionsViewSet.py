#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption, SPUSpecification
from shop_admin.serializers.PageNum import PageNum
from shop_admin.serializers.option_serializer import OptionSerializer, SpecSerializer


class Optionsimple(ListAPIView):
    """
        获取规格spec信息
    """
    serializer_class = SpecSerializer
    queryset = SPUSpecification.objects.all()

class OptionViewSet(ModelViewSet):
    """

        {
            "id": "选项id",
            "value": "选项名称",
            "spec": "规格名称",
            "spec_id": "规格id"
        },
        ...
        spu商品规格表
    """
    serializer_class = OptionSerializer
    # 指定分页器
    pagination_class = PageNum
    # 指定视图所使用的查询集
    queryset = SpecificationOption.objects.all()