from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# from shop.utils.models import BaseModel

class User(AbstractUser):
     # 自定义用户模型类,在自定义用户模型类时要到settings.py中设置AUTH_USER_MODEL = 'users.User'，否则依赖系统自带用户模型类global_settings
     '''
         继承父类：AbstractUser父类
         创建用户必选： username、password
         创建用户可选：email、first_name、last_name、last_login、date_joined、is_active 、is_staff、is_superuse
         判断用户是否通过认证：is_authenticated
     '''
     mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')
     # email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
     # blank=True表示这个字段在表单中可以不填。null=True表示这个字段在数据库中可以为空。
     # default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
     #                                     on_delete=models.SET_NULL, verbose_name='默认地址')


     class Meta:
         db_table='tb_user'  # 自定义数据库表名为tb_user
         verbose_name = '用户'  # 后台显示用户表的名称
         verbose_name_plural = verbose_name #类属性，它的作用域也是整个类，用于指定在后台显示用户表的复数名称

     # 调试用的
     def __str__(self):
         return self.username


# class Address(BaseModel):
#     """用户地址"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
#     title = models.CharField(max_length=20, verbose_name='地址名称')
#     receiver = models.CharField(max_length=20, verbose_name='收货人')
#     province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
#     city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
#     district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
#     place = models.CharField(max_length=50, verbose_name='地址')
#     mobile = models.CharField(max_length=11, verbose_name='手机')
#     tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
#     email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
#     is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
#
#     class Meta:
#         db_table = 'tb_address'
#         verbose_name = '用户地址'
#         verbose_name_plural = verbose_name
#         ordering = ['-update_time'] # 根据根据updatetime字段倒序更新,updatetime字段在BaseModel模型中