from django.apps import AppConfig

# 这个文件用于定义子应用的应用配置类，通常继承自 django.apps.AppConfig。
# 在这里，您可以指定应用的名称、配置一些应用级别的设置等。

class BookConfig(AppConfig):
    # 这个属性用于指定应用的名称，通常是子应用的目录名。
    default_auto_field = "django.db.models.BigAutoField"
    # 这个属性用于指定应用的名称，通常是子应用的目录名。
    # 是AppConfig.name = app_name
    name = "book"
    # AppConfig.name.verbose_name = self.label.title()
    verbose_name='book:图书管理'


