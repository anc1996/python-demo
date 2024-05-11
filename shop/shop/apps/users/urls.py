#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import *


urlpatterns = [
    # 用户注册，反向解析写法：reverse(users:register)
    re_path(r'^register/$', RegisterView.as_view(), name='register'),
    # 判断用户名是否重复注册，反向解析写法：reverse(users:usernamecount)
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view(), name='usernamecount'),
    # 判断手机号是否重复注册，反向解析写法：reverse(users:mobilecount)
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view(), name='mobilecount'),
    # 用户登录，反向解析写法：reverse(users:login)
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    # 用户退出，反向解析写法：reverse(users:logout)
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 用户中心，反向解析写法：reverse(users:info)
    re_path(r'^info/$', UserInfoView.as_view(), name='info'),
    # 添加邮箱，反向解析写法：reverse(users:email)
    re_path(r'^emails/$', EmailView.as_view(),name='emails'),
    # 验证邮箱
    re_path(r'^emails/verification/$', VerifyEmailView.as_view()),
    # 显示用户地址页面
    re_path(r'^addresses/$', AddressView.as_view(), name='address'),
    # 新增用户地址
    re_path(r'^addresses/create/$',CreateAddressView.as_view(),name='createaddress'),
    # 修改和删除用户地址
    re_path(r'^addresses/(?P<address_id>\d+)/$', UpdateDestroyAddressView.as_view()),
    # 设置用户默认地址
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', DefaultAddressView.as_view()),
    # 更新收货人地址的标题
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', UpdateTitleAddressView.as_view()),
    # 修改密码
    re_path(r'^password/$', ChangePasswordView.as_view(), name='pass'),
    # 用户浏览记录
    re_path(r'^browse_histories/$', UserBrowseHistory.as_view()),
]