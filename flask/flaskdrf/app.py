from flask import Flask,Blueprint

from flask_restful import Api,Resource
from flask import make_response, current_app
from flask_restful.utils import PY3
from json import dumps


from Requestparser import RequestParserResource
from Response_flask import ResponseResource1,ResponseResource2
from decorator_class import *

# 第一步：创建一个Flask应用程序
app = Flask(__name__)
# 第二步：创建一个蓝图对象
user_bp=Blueprint('user',__name__)

# Api⽤来在Flask中创建接⼝
'''
应用程序的主要入口点。
    您需要使用 Flask 应用程序初始化它： 
    >>> app = Flask(__name__)
    >>> api = restful.Api(app)
    
    #     :param app: the Flask application object
    #     :type app: flask.Flask or flask.Blueprint
'''

# api = Api(app)
# 第三步：创建一个API对象
user_api=Api(user_bp)

# 自定义json序列化处理,接口返回的JSON数据具有如下统一的格式
@user_api.representation('application/json')
def output_json(data, code, headers=None):
    """使用 JSON 编码的正文进行 Flask 响应"""

    settings = current_app.config.get('RESTFUL_JSON', {})

    if 'message' not in data:
    # 在此处添加自定义的json序列化处理
        data={
            'message':'ok',
            'data':data
        }

    # 如果我们处于调试模式，并且没有设置缩进，我们将其设置为此处的合理价值。
    # 请注意，这不会覆盖任何现有值已设置。 我们还设置了“sort_keys”值。
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # 始终用新行结束 JSON 转储
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class HelloWorldResource(Resource):
    def get(self):
        return {'get': 'hello world'}

    def post(self):
        return {'post': 'hello world'}

'''
add_resource(resource, *urls, **kwargs)
    为API添加资源。
    参数：
        resource (Resource) – 要添加的资源类。
        urls (str) – 要绑定资源的URL。
        endpoint (str) – 资源的名称，用于生成URL。
        defaults (dict) – 要传递给资源的默认值。
        resource_class_args (tuple) – 传递给资源构造函数的参数。
        resource_class_kwargs (dict) – 传递给资源构造函数的关键字参数。
   例如::
            api.add_resource(HelloWorld, '/', '/hello')
            api.add_resource(Foo, '/foo', endpoint="foo")
            api.add_resource(FooSpecial, '/special/foo', endpoint="foo")
'''


# 第四步：添加资源
user_api.add_resource(HelloWorldResource, '/users/hello')
user_api.add_resource(DemoResource1, '/users/DemoResource1')
user_api.add_resource(DemoResource2, '/users/DemoResource2')

# Requestparser
user_api.add_resource(RequestParserResource, '/users/request')

# Response_flask
user_api.add_resource(ResponseResource1, '/users/response1')
user_api.add_resource(ResponseResource2, '/users/response2')

# 第五步：注册蓝图，蓝图（Blueprint）是一个容器，用于组织相关的路由和视图。
app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
