#!/user/bin/env python3
# -*- coding: utf-8 -*-
# 使用工厂模式创建Flask app，并结合使用配置对象与环境变量加载配置

from flask import Flask

class DefaultConfig(object):
    """配置"""
    SECRET_KEY = '1234sdfesdfsdfwerreweeee56'

def create_flask_app(DefaultConfig):

    """构建 Flask app对象工厂"""
    app=Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

    # 配置文件加载，这三种方式同时写，不会覆盖。它们会分别加载配置信息，
    # 如果配置信息有重复的键值对，那么后面的配置会覆盖前面的配置。但是，它们不会互相覆盖，而是各自独立地加载配置信息。

    app.config.from_object(DefaultConfig)

    app.config.from_envvar('product_config')

    return app

app=create_flask_app(DefaultConfig)

@app.route('/')
def hello_world():  # put application's code here
    # 读取配置信息
    print('SECRET_KEY:',app.config.get('SECRET_KEY'))
    return 'welcome to factory!'


if __name__ == '__main__':
    # export product_config='setting.py'
    # python product_setting.py
    app.run(host="0.0.0.0", port=5001, debug = True)