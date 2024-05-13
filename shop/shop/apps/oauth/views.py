import logging
import re

from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django_redis import get_redis_connection

from carts.utils import merge_cart_cookie_to_redis
from users.models import User
from .QQLoginTool.QQtool import OAuthQQ
from shop.utils.response_code import RETCODE
from .models import OAuthQQUser
from .utils import generate_access_token, check_access_token


# Create your views here.
class QQAuthURLView(View):
    """
    提供QQ登录页面网址
    链接：https://graph.qq.com/oauth2.0/authorize?
            response_type=token&
            client_id=appid&
            redirect_uri=(注册appid时填写的主域名下的地址)&
            state=next :表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
    """
    def get(self,request):

        next=request.GET.get('next')
        print('next原先地址:',next)
        # 创建工具对象

        # 生产QQ登录扫描页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        # QQ第一步：获取Authorization Code
        login_url = oauth.get_qq_url()
        # 响应结果
        return JsonResponse({'code':RETCODE.OK,'errmsg':'OK','login_url':login_url})

class QQAuthUserView(View):

    """qq扫码登录后的回调处理"""
    def get(self,request):
        # 1.获取回调后的code码
        code=request.GET.get('code')
        if code is None:
            return HttpResponseServerError('获取code失败')
        """
        QQ第二步：通过Authorization Code获取Access Token
            https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&
            client_id=appid&client_secret=appkey&code=(*****)&redirect_uri=(注册appid时填写的主域名下的地址)
            例如：
            http://ov-vo.cn/oauth_callback?code=486F2****9AC4&state=next
        """
        # 2.创建QQ工具对象
        oauth=OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token=oauth.get_access_token(code)
            """QQ第三步：通过access_token获取openid"""
            openid=oauth.get_open_id(access_token)
        except Exception as e:
            logger.error('错误信息:%s'% e )
            return HttpResponseServerError('OAuth2.0认证失败')

        # 使用openid 该qq用户是否绑定过美多商城的用户
        try:
            oauth_qq_user=OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist as e:
            # openid未绑定用户
            """oauth_callback.html的access_token_openid网页记录openid"""
            # openid加密发送到密文发送到网页
            access_token_openid=generate_access_token(openid)
            context={'access_token_openid':access_token_openid}
            return render(request,'oauth_callback.html',context=context)
        else:
            # openid已绑定用户,oauth_user.user从qq模型类找到对应的user模型类对象
            login(request,oauth_qq_user.user)
            '''响应结果：重定向首页'''
            # 将用户名写入cookie中
            next = request.GET.get('state')
            response = redirect(next)
            # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
            response.set_cookie('username', oauth_qq_user.user.username, max_age=3600 * 24 * 15)

            # 用户登录成功，合并cookie购物车到redis购物车
            response = merge_cart_cookie_to_redis(request=request, user=oauth_qq_user.user, response=response)

            return response

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 1.接收参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')

        # 2.校验参数
        # 判断参数是否齐全
        if not all([mobile, password, sms_code_client]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('VerifyCode')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        print(sms_code_server)
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '输入短信验证码有误'})
        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': '失效的openid'})

        # 使用手机号查询对应的用户是否存在
        try:
            user=User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 如果用户不已存在，新建用户
            user=User.objects.create_user(username=mobile,password=password,mobile=mobile)
        else:
            # 如果用户已存在，需要校验登录密码
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        # 将用户绑定到openid
        try:
            oauth_qq_user=OAuthQQUser.objects.create(user=user,openid=openid)
        except Exception as e:
            logger.error(e) # 打印日志
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ登录失败'})
        # 实现状态保持
        login(request, oauth_qq_user.user)
        '''响应结果：重定指定回调的位置'''
        # 将用户名写入cookie中
        next=request.GET.get('state')
        response = redirect(next)
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
        response.set_cookie('username', oauth_qq_user.user.username, max_age=3600 * 24 * 15)

        # 用户登录成功，合并cookie购物车到redis购物车
        response = merge_cart_cookie_to_redis(request=request, user=oauth_qq_user.user, response=response)

        return response



# 创建日志输出器
logger=logging.getLogger('oauth')