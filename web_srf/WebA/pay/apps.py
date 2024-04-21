from django.apps import AppConfig


class PayConfig(AppConfig):
    # 这个属性用于指定应用的名称，通常是子应用的目录名。
    default_auto_field = 'django.db.models.BigAutoField'
    # 是AppConfig.name = app_name
    name = 'pay'
    verbose_name='pay:支付管理'
