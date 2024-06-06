#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db import transaction

from celery_tasks.static_details.tasks import get_detail_html
from goods.models import SKU, GoodsCategory, SKUSpecification, SPUSpecification, SpecificationOption


class SKUSpecificationSerialzier(ModelSerializer):
    """
      SKU具体规格表序列化器
    """
    # spu规格名称id
    spec_id = serializers.IntegerField()
    # spu规格值的value
    option_id = serializers.IntegerField()
    class Meta:
        model = SKUSpecification # SKUSpecification中sku外键关联了SKU表
        fields=("spec_id",'option_id')

class SkuSerializer(ModelSerializer):
    """
        SKU的序列化器
    """
    # 指定所关联的spu表信息
    spu_id = serializers.IntegerField()
    # 指定所关联的选项信息 关联嵌套返回
    specs = SKUSpecificationSerialzier(read_only=True, many=True)
    # 指定分类信息
    category_id = serializers.IntegerField()
    class Meta:
        model = SKU
        fields = "__all__"
        # read_only_fields指定只读字段，不会被序列化器接收
        read_only_fields = ('spu', 'category')

    def create(self, validated_data):
        """
            {'caption': '123', 'category_id': 115,
            'cost_price': Decimal('12344.00'),
            'is_launched': True,
            'market_price': Decimal('12344.00'),
            'name': 'sd', 'price': Decimal('111444.00'),
            'spu_id': 3, 'stock': 122}
            :param validated_data: # validated_data是前端传递的数据
            :return: sku
        """
        # specs前端返回的是list类型，当前list
        # 'specs': [{'option_id': 14, 'spec_id': '6'}, {'option_id': 21, 'spec_id': '7'}]
        specs = self.context['request'].data.get('specs')
        # # 开启事务
        with transaction.atomic():
            try:
                # 设置保存点
                save_point = transaction.savepoint()
                # 保存sku表
                sku=SKU.objects.create(**validated_data)
                # 保存sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.create(spec_id=spec['spec_id'],option_id=spec['option_id'],sku=sku)
            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:
                # 提交
                transaction.savepoint_commit(save_point)
                # 生成详情页的静态页面
                get_detail_html.delay(sku.id)
                return sku

    def update(self, instance, validated_data):
        """
         {
            "id": "商品SKU ID",
            "name": "商品SKU名称",
            "goods": "商品SPU名称",
            "goods_id": "商品SPU ID",
            "caption": "商品副标题",
            "category_id": "三级分类id",
            "category": "三级分类名称",
            "price": "价格",
            "cost_price": "进价",
            "market_price": "市场价",
            "stock": "库存",
            "sales": "销量",
            "is_launched": "上下架",
            "specs": [
                {
                    "spec_id": "规格id",
                    "option_id": "选项id"
                },
                ...
            ]
        }
        :param instance:
        :param validated_data:
        :return:
        """
        specs = self.context['request'].data.get('specs')
        # # 开启事务
        with transaction.atomic():
            try:
                # 设置保存点
                save_point = transaction.savepoint()
                # 修改sku表
                SKU.objects.filter(id=instance.id).update(**validated_data)

                # 获取当前 SKU 的所有规格
                SKUSpecification_List = SKUSpecification.objects.filter(sku=instance)

                # 获取表中所有现有规格的spec_id集合
                existing_spec_ids = set(SKUSpecification_List.values_list('spec_id', flat=True))
                # 获取列表中所有规格的spec_id集合
                new_spec_ids = set(int(spec['spec_id']) for spec in specs)

                # 找出需要删除的规格
                specs_to_delete = existing_spec_ids - new_spec_ids
                # 找出需要更新的规格
                specs_to_update = existing_spec_ids - specs_to_delete
                # 找出需要创建的规格
                specs_to_create = new_spec_ids - existing_spec_ids

                # 删除多余的规格
                if specs_to_delete:
                    SKUSpecification.objects.filter(sku=instance, spec_id__in=specs_to_delete).delete()

                # 更新现有的规格
                for spec in specs:
                    if int(spec['spec_id']) in specs_to_update:
                        SKUSpecification.objects.filter(sku=instance, spec_id=spec['spec_id']).update(
                            **spec)

                # 创建新的规格
                for spec in specs:
                    if int(spec['spec_id']) in specs_to_create:
                        SKUSpecification.objects.create(spec_id=spec['spec_id'], option_id=spec['option_id'],
                                                        sku=instance)

            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:
                # 提交
                transaction.savepoint_commit(save_point)
                # 生成详情页的静态页面
                get_detail_html.delay(instance.id)
                return instance




class SKUCategorieSerializer(ModelSerializer):
    """
          商品分类序列化器
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class SPUOptineSerializer(serializers.ModelSerializer):
    """
      SPU规格选项序列化器
    """
    class Meta:
        model = SpecificationOption
        fields=('id','value','spec_id')

class SPUSpecSerialzier(ModelSerializer):
    """
        SPU规格序列化器
    """

    # 关联序列化返回SPU表数据（通过字符串关联）
    spu = serializers.StringRelatedField(read_only=True)
    # 关联序列化返回SPU表数据（通过整数关联）
    spu_id = serializers.IntegerField(read_only=True)
    # 关联序列化返回 规格选项信息,由于SpecificationOption的spec中关联options属性
    options = SPUOptineSerializer(read_only=True, many=True)  # 使用规格选项序列化器

    class Meta:
        # SPUSpecification模型类
        model = SPUSpecification
        fields = "__all__"


