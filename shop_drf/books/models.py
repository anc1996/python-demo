#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class BookInfo(models.Model):
    """
     1.主键 当前会自动生成
     2.属性复制过来就可以
     """
    """
    书籍表:
        id,name,pub_date,readcount,commentcount,is_delete
    """
    # 默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。
    # 属性名=属性类型(选项)
    # CharField：一个字符串字段，适用于小到大的字符串。
    name=models.CharField(max_length=10,unique=True,verbose_name='名字')
    # 发布日期
    # DateField：一个日期字段，适用于日期。
    pub_date=models.DateField(null=True,verbose_name='发布日期')
    # 阅读量
    # IntegerField：一个整数字段，适用于整数。
    readcount=models.IntegerField(default=0,verbose_name='阅读量')
    # 评论量
    commentcount=models.IntegerField(default=0,verbose_name='评论量')
    # 是否逻辑删除
    # BooleanField：一个布尔字段，适用于True或False。
    is_delete=models.BooleanField(default=False,verbose_name='书是否删除')
    #自动为我们添加一个属性，这个属性可以通过书籍查询人物信息。
    class Meta:
        # 用于模型的数据库表的名称：
        db_table='bookinfo'
        # 在admin站点中显示的名称
        verbose_name = '图书表'
        verbose_name_plural=verbose_name

    def __str__(self):
        """将模型类以字符串的方式输出"""
        return self.name

class PeopleInfo(models.Model):
    # 书籍: 人物  1:n
    # 西游记:  孙悟空,白骨精
    # on_delete

    # 默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。
    name = models.CharField(max_length=20, verbose_name='名称')
    # 性别
    # 有序字典
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2,'secrecy')
    )
    # SmallIntegerField：一个小整数字段，适用于小整数。
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    # 描述
    description = models.CharField(max_length=200, null=True, verbose_name='描述')
    # ForeignKey：一个外键字段，用于关联另一个模型。
    # 外键book建立在PeopleInfo表中，关联BookInfo表
    #     CASCADE,级联删除。Django 模拟了 SQL 约束 ON DELETE CASCADE 的行为，也删除了包含 ForeignKey 的对象。
    #     DO_NOTHING,不采取任何行动。如果你的数据库后端强制执行引用完整性，这将导致一个 IntegrityError 除非你
    #               手动添加一个 SQL ON DELETE 约束条件到数据库字段。
    #     PROTECT,通过引发 ProtectedError，即 django.db.IntegrityError 的子类，防止删除被引用对象。
    #     RESTRICT,通过引发 RestrictedError （ django.db.IntegrityError 的一个子类）来防止删除被引用的对象。
    #               与 PROTECT 不同的是，如果被引用的对象也引用了一个在同一操作中被删除的不同对象，
    #               但通过 CASCADE 关系，则允许删除被引用的对象。
    #     SET,将 ForeignKey 设置为传递给 SET() 的值，或者如果传递的是可调用对象，则调用它的结果。
    #     SET_DEFAULT,将 ForeignKey 设置为默认值，必须为 ForeignKey 设置一个默认值。
    #     SET_NULL,设置 ForeignKey 为空；只有当 null 为 True 时，才有可能。
    book=models.ForeignKey(BookInfo,on_delete=models.CASCADE,verbose_name='图书')
    # 逻辑删除
    is_delete=models.BooleanField(default=False,verbose_name='人物是否删除')
    class Meta:
        db_table='peopleinfo'
        verbose_name='人物表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name