from django.contrib import admin
from book.models import BookInfo,PeopleInfo
# Register your models here.
# 这个文件用于注册您的模型到 Django 的管理界面。
# 您可以通过继承 admin.ModelAdmin 类并定义一些属性和方法来定制管理界面的行为。

#注册模型
# admin.site.register(模型类)
admin.site.register(BookInfo)
admin.site.register(PeopleInfo)