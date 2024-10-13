
# flask-bootstrap的使用：

使用flask-bootstrap:
步骤：

1. pip install flask-bootstrap

2. 进行配置：

   ```python
    from flask-bootstrap import Bootstrap
    bootstrap = Bootstrap()
    # 在__init__.py中进行初始化：
   
    ###### 初始化bootstrap
   
    bootstrap.init_app(app=app)
   ```

   

 

3. 内置的block：

   ```python
   {% block title %}首页{% endblock %}
   
   {% block navbar %} {% endblock %}
   
   {% block content %} {% endblock %}
   
   {% block styles %} {% endblock %}
   
   {% block srcipts %} {% endblock %}
   
   {% block head %} {% endblock %}
   
   {% block body %} {% endblock %}
   ```

4. 创建base.py

   ```python
   {% extends "bootstrap/base.html" %}
   {% block title %}首页{% endblock %}
   {% block styles %}
       {{ super() }}
       <style>
          .....
       </style>
   {% endblock %}
   
   {% block navbar %}
   	....
      
   {% endblock %}
   
   {% block content %}
       {% block newcontent %}
           <h1>Hello, Bootstrap</h1>
       {% endblock %}
       {% block footer %}
           <p id="myfoot">京ICP备11008000号-6京公网安备11010802020853</p>
       {% endblock %}
   {% endblock %}
   ```

   

5. 子模板继承父模板：

   ```
   {% extends 'base.html' %}
   {% block title %}
       博客首页
   {% endblock %}
   {% block styles %}
       {{ super() }}
       <style>
         .....
       </style>
   {% endblock %}
   
   {% block newcontent %}
       <div id="container">
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
           <div class="article"></div>
       </div>
   {% endblock %}
   
   ```

   

# 会话机制

## （1）cookie

　　在网站中，HTTP请求是无状态的。也就是说，即使第一次用户访问服务器并登录成功后，第二次请求服务器依然不知道当前发起请求的是哪个用户。cookie的出现就是为了解决这个问题，第一次登录后服务器返回一些数据（cookie）给浏览器，浏览器将这些数据保存在本地。当用户发起第二次请求的时候，浏览器自动的将上次请求得到的cookie数据携带给服务器，服务器通过这些cookie数据就能分辨出当前发起请求的是哪个用户了。cookie存储的数据量有限，不同的浏览器有不同的存储大小，但一般不超过4K，因此使用cookie只能存储一些少量的数据。

## （2）session

　　session与cookie的作用有点类似，都是为了存储用户相关的信息。不同的是，cookie是存储在本地浏览器，session存储在服务器。存储在服务器的数据会更加的安全，不容易被窃取。但存储在服务器也有一定的弊端，就是会占用服务器的资源。

## （3）cookie和session的结合使用

　　web开发发展至今，cookie和session的使用已经出现了一些非常成熟的方案。在如今的市场和企业里，一般有两种存储方式：

- 存储在服务器：通过cookie存储一个session_id，然后具体的数据则保存在session中。当用户已经登录时，会在浏览器的cookie中保存一个session_id，下次再次请求的时候，会把session_id携带上来，服务器根据session_id在session库中获取用户的session数据，从而能够辨别用户身份，以及得到之前保存的状态信息。这种专业术语叫做server side session
- 将session数据加密，然后存储在cookie中。这种专业术语叫做client side session，flask采用的就是这种方式，但是也可以替换成其它形式



## 实现方式：

1. ### cookie方式：

-   保存：

  ```
     通过response对象保存。
      response = redirect(xxx)
      response = render_template(xxx)
      response = Response()
      response = make_response()
      response = jsonify()
      通过对象调用方法
      response.set_cookie(key,value,max_age)
      其中max_age表示过期时间，单位是秒
      也可以使用expires设置过期时间，expires=datetime.now()+timedelta(hour=1)
  ```

  

-   获取：    

  ```
  通过request对象获取。
      request.form.get()
      request.args.get()
      cookie也在request对象中
      request.cookies.get(key) ----> value
  ```

  

-   删除：

     

  ```
   通过response对象删除。 把浏览器中的key=value删除了
      response = redirect(xxx)
      response = render_template(xxx)
      response = Response()
      response = make_response()
      response = jsonify()
     通过对象调用方法
      response.delete_cookie(key)
  ```

  



2. ### session方式：

   session：  是在服务器端进行用户信息的保存。一个字典
   注意：
   使用session必须要设置配置文件，在配置文件中添加SECRET_KEY='xxxxx'，
   添加SECRET_KEY的目的就是用于sessionid的加密。如果不设置会报错。

   -   设置：
         如果要使用session，需要直接导入：
         from flask import session

   ​           把session当成字典使用，因此：session[key]=value
   ​           就会将key=value保存到session的内存空间
   ​            并会在响应的时候自动在response中自动添加有一个cookie：session=加密后的id 

   -   获取
          用户请求页面的时候就会携带上次保存在客户端浏览器的cookie值，其中包含session=加密后的id
          获取session值的话通过session直接获取，因为session是一个字典，就可以采用字典的方式获取即可。
          value = session[key] 或者 value = session.get(key)

     > ​     这个时候大家可能会考虑携带的cookie怎么用的？？？？
     > ​     其实是如果使用session获取内容,底层会自动获取cookie中的sessionid值，
     > ​     进行查找并找到对应的session空间

     

   -    删除
         session.clear()  删除session的内存空间和删除cookie
         del session[key]  只会删除session中的这个键值对，不会删除session空间和cookie

   ---- 5.28 -----

1.短信息发送：


2.登录权限的验证
只要走center路由，判断用户是否是登录状态，如果用户登录了，可以正常显示页面，如果用户没有登录
则自动跳转到登录页面进行登录，登录之后才可以进行查看。

钩子函数：
直接应用在app上：
```python
before_first_request
before_request
after_request
teardown_request
```

应用到蓝图：
```python
before_app_first_request
before_app_request
after_app_request
teardown_app_request
```

3.文件上传