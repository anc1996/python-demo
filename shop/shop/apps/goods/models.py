from django.db import models


from shop.utils.models import BaseModel
# Create your models here.


'''
- models.CASCADE，删除关联数据，与之关联也删除
- models.DO_NOTHING，删除关联数据，引发错误IntegrityError
- models.PROTECT，删除关联数据，引发错误ProtectedError
- models.SET_NULL，删除关联数据，与之关联的值设置为null（前提FK字段需要设置为可空）
- models.SET_DEFAULT，删除关联数据，与之关联的值设置为默认值（前提FK字段需要设置默认值）
- models.SET，删除关联数据，
              a. 与之关联的值设置为指定值，设置：models.SET(值)
              b. 与之关联的值设置为可执行对象的返回值，设置：models.SET(可执行对象)
'''
class GoodsChannelGroup(BaseModel):
    """商品频道组"""
    # 频道组名
    name = models.CharField(max_length=20, verbose_name='频道组名')

    class Meta:
        db_table = 'tb_channel_group'
        verbose_name = '商品频道组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsCategory(BaseModel):
    """商品类别"""
    # 类别名称
    name = models.CharField(max_length=10, verbose_name='名称')
    # 父类别,自连接
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsChannel(BaseModel):
    # 所属频道组名
    group=models.ForeignKey(GoodsChannelGroup,on_delete=models.PROTECT, verbose_name='频道组名')
    # 顶级商品类别
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,verbose_name='顶级商品类别')
    # 频道页面链接
    url = models.CharField(max_length=50, verbose_name='频道页面链接')
    # 组内顺序
    sequence = models.IntegerField(verbose_name='组内顺序')

    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModel):
    """品牌"""
    # 品牌名称
    name = models.CharField(max_length=20, verbose_name='名称')
    # Logo图片链接
    logo = models.ImageField(verbose_name='Logo图片')
    # 品牌首字母
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SPU(BaseModel):
    """商品SPU"""
    # 商品名称
    name = models.CharField(max_length=50, verbose_name='名称')
    # 品牌id
    brand=models.ForeignKey(Brand,on_delete=models.PROTECT, verbose_name='品牌')
    # 一级类别id
    category1 =models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一级类别')
    # 二级类别
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_spu', verbose_name='二级类别')
    # 三级类别
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_spu', verbose_name='三级类别')
    # 销量
    sales = models.IntegerField(default=0, verbose_name='销量')
    # 评价数
    comments = models.IntegerField(default=0, verbose_name='评价数')
    # 详细介绍
    desc_detail = models.TextField(default='', verbose_name='详细介绍')
    # 包装信息
    desc_pack = models.TextField(default='', verbose_name='包装信息')
    # 售后服务
    desc_service = models.TextField(default='', verbose_name='售后服务')

    class Meta:
        db_table = 'tb_spu'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SKU(BaseModel):
    """商品SKU"""
    # 商品SKU名称
    name = models.CharField(max_length=50, verbose_name='名称')
    # 商品副标题
    caption = models.CharField(max_length=100, verbose_name='副标题')
    # spu商品id
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='商品')
    # 从属类别id
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='从属类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进价')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售')
    default_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModel):
    """SKU图片"""
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)

class SPUSpecification(BaseModel):
    """商品SPU规格"""
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name='specs', verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='规格名称')

    class Meta:
        db_table = 'tb_spu_specification'
        verbose_name = '商品SPU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.spu.name, self.name)


class SpecificationOption(BaseModel):
    """SPU规格选项"""
    spec = models.ForeignKey(SPUSpecification, related_name='options', on_delete=models.CASCADE, verbose_name='规格')
    value = models.CharField(max_length=20, verbose_name='选项值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)


class SKUSpecification(BaseModel):
    """SKU具体规格"""
    # sku商品id
    sku = models.ForeignKey(SKU, related_name='specs', on_delete=models.CASCADE, verbose_name='sku')
    # spu规格名称id
    spec = models.ForeignKey(SPUSpecification, on_delete=models.PROTECT, verbose_name='规格名称')
    # spu规格值的value
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='规格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = 'SKU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)


class GoodsVisitCount(BaseModel):
    """统计分类商品访问量模型类"""
    # 每一天每一个id生成多少访问量
    count = models.IntegerField(verbose_name='访问量', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='统计日期')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品分类')

    class Meta:
        db_table = 'tb_goods_visit'
        # Django 将使用 verbose_name 的值作为表名。
        verbose_name = '统计分类商品访问量'
        # Django 将使用 InlineModelAdmin.verbose_name + 's'。
        verbose_name_plural = verbose_name