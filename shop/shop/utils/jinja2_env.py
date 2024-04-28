#!/user/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage # 静态文件的存储

# 为 Django 模板不支持调用带参数的函数。由于 Jinja2 没有此限制，因此建议将你要用作上下文处理器的函数放在模板的全局变量 jinja2.Environment 中使用，如下所述
def jinja2_environment(**options):

    # 1.创建 Environment实例
    env = Environment(**options)
    # 2.指定(更新) jinja2的函数指向django的指定过滤器

    env.globals.update({
        # 将Django中的date、static和url函数添加到Jinja2环境的全局变量中。
        # 这样在Jinja2模板中就可以直接使用这些函数，就像在Django中使用模板标签一样。
        # 方法一：
        "static": static, # 静态文件的前缀，给定静态资产的相对路径，返回资产的绝对路径。
        # 方法二：
        # 'static': staticfiles_storage.url,  # 静态文件的前缀
        "url": reverse, # 反向解析
    })
    # 3.返回Environment实例
    return env

print("static",staticfiles_storage.url)
'''
到时html文件可以使用python里static、url函数
<img src="{{ static('path/to/company-logo.png') }}" alt="Company Logo">
<a href="{{ url('admin:index') }}">Administration</a>
'''
