#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
# sys.path.insert(0, '../')

from django.template import loader



from celery_tasks.main import celery_app

from contents.utils import get_categories, get_breadcrumb
from goods.models import SKU
from shop.settings import dev_settings as settings

@celery_app.task(bind=True,name='get_detail_html',retry_backoff=3,max_retries=4) # name给任务起别名
def get_detail_html(self,sku_id):
    """
    生成静态商品详情页面
    :param sku_id: 商品sku id
    """

    sku = SKU.objects.get(id=sku_id)

    # 查询商品分类
    categories_list = get_categories()
    # 查询面包屑导航
    breadcrumb = get_breadcrumb(sku.category)

    # 1.构建当前商品的规格键，
    # 获取当前显示商品的所有规格，例如sku=2
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        # 添加该规格的所有选项 ，sku-key对应规格id为[1，3，7]
        sku_key.append(spec.option.id)

    # 2.获取当前商品的所有SKU
    skus = sku.spu.sku_set.all()
    # 构建不同规格参数（选项）的sku字典
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.specs.order_by('spec_id')
        # 用于形成规格参数-sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数-sku字典添加记录
        spec_sku_map[tuple(key)] = s.id
    # spec_sku_map --> {(1,4,7):1,(1,3,7):2}

    # 获取当前商品的这一类所有的规格信息
    goods_specs = sku.spu.specs.order_by('id')
    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(goods_specs):
        return
    # 遍历当前商品的规格信息
    for index, spec in enumerate(goods_specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = spec.options.all()
        # 遍历该规格的选项
        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        # 将规格选项赋值给spec
        spec.spec_options = spec_options

    # 构造上下文
    context = {
        'categories': categories_list,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,
    }

    template = loader.get_template('detail.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'detail/'+str(sku_id)+'.html')
    with open(file_path, 'w') as f:
        f.write(html_text)