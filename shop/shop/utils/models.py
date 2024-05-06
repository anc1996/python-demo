from django.db import models


# 为了给项目中模型类补充数据创建时间和更新时间两个字段，我们需要定义模型类基类。
class BaseModel(models.Model):
    """为模型类补充字段"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，不会创建BaseModel的表用来数据迁移
        abstract = True