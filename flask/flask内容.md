# 课堂纪要

# 1 Flask框架  

 核心 Werkzerug + Jinja2

轻 -> 只提供核心

**最新版本 1.0.2**

## 2 框架对比

问题：

1. DJango与Flask谁好？
2. 对比一下两个框架？

只有更合适的 -> 轻重对比-> 框架选择上 ：

自由、灵活、高度定制 -> Flask

快速实现业务 、不考虑技术选型，越简单直接越好-> Django

# 3 工程搭建

### Django 

   django-admin startproject xxx

   python manage.py startapp users

   python manage.py runserver

## Flask

### 初始化参数

* `import_name`
* static_url_path
* static_folder
* template_folder

### 工程配置参数

* app.config.from_object(配置对象)
   * 继承 —> 优点 复用
   * 敏感数据暴露  缺点
* app.config.from_pyfile(配置文件)
   * 优点 -> 独立文件 保护敏感数据
   * 缺点 -> 不能继承 文件路径固定 不灵活
* app.config.from_envvar('环境变量名')
   * 优点 -> 独立文件 保护敏感数据  文件路径不固定 灵活
   * 缺点-> 不方便 要记得设置环境量
   * 设置环境变量
      * 终端 export
      * pycharm 设置

### Flask新式开发服务器运行 

flask run

## 4 路由

### 查询路由方式：

* flask routes
* app.url_map

### 请求方式

GET

OPTIONS(自带)    -> 简化版的GET请求 用于询问服务器接口信息的

比如接口允许的请求方式  允许的请求源头域名

+ CORS 跨域  django-cors  ->中间件中拦截处理了options请求

+ www.meiduo.site  -> api.meiduo.site/users/1

  + options  api.meiduo.site/uses/1

    返回response  -> allow-origin 'www.meiduo.site'

  * GET api.meiduo.site/users/1

HEAD(自带)  简化版的GET请求

* 只返回GET请求处理时的响应头头，不返回响应体

自定 POST  PUT  DELETE  PATCH

 405 Method not allowed

## 5 蓝图









