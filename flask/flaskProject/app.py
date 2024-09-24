#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
# 首先我们导入了 Flask 类。该类的实例将会成为我们的 WSGI 应用。
from flask import Flask, Blueprint,g,abort
from config import DefaultConfig
from werkzeug.routing import BaseConverter

from goods import goods_bp
from users import users
from flask_context import context_bp
from flask_context1 import context_bp1


# 接着我们创建一个该类的实例。第一个参数是应用模块或者包的名称。 __name__ 是一个适用于大多数情况的快捷方式。有了这个参数， Flask 才能知道在哪里可以找到模板和静态文件等东西。
# 创建 Flask 实例
# Flask程序所在的包(模块)，传 __name__ 就可以其可以决定 Flask 在访问静态文件时查找的路径:寻找工程目录下的 static 和 templates 目录
#     import_name: 应用的导入名称，通常为app或application。
#     static_url_path: 静态文件URL前缀，默认为None。
#     static_folder: 静态文件存放的目录，默认为"static"。
#     static_host: 静态文件服务器的主机名，默认为None。
#     host_matching: 是否启用主机名匹配，默认为False。
#     subdomain_matching: 是否启用子域名匹配，默认为False。
#     template_folder: 模板文件存放的目录，默认为"templates"。
#     instance_path: 应用实例的路径，默认为None。
#     instance_relative_config: 是否使用相对路径配置，默认为False。
#     root_path: 应用的根路径，默认为None。

# 环境变量要写：export FLASK_APP=app:app
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')


# 环境变量要写：export FLASK_APP=app:app1
app1 = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# 创建redis客户端
app.redis_cli='redis client'
app1.redis_cli='redis client'

import exception
import lifecycle


# 配置文件加载，这三种方式同时写，不会覆盖。它们会分别加载配置信息，
# 如果配置信息有重复的键值对，那么后面的配置会覆盖前面的配置。但是，它们不会互相覆盖，而是各自独立地加载配置信息。

'''第一种方式：'''
# 从 config.py 文件中加载配置信息
# app.config.from_object(DefaultConfig)

'''第二种方式：'''
# 从 setting.py 文件中加载配置信息
# silent 参数设置为 True，如果没有找到配置文件，则不会报错
# app.config.from_pyfile('setting.py', silent=True)



'''第三种方式：'''
# 从环境变量中加载配置信息
'''
    在Linux系统中设置和读取环境变量的方式如下：
        export 变量名=变量值  # 设置
        echo $变量名  # 读取
    先在终端中执行如下命令
        export PROJECT_SETTING='/*/setting.py'
        
'''
# silent 参数设置为 True，如果没有设置环境变量，则不会报错，可以看pycharm调试配置
# export PROJECT_SETTING='setting.py'
app.config.from_envvar('PROJECT_SETTING', silent=True)


# 检查配置信息是否加载成功
print(f"app.config:{app.config}")

# 使用 route() 装饰器告诉 Flask 触发函数的 URL
# 该函数将返回一个字符串，表示用户访问网站时看到的内容
@app.route('/hello')
def hello_world():  # put application's code here
    # 读取配置信息
    print('SECRET_KEY:',app.config.get('SECRET_KEY'))
    return 'Hello World!'

# 在应用中的url_map属性中保存着整个Flask应用的路由映射信息，可以通过读取这个属性获取路由信息
print(app.url_map)

@app.route('/traversal')
def route_map():
    # 遍历所有路由信息
    rules_iterator = app.url_map.iter_rules()
    return json.dumps([{'name': rule.endpoint, 'path': rule.rule} for rule in rules_iterator])


@app.route("/itcast1", methods=["POST"])
def view_func_1():
    return "hello world 1 "

@app.route("/itcast2", methods=["GET", "POST" ])
def view_func_2():
    return "hello world 2 "

# 创建蓝图对象
user_bp = Blueprint('user', __name__)

@user_bp.route('/user_profile')
def get_profile():
    return 'user profile'


# 注册蓝图对象, url_prefix参数指定了蓝图对象中所有路由的URL前缀
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(goods_bp,url_prefix='/goods')
app.register_blueprint(users,url_prefix='/users')
app.register_blueprint(context_bp,url_prefix='/context_bp')
app1.register_blueprint(context_bp1,url_prefix='/context_bp1')


class MobileConverter(BaseConverter):
    def __init__(self, mobile):  # url_map是固定的参数，将整个列表进行带入
        # 调用父类的初始化方法
        super().__init__(mobile)
        self.regex = r'1[3-9]\d{9}'


# 注册自定义转换器
app.url_map.converters['mobile'] = MobileConverter
@app.route('/mobile/<mobile:mobile_num>')
def show_mobile(mobile_num):
    # 显示 /mobile/ 后面的手机号
    return f'mobile: {mobile_num},type:{type(mobile_num)}'


def db_query():
    # g 作为 flask 程序全局的一个临时变量，充当中间媒介的作用，我们可以通过它在一次请求调用的多个函数间传递一些数据。每次请求都会重设这个变量。
    user_id = g.user_id
    user_name = g.user_name
    print('user_id={} user_name={}'.format(user_id, user_name))
    return 'db_query page user_id={},user_name={}'.format(user_id,user_name)

@app.route('/g')
def get_user_profile():
    return db_query()



def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is not None:
            print('Decorator:login_required')
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper

@app.route('/')
def index():
    return 'home page user_id={}'.format(g.user_id)

@app.route('/profile')
@login_required
def get_user_profile():
    return 'user profile page user_id={}'.format(g.user_id)



# 如果__name__注释掉，用flask run启动，否则用python app.py启动
# flask run 等价于 python -m flask run
if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0", port=5001, debug = True)
