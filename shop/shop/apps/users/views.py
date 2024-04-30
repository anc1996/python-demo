import re,logging

from django.contrib.auth import login
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db import DatabaseError
from django_redis import get_redis_connection
from django.urls.base import reverse

from .models import User
from shop.utils.response_code import RETCODE
# Create your views here.

# 创建日志输出器
logger=logging.getLogger('users')

# Create your views here.
''' 1、提供用户注册页面,判断用户名是否重复注册,判断手机号是否重复注册
    2、提供登录页面
    3、退出登录
    4、展示首页用户名信息
    5、判断是否登录，为用户中心和我的订单做准备
    6、展示，用户中心
    7、添加邮箱,验证邮箱
    8、新增、删除、修改用户收获地址，设置用户默认地址，修改收货人地址的标题
    9、用户浏览记录
'''

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用username查询对应的记录的条数
        count=User.objects.filter(username=username).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self,request,mobile):
        """
        :param request:请求对象
        :param mobile:手机号
        :return:JSON
        """
        count=User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

class RegisterView(View):

    def get(self, request):
        """
         提供注册界面
         :param request: 请求对象
         :return: 注册界面
         """
        return render(request, 'register.html')


    def post(self,request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """
        # 1.接收参数：表单参数
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile=request.POST.get('mobile')
        allow = request.POST.get('allow')
        sms_code_client=request.POST.get('sms_code')


        # 2.校验参数：前后端校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全。
        # 判断参数是否齐全，all([list]):会去校验列表中元素是否存在空值，若为空，false
        if not all([username,password,password2,mobile,allow]):
            return HttpResponseForbidden('如果缺少必传参数，响应错误提示信息，403')
        # 判断用户名是否是5-20个字符
        if not re.match('^[a-zA-Z0-9_-]{5,20}$',username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个字符
        if not re.match('^[0-9A-Za-z]{8,20}$',password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次输入的密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match('^1[3-9]\d{9}$',mobile):
            return HttpResponseForbidden('请输入正确的手机号码')

        # 判断用户是否勾选用户协议，发送过来html是on的字符串
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议')

        # 判断短信验证码是否输入正确验证码
        redis_conn=get_redis_connection('VerifyCode')
        sms_code_server=redis_conn.get('sms_%s' % mobile).decode()
        if sms_code_server is None:
            return render(request,'register.html', {'sms_code_errmsg': '短信验证码已失效'})
        if sms_code_server!=sms_code_client:
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
        try:
            redis_conn.delete('sms_%s' % mobile)
        except Exception as e:
            logger.error(e)
        count = User.objects.filter(username=username).count()
        mobile_count=User.objects.filter(mobile=mobile).count()
        if count!=0:
            return render(request, 'register.html', {'register_errmsg': '用户名已存在'})
        if mobile_count!=0:
            return render(request, 'register.html', {'register_errmsg': '手机号已存在'})


        # 3.保存注册数据：注册数据业务的核心
        try:
            # password自带哈希加密
            user=User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            logger.error(DatabaseError)
            return render(request, 'register.html', {'register_errmsg': '注册失败'})


        # 4.实现状态保持
        # 在请求中保留用户 ID 和后端。这样，用户就不必对每个请求重新进行身份验证。请注意，匿名会话期间的数据集将在用户登录时保留
        # 该方法包含状态保持
                # request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
                # request.session[BACKEND_SESSION_KEY] = backend
                # request.session[HASH_SESSION_KEY] = session_auth_hash
        login(request, user)

        # 5.响应结果：重定向首页
        response=redirect(reverse('contents:index'))
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


class LoginView(View):
    """用户登录"""

    def get(self,request):
        """
        提供用户登录页面
        :param request:
        :return:render()登录页面
        """
        return render(request,'login.html')

    def post(self,request):
        """
        实现用户登录逻辑
        :param request:
        :return:
        """
        # 接收参数
        # username=request.POST.get('username')
        # password = request.POST.get('password')
        # remembered = request.POST.get('remembered')
        # # 校验参数
        # if not all([username, password]):
        #     return HttpResponseForbidden('登录时缺少必传参数，响应错误信息，403')
        # # 用户名是5-20个字符，[a-zA-Z0-9_-]
        # if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
        #     return HttpResponseForbidden('请输入5-20个字符的用户名')
        # # 判断密码是否相同，且密码是否是8-20个字符
        # if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
        #     return HttpResponseForbidden('请输入8-20位的密码')
        # # 认证登录用户：使用账号查询用户是否存在，如果用户存在，再校验密码是否正确
        # user=authenticate(username=username,password=password,request=request)
        # if user is None:
        #     return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
        # # 使用记住用户，确定状态保持周期
        # login(request, user)
        # if remembered!='on':
        #     # 用户没有记住登录：状态保持浏览器会话结束后消失，value单位为秒
        #     request.session.set_expiry(0)
        #     # 如果value为0, the user's session cookie will expire when the user's web browser is closed.
        # else: # 记住登录：状态保持信息为保持2周
        #     request.session.set_expiry(None) # 如果value为None，那么session有效期将采用系统默认值， 默认为两周,
        # # 用户展示：在响应结果之前，先取出next
        # next_value=request.GET.get('next')
        # # 响应结果
        # if  next_value:
        #     # 重定向到next
        #     response=redirect(next_value)
        # else:
        #     # 重定向到首页
        #     response = redirect(reverse('contents:index'))
        # # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
        # response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        #
        # # 用户登录成功，合并cookie购物车到redis购物车
        # response=merge_cart_cookie_to_redis(request=request, user=user, response=response)
        # return response
