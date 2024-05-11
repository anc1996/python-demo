from django.db import models

from shop.utils.models import BaseModel
# Create your models here.

class ContentCategory(BaseModel):
    """广告内容类别"""
    # 广告类别名称
    name = models.CharField(max_length=50, verbose_name='名称')
    # 类别识别键名
    key = models.CharField(max_length=50, verbose_name='类别键名')

    class Meta:
        db_table = 'tb_content_category'
        verbose_name = '广告内容类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Content(BaseModel):
    """广告内容"""
    # 广告内容类别,id:外键
    category = models.ForeignKey(ContentCategory,on_delete=models.PROTECT,verbose_name='类别')
    # 广告标题
    title = models.CharField(max_length=100, verbose_name='标题')
    # 内容网页链接地址
    url = models.CharField(max_length=300, verbose_name='内容链接')
    # 广告图片地址
    image = models.ImageField(null=True, blank=True, verbose_name='图片')
    # 广告文本内容
    text = models.TextField(null=True, blank=True, verbose_name='内容')
    # 同类别广告内顺序
    sequence = models.IntegerField(verbose_name='排序')
    # 是否展示
    status = models.BooleanField(default=True, verbose_name='是否展示')

    class Meta:
        db_table = 'tb_content'
        verbose_name = '广告内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name + ': ' + self.title
