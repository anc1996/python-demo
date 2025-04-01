from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from book.models import BookInfo
from django.views import View
import json
# 这个文件用于定义视图函数或类。视图是 Django 中的 HTTP 请求处理逻辑，它接收 HTTP 请求并返回 HTTP 响应。
# Create your views here.

"""
视图
1.就是python函数
2.函数的第一个参数就是 请求 和 请求相关的 它是 HttpRequest的实例对象
3.我们必须要返回一个相应   相应是 HttpResponse的实例对象/子类实例对象
"""

def index1(request):
    name = '志玲姐姐 '
    # request, template_name, context=None
    # 参数1: 当前的请求
    # 参数2: 模板文件
    # 参数3:context 传递参数
    print('request请求:', request)
    # 实现业务逻辑
    # 1.先把所有书籍查询出来
    # select * from bookinfo
    # ORM
    books = BookInfo.objects.all().order_by('-name')
    # books = [BookInfo(),BookInfo()]
    # get_queryset()返回一个QuerySet对象，包含所有的对象。
    # 2.组织成字典的数据
    context = {'name': name, 'books': books}
    # 3.将组织号的数据传递给模板
    # for book in books:
    #     print('书籍：', book)
    # 4.模板渲染
    return render(request, 'index1.html', context=context)
    # def render(
    #     request, template_name, context=None, content_type=None, status=None, using=None):
    # 这个函数render是用于渲染一个模板并返回一个Http响应。它接受以下参数：
    #     request：这个参数是Http请求对象，用于传递请求相关的数据和信息。
    #     template_name：这是一个字符串，表示要渲染的模板名称。
    #     context：（可选）一个字典，用于传递给模板的字典对象。默认值为None，表示使用空字典。
    #     content_type：（可选）一个字符串，表示响应的内容类型。默认值为None，表示使用默认的Content - Type。
    #     status：（可选）一个整数，表示响应的状态代码。默认值为None，表示使用默认的状态码。
    #     using：（可选）一个字符串，表示使用的模板引擎。默认值为None，表示使用默认的模板引擎。
    #     return HttpResponse(content, content_type, status)
    # return HttpResponse('index1')

def index(request):
    # 登陆成功之后需要跳转到首页
    # 注册成功之后需要跳转到首页

    '''
    reverse  就是通过 name 来动态获取路径(路由)
          如果没有设置namespace 则可以通过name来获取 reverse(name)
          如果有设置namespace 则可以通过namespace:name来获取 reverse(namespace:name)
    '''
    # 1.动态获取路径参数
    path = reverse('book:index')
    # redirect跳转页面
    print('path:', path) # path: /book/index/
    context='index路径:'+path
    return HttpResponse(content=context)


def detail1(request,category_id, book_id):
    print('request请求:', request)
    # 由于正则表达式有分组位置参数，可获取到分组中的数据，若调换顺序会报错
    print('request请求路径参数:', category_id, book_id)
    context = {'category_id': category_id, 'book_id': book_id}
    return HttpResponse(context.items())

def detail2(request, category_id, book_id):
    ###########################GET 查询字符串#################################
    """
        http://127.0.0.1:8000/detail2/100/110?username=it&password=123
        定义视图接受参数，category_name=math，book_id=100
            以? 作为一个分隔
            ?前边 表示 路由
            ?后边 表示 get方式传递的参数 称之为 查询字符串
            ?key=value&key=value...
            我们在登陆的时候会输入用户名和密码 理论上 用户名和密码都应该以POST方式进行传递
                用 get方式来传递用户名和密码,QueryDict类型的对象用来处理同一个键带有多个值的情况
                get('键',默认值)   如果键不存在则返回None值，可以设置默认值进行后续处理
    """
    query_params = request.GET # request.GET获取请求中的查询字符串数据。
    print('query_params:', query_params)
    # 这种明确的关键字参数传递方式，不会出现位置参数的问题
    print('request请求路径参数:', category_id, book_id)
    # QueryDict 以普通的字典形式来获取 一键多值的是时候 只能获取最后的那一个值
    # 我们想获取 一键一值的化 就需要使用 QueryDict 的get方法
    if len(query_params.getlist('username'))<2 and len(query_params.getlist('password'))<2:
        username=query_params.get('username','none')
        password=query_params.get('password','none')
        data={'category_id': category_id, 'book_id': book_id,'username':username,'password':password}
        context={'一键一值':data}
    else:
    # 比如   detail2/1/1?username=it&password=123&username=python&password=web
        username_list=query_params.getlist('username')
        password_list=query_params.getlist('password')
        data={'category_id': category_id, 'book_id': book_id,'username_list':username_list,'password_list':password_list}
        context={'一键多值':data}
    return HttpResponse(context.items())

def detail3(request):
    ###########################POST 表单数据#################################
    '''
    :param request:
    :return:
    范例：post请求 http://127.0.0.1:8000/book/detail3/
    参数POST body报文体输入参数： username：17688888888;password：123456
    在get params输入参数：search：it
    '''
    query_params_post=request.POST
    query_params_get=request.GET
    # 获取所有不包含在默认值中的值
    custom_params_get = {key:value for key,value in query_params_get.items() if key is not None}
    custom_params_post = {key: value for key, value in query_params_post.items() if key is not None}
    print('query_params_get:', custom_params_get)
    print('query_params_post:',query_params_post)
    context={'query_params_get':custom_params_get,'query_params_post':custom_params_post}
    return HttpResponse(context.items())


def post_json(request):
    ###########################POST json数据#################################
    """
      范例：http://127.0.0.1:8000/book/post_json/
      在body选raw的json，输入下面参数json格式：
      {
          "name":"itcast",
          "password":"cdde"
      }
      """
    request_post=request.POST # <QueryDict: {}>，通过json发送的数据，request.POST是一个空字典
    print('request_post:',request_post)
    request_body=request.body # 得到数据是一个字节类型的数据
    body_decode=request_body.decode() # 解码成字符串
    """
        导入 import json
        json.dumps   将字典转换为 JSON形式的字符串
        json.loads   将JSON形式的字符串转换为字典
    """
    if len(body_decode) <1:
        return HttpResponseBadRequest('没有数据')
    data_dict=json.loads(body_decode) # 将json字符串转换为字典
    print('data_dict:',data_dict)
    return HttpResponse(json.dumps(data_dict),content_type='application/json; charset=utf-8')

def get_header(request):
    ###########################GET 请求头#################################
    """
    范例：http://http://127.0.0.1:8000/book/get_header/
    """
    # META是这个对象的一个属性，它包含了更多的信息，例如请求的路径、端口、HTTP协议版本、cookies、headers等。
    # 这些信息对于理解和处理请求非常有用
    request_meta=request.META
    print(request_meta)
    if len(request_meta)<1:
        return HttpResponseBadRequest('没有数据')

    '''
        元数据里面主要内容：
        CONTENT_TYPE：请求的内容类型，例如"application/json"、"text/html"等。
        HTTP_HOST：请求的主机名和端口号，如果有端口号的话。
        SERVER_PORT：服务器的端口号。
        SERVER_PROTOCOL：服务器使用的协议，例如"HTTP/1.1"、"HTTP/2"等。
        CONTENT_LENGTH：请求的内容长度，以字节为单位。
        HTTP_ACCEPT：客户端能接收的内容类型，例如"application/json"、"text/html"等。
        HTTP_USER_AGENT：客户端的浏览器信息，通常用于识别客户端类型。
        HTTP_REFERER：客户端发出请求的页面的URL。
        HTTP_ACCEPT_ENCODING：客户端能支持的编码方式，例如"gzip"、"deflate"等。
        HTTP_ACCEPT_LANGUAGE：客户端首选的语言，用于返回适合客户端的语言版本的内容。
        HTTP_COOKIE：客户端的Cookie信息。
        HTTP_CONNECTION：客户端期望的服务器连接类型，例如"keep-alive"、"close"等。
        HTTP_CACHE_CONTROL：客户端对缓存的要求，例如"max-age=0"、"no-cache"等。
        HTTP_UPGRADE_INSECURE_REQUESTS：客户端是否升级到HTTPS请求。
        REMOTE_USER：客户端的用户名，通常用于身份验证。
        REMOTE_ADDR：客户端的IP地址。
    '''
    # 定义一个字典，存放所有的请求头字段
    HEADER_FIELDS = {
        'CONTENT_TYPE', 'HTTP_HOST', 'SERVER_PORT', 'SERVER_PROTOCOL', 'CONTENT_LENGTH',
        'HTTP_ACCEPT', 'HTTP_USER_AGENT', 'HTTP_REFERER', 'HTTP_ACCEPT_ENCODING',
        'HTTP_ACCEPT_LANGUAGE', 'HTTP_COOKIE', 'HTTP_CONNECTION', 'HTTP_CACHE_CONTROL',
        'HTTP_UPGRADE_INSECURE_REQUESTS', 'REMOTE_USER', 'REMOTE_ADDR'
    }
    context_dict = {}
    for field in HEADER_FIELDS:
        value = request.META.get(field, 'none')
        context_dict[field] = value

    '''
    method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    user：请求的用户对象。
    path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    encoding：一个字符串，表示提交的数据的编码方式。
    如果为None则表示使用浏览器的默认设置，一般为utf-8。
    这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    FILES：一个类似于字典的对象，包含所有的上传文件。
    '''
    context_json = json.dumps(context_dict)
    # 返回一个json格式的字符串
    return HttpResponse(context_json,content_type='application/json; charset=utf-8')

def response1(request):
    ###########################HttpResponse#################################
    '''
       范例：http://http://127.0.0.1:8000/book/response/
        :param request:
        :return: HttpResponse
    '''
    data = {'name': 'itcast'} #只有name
    # HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
    # content       传递字符串 ,但不能传递对象,字典等数据
    # statue        HTTP status 必须是系统的 100-599
    # content_type  是一个MIME类型，英文全称是Multipurpose Internet Mail Extensions，中文意思是多用途互联网邮件扩展类型
    #               语法形式是: 大类/小类
    #                   text/html   text/css    text/javascript
    #                   application/json
    #                   image/png   image/gif   image/jpeg
    #                   audio/mp3   audio/mp4
    #                   video/mp4   video/avi
    #                   application/pdf application/zip
    #                   application/msword
    context=json.dumps(data)
    return HttpResponse(content=context,status=200,content_type='application/json')

def jsonresponse(request):
    ###########################JsonResponse#################################
    '''
    范例：http://ip:port/book/jsonresponse/
        :param request:
        :return: JsonResponse
    '''
    data = {'name': 'itcast'}
    # 自动将字典转换为json格式的字符串,
    # safe=False  表示可以传递非字典类型的数据，默认True只能传递字典类型的数据
    return JsonResponse(data,safe=True)

def redirect1(request):
    ########################### redirect  #################################
    '''
    范例：http://ip:port/book/tiaozhuan/
    :param request:
    :return: redirect
    
    HttpResponseRedirect 是 Django 中的一个类，直接生成 HTTP 状态码为 302 的响应，用于告诉浏览器重定向到指定的 URL。
    Redirect 类是一个简单的视图函数，底层使用了 HttpResponseRedirect 或 HttpResponsePermanentRedirect。
        可以接受多种类型的输入，包括 URL 字符串、命名路由（reverse）、模型对象等。
    '''
    path = reverse('book:index')
    return redirect(path)

def redirect2(request):
    ###########################  HttpResponseRedirect  #################################
    '''
    范例：http://ip:port/book/tiaozhuan/
    :param request:
    :return: HttpResponseRedirect
    '''
    # 也可以用reverse来获取路径
    return HttpResponseRedirect('/book/index1/')

'''
    HttpResponseRedirect 301:永久重定向
    HttpResponsePermanentRedirect 302:临时重定向
    HttpResponseNotModified 304:未修改
    HttpResponseBadRequest 400:请求错误
    HttpResponseNotFound 404:未找到
    HttpResponseForbidden 403:禁止访问
    HttpResponseNotAllowed 405:不允许的方法
    HttpResponseGone 410:已经不存在
    HttpResponseServerError 500:服务器错误
'''


"""
面试题:
    你是如何理解cookie的? / 你谈一谈cookie/
    1. 概念
    2. 流程 (大体流程,从http角度分析)
    3. 在开发过程中哪里使用了
    4. 你在开发过程中遇到什么印象深刻的地方

保存在客户端的数据叫做 cookie
    1.cookie是保存在客户端
    2.cookie是基于域名(IP)的
    3.cookie是有时间限制的
    4.cookie是有大小限制的
    
    
    流程(原理)
        第一次请求过程
        ① 我们的浏览器第一次请求服务器的时候,不会携带任何cookie信息
        ② 服务器接收到请求之后,发现请求中没有任何cookie信息
        ③ 服务器响应时，在Response Headers响应头设置set_cookie信息返回给浏览器
        ④ 我们的浏览器接收到这个响应之后,浏览器会将cookie信息到保存到本地（浏览器缓存中）
        第二次及其之后的过程
        ⑤ 当我们的浏览器第二次及其之后的请求都会在请求头Request Headers携带cookie信息。
            这里的“携带cookie信息”是指浏览器会自动将之前保存的cookie信息添加到请求头中
        ⑥ 我们的服务器接收到请求之后,会发现请求头Request Headers中携带的cookie信息,这样的话就认识是谁的请求了

"""

def set_cookie(request):
    """
        范例:http://ip:port/book/set_cookie/?username=zhangsan
        :param request:
        :return:
     """
    # 第一次
    # 1.先判断有没有cookie信息
    # 2.获取用户名,设置cookie信息
    # HttpResponse.set_cookie(cookie名, value=cookie值, max_age=cookie有效期)
        # key,value
        # max_age 单位是秒
        # 时间是 从服务器接收到这个请求时间 + 秒数 计算之后的时间
    
    if request.GET.get('username') is None:
        return HttpResponseBadRequest('没有请求参数，设置cookie失败')
    username = request.GET.get('username')
    # 3. 因为我们假设没有cookie信息,我们服务器就要设置cookie信息
    context='设置cookie成功,username:'+username
    response = HttpResponse(content=context)
    # key,value
    response.set_cookie(key='username', value=username,max_age=3600) # max_age=3600,有效期一小时

    # 删除cookie的2种方式
    # response.delete_cookie(key)
    # response.set_cookie(key,value,max_age=0)

    # 4.返回相应
    return response

def get_cookie(request):
    """
    范例:http://ip:port/book/get_cookie/
    :param request:
    :return:
    """
    # ⑤ 当我们的浏览器第二次及其之后的请求都会在请求头携带cookie信息
    # ⑥ 我们的服务器接收到请求之后, 会发现请求中携带的cookie信息, 这样的话就认识是谁的请求了
    #  request.COOKIES 是个字典
    username = request.COOKIES.get('username')
    if username is None:
        return HttpResponseBadRequest('没有cookie信息')
    context='获取cookie成功,username:'+username
    return HttpResponse(content=context)

def del_cookie(request):
    """
    范例:http://ip:port/book/del_cookie/
    :param request:
    :return:
    """
    if request.COOKIES.get('username') is None:
        return HttpResponseBadRequest('没有cookie信息')
    response = HttpResponse(content='删除cookie成功')
    response.delete_cookie('username')
    return response

'''
保存在服务器的数据叫做 session，浏览器禁用cookie，session就无法实现，session是基于cookie的
    0.概念
    1.流程
        第一次请求：
            ① 我们第一次请求的时候可以携带一些信息(用户名/密码)，但是这些信息不会被存储在cookie中。 
            ② 当服务器接收到这个请求之后，进行用户名和密码的验证。如果验证没有问题，服务器会创建一个session，
            并将session信息保存在服务器端。同时，服务器会在响应头中设置一个sessionid的cookie信息。 
            ③ 客户端(浏览器)在接收到响应之后，会将cookie信息保存起来。这个cookie信息是以sessionid为key，value为xxxxx的形式保存的。
        第二次及其之后的请求：
            ④ 第二次及其之后的请求都会携带session id信息。这个session id信息是浏览器在第一次请求时从服务器接收到的，并保存在cookie中的。 
            ⑤ 当服务器接收到这个请求之后，会获取到sessionid信息，然后进行验证。验证成功，则可以获取session信息(session信息保存在服务器端)。    
    从HTTP角度来说，每次请求和响应都遵循HTTP协议。在请求头中，我们可以通过Cookie字段携带cookie信息。在响应头中，我们可以通过Set-Cookie字段设置cookie信息。
'''

def set_session(request):
    '''
    范例:http://ip:port/book/set_session/?username=zhangsan&password=123456
    :param request:
    :return:HttpResponse
    第一次请求流程：
           ① 先判断有没有用户名和密码或者cookie信息
           ② 对用户名和密码的验证,验证没有问题可以设置session信息
           ③ 在设置session信息的同时(session信息保存在服务器端).服务器会在响应头中设置一个sessionid的cookie信息(由服务器自己设置的,不是我们设置的)
           ④ 客户端(浏览器)在接收到响应之后,会将cookie信息保存起来 (保存 sessionid的信息)
    '''
    username = request.GET.get('username')
    cooke_username = request.COOKIES.get('username')
    if username is None and  cooke_username is None:
        return HttpResponseBadRequest('没有请求参数，设置session失败')
    if username is not None:
        request.session['username'] = username # 同时保存到数据库里，
        context = '设置session成功,username:' + username
    else:
        request.session['username'] = cooke_username
        context = '设置session成功,username:' + cooke_username
    return HttpResponse(content=context)
    # 设置成功，浏览器响应头有Set-Cookie:sessionid=ka1szggdmyfhup5eyqkpog1rhy2u9wxu

def get_session(request):
    '''
    范例:http://ip:port/book/get_session/
    :param request:
    :return:HttpResponse
    第二次及其之后的请求流程：
        ⑤ 第二次及其之后的请求都会在请求头携带session id信息
        ⑥ 服务器接收到请求之后,会获取到sessionid信息,然后进行验证。验证成功，则可以获取session信息(session信息保存在服务器端)
    '''
    username = request.session.get('username')
    if username is None:
        return HttpResponseBadRequest('没有session信息')
    context = '获取session成功,username:' + username
    return HttpResponse(content=context)


"""
登陆页面
    GET 请求是获取 登陆的页面
    POST 请求是 验证登陆 (用户名和密码是否正确)
"""
# 我想由2个视图 变为 1个视图
def login1(request):
    '''
    范例：http://ip:port/book/login/
    :param request:
    :return:
    '''
    # GET 请求是获取登陆的页面
    if request.method=='GET':
        # return render() 用render返回页面
        return HttpResponse('GET 请求是获取登陆的页面')
    else:
        return HttpResponse(' # POST 请求是验证登陆 (用户名和密码是否正确)')


"""
面向对象

    类视图 是采用的面向对象的思路
    1.定义类试图
        ① 继承自 View  (from django.views import View)
        ② 不同的请求方式 有不同的业务逻辑
            类试图的方法 就直接采用 http的请求方式的名字 作为我们的函数名.例如: get,post,put,delete
        ③  类试图的方法的第二个参数 必须是请求实例对象
            类试图的方法 必须有返回值 返回值是HttpResopnse及其子类
    原理：在Django中，View是一个视图，它是Django中处理HTTP请求的核心。每个视图函数（或类）都会根据请求的URL和HTTP方法（如GET、POST等）执行相应的代码。
         视图函数通常会渲染一个HTML模板或者返回一个JSON响应。
         通过继承View类，可以创建一个新的视图。新视图可以重写父类的dispatch()方法，以定义自己的URL处理逻辑。
"""


class LoginView(View):
    """类视图：处理注册"""
    def get(self,request):
        '''
        范例：http://ip:port/book/login/
        处理GET请求，返回注册页面
        :param request:
        :return:
        '''
        return render(request,'login.html')

    def post(self,request):
        '''
        范例：http://ip:port/book/login/
        处理POST请求，验证注册信息
        :param request:
        :return:
        '''
        return HttpResponse('POST 请求是验证登陆 (用户名和密码是否正确)')

    def put(self,request):
        return HttpResponse('put')

"""
个人中心页面      --  必须登陆才能显示
GET 方式 展示 个人中心
POST 实现个人中心信息的修改
定义类视图
导入from django.contrib.auth.mixins import LoginRequiredMixin 
# 它用于要求视图进行身份验证，即只有登录用户才能访问该视图。如果用户未登录访问了这个视图，它将重定向到 settings 中指定的登录页面。
"""

from django.contrib.auth.mixins import LoginRequiredMixin

class CenterView(LoginRequiredMixin,View): # 多继承，由于LoginRequiredMixin的方法，如果没有找view视图方法
    
    login_url = reverse_lazy('book:login') # 惰性执行，只有在实际需要时才会解析 URL。
    redirect_field_name = "" # 默认是next，这里修改为
    
    # 范例:http://127.0.0.1:8000/center
    # LoginRequiredMixi判断是否验证用户已登录，若没有登录返回404
    def get(self,request):
        return HttpResponse('个人中心展示')

    def post(self, request):
        return HttpResponse('个人中心修改')

#############################模板############################################
class HomeView(View):
    
    # 范例:http://127.0.0.1:8000/book/home
    # Django自带的模板引擎也是一款功能强大的模板引擎，它与Django框架紧密集成，使用起来非常方便
    def get(self,request):
        username = request.COOKIES.get('username')
        # 2.组织数据
        context = {
            'username': username,
            'age': 14,
            'localtime': datetime.now(),
            'friends': ['tom', 'jack', 'rose'],
            'money': {
                '2019': 12000,
                '2020': 18000,
                '2021': 25000,
            },
            'desc': '<script>alert("这是脚本")</script>'  # 脚本，留意
        }
        return render(request, 'index.html', context=context)

class JinjaView(View):
    # Jinja2是一款非常流行的Python模板引擎，它具有丰富的功能，例如变量、循环、条件语句等。Jinja2的性能也很好，因为它是用Cython编写的。
    '''
    范例:http://127.0.0.1:8000/home
    '''
    def get(self,request):
        # 1.获取数据
        username=request.COOKIES.get('username')
        # 2.组织数据
        context={
            'username': username,
            'age': 14,
            'localtime': datetime.now(),
            'friends': ['tom', 'jack', 'rose'],
            'money': {
                '2019': 12000,
                '2020': 18000,
                '2021': 25000,
            },
            'desc': '<script>alert("这是脚本")</script>'  # 脚本，留意
        }
        return render(request, 'index-jinja2.html', context=context)



class VueView(View):
    def get(self,request):
        return render(request, 'index-vue.html')

    def post(self,request):
        pass
