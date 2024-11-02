
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


验证码:
    步骤：
      1. 生成验证码
       pip install pillow


        from PIL import Image, ImageFont, ImageDraw, ImageFilter
      2. image对象 code验证码
      3.
           /login
           GET:
           渲染
           login.html
               |--- <img src="{{url_for('blog.pic')}}" alt="ABC" style="height:34px;" id="pic">
           POST:
               获取数据
               验证码的匹配
               验证用户和密码（check_password_hash）
               session['uname'] =
               重定向到首页
           /pic
             image对象 code验证码
             将image对象转成二进制
             make_response(buf_bytes)  ---->response
             response.headers['Content-Type']= 'image/jpg'
    
             session['code']=code验证码
             return response

缓存中：
    pip install redis
    pip install flask-caching

    启动redis
    进到redis目录：
       redis-server redis.windows.conf



使用缓存：

    1. Cache对象
    
       from flask-caching import Cache
    
       cache = Cache()
    
    2.
    config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_REDIS_PORT': 6379
    }
    
    def create_app():
        .....
        cache.init_app(app,config)
    
    3. 设置缓存:
       cache.set(key,value,timeout=second)   ----> flask_cache_pic_abc
       cache.set_many([(key,value),(key,value),(key,value),...])
    
       获取缓存值:
       cache.get(key)  --->value
       cache.get_many(key1,key2,...)
    
       删除缓存:
       cache.delete(key)
       cache.delete_many(key1,key2,...)
       cache.clear()
    
    视图函数缓存:
    @app.route("/")
    @cache.cached(timeout=50)
    def index():
        return render_template('index.html')

SMS: 手机验证码
1. 获取验证码：
   1. 输入手机号码
   2. 通过ajax发送请求
   3. 后端： 获取手机号码
      使用requests向第三方的服务端（网易云信）发送请求
      URL https://api.netease.im/sms/sendcode.action
      method： POST
      header:
        headers={}
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        AppSecret = 'ee8d51d1061e'
        Nonce = '74093849032804'
        CurTime = str(time.time())
        headers['AppKey'] = 'cc735ffe22684cc4dab2dc943540777c'
        headers['Nonce'] = Nonce
        headers['CurTime'] = CurTime
        s = AppSecret + Nonce + CurTime
        headers['CheckSum'] = hashlib.sha1(s.encode('utf-8')).hexdigest().lower()
        res = requests.post(url, data={'mobile': phone}, headers=headers)
       4.获取响应对象：
       res.text     文本内容
       res.content  二进制

    5. 转成json对象
       r = json.loads(res.text)

       r.obj  ---> 验证码

       保存到缓存中: cache.set(phone,r.obj)

    6. 返回json结果给ajax

2.登录验证：
   获取手机号码和验证码进行验证
        phone = request.form.get('phone')
        validate = request.form.get('valiadate')
        code = cache.get(phone)
        if code == validate:
            user = User.query.filter(User.phone == phone).first()
            cache.set('uname', user.username)
            session['uname'] = user.username
            return redirect(url_for('blog.index'))
        else:
            flash('手机验证码错误')
            return render_template('login_phonecode.html')

七牛云存储：


nginx:
安装可以参照的路径:
  http://nginx.org/en/linux_packages.html#Ubuntu

# Nginx

启动Nginx
	nginx 	[ -c  configpath]   默认配置目录：/etc/nginx/nginx.conf
信息查看
	nginx 	-v
	nginx	-V
查看进程：
	ps -ef |grep nginx
控制Nginx
	nginx -s signal
		stop 		快速关闭
		quit		优雅的关闭
		reload		重新加载配置

通过系统管理
	systemctl  status  nginx	查看nginx状态
	systemctl  start    nginx	启动nginx服务
	systemctl  stop     nginx   关闭nginx服务
	systemctl  enable nginx	设置开机自启
	systemctl  disable nginx	禁止开机自启

# wtform

flask-wtf:集成了wtform，csrf的保护和文件上传功能，图形验证码。

1。安装：

```SH
pip3 install Flask-WTF
```

全局使用csrf保护，

```python
csrf = CSRFProtect(app=app)
# 必须需要设置SECRET_KEY这个配置项
app.config['SECRET_KEY'] = 'fgfhdf4564'
```

2。定义form.py:

```python
# 在文件中中添加：

class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
```

各种：Field类型

- StringField
- PasswordField
- IntegerField
- DecimalField
- FloatField
- BooleanField
- RadioField
- SelectField
- DatetimeField

各种的验证：

- DataRequired
- EqualTo
- IPAddress
- Length
- NumberRange
- URL
- Email
- Regexp

3.使用：

 视图中：

```python
   .....
   form =UserForm()
   return render_template('user.html',form=form)
```

 模板中：

```html
    <form action='' method=''>
      {{form.csrf_token}}
      {{form.name}}
      {{form.password}}
      <input type='submit' value=''/>
    </form>
```

4.提交验证：

```python
@app.route('/',methods=['GET','POST'])
def hello_world():
 uform = UserForm()
 if uform.validate_on_submit():   ------->主要通过validate_on_submit进行校验
     print(uform.name)
     print(uform.password)
     return '提交成功！'

 return render_template('user.html', uform=uform)
```

## 文件上传：

1。定义form

```python
class UserForm(FlaskForm):
    。。。。。。
    # 上传使用的就是FileField，如果需要指定上传文件的类型需要使用：FileAllowed
    icon = FileField(label='用户头像', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], message='必须是图片文件格式')])
```

2。模板中的使用同其他类型的字段，但是必须在form上面：enctype="multipart/form-data",multipart/form-data 是一种用于在 HTTP 请求中上传文件的编码类型。它允许你在一个表单中同时上传文件和文本数据。使用 multipart/form-data 的主要原因是为了支持文件上传，并且能够处理二进制数据和文本数据。

3。视图函数中如果验证成功，通过：

```python
    icon = uform.icon.data  #  -----》icon是FileStorage类型
    filename = secure_filename(icon.filename)
    icon.save(os.path.join(UPLOAD_DIR, filename))
```

