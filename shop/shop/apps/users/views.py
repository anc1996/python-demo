import re

from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db import DatabaseError
from .models import User

# Create your views here.



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
        # sms_code_client=request.POST.get('sms_code')


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



        # 3.保存注册数据：注册数据业务的核心
        try:
            # password自带哈希加密
            user=User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 4.实现状态保持


        # 5.响应结果：重定向首页
        return HttpResponse('注册成功')