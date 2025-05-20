from django.apps import AppConfig

"""
apps.py的主要功能:
    通过name属性指定应用的Python导入路径。
    自定义数据库字段类型：通过default_auto_field指定默认主键字段类型。
    信号注册：在ready()方法中可以连接信号处理器。
    通过verbose_name属性为应用设置更友好的显示名称。
"""

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # 设置默认主键字段为BigAutoField
    name = 'blog'  # 指定应用的导入路径

    # 这段代码在应用加载时清除代理设置，不是标准用法
    # 通常这类环境配置应该放在项目的settings.py或单独的初始化模块中
    import os
    for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
        if proxy_var in os.environ:
            del os.environ[proxy_var]  # 删除代理设置

    os.environ['NO_PROXY'] = '*' # 设置不使用代理