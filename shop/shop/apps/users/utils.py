#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re

from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData


from users.constants import VERIFY_EMAIL_TOKEN_EXPIRES
from users.models import User


# 自定义用户认证的后端：实现多账号登录
def generate_verify_email_url(user_id,user_email):
    """
       生成邮箱验证链接
       :param user: 当前登录用户
       :return: token
    """
    # 创建序列号对象
    # Serializer('密钥，越复杂越安全','过期时间')
    s = Serializer(settings.SECRET_KEY, VERIFY_EMAIL_TOKEN_EXPIRES)
    # 准备待序列号的字典数据
    data={'user_id':user_id,'email':user_email}
    # 调用dumps方法进行序列化，bytes
    ciphertext=s.dumps(data)
    # 返回转成string，序列化的数据,
    token=ciphertext.decode()
    verify_url = settings.EMAIL_VERIFY_URL+'?token=' + token
    return verify_url

def check_verify_email_token(token):
    """
    解密token获取user_id,email信息
    :param token:
    :return:user
    """
    s = Serializer(settings.SECRET_KEY, VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data=s.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email=data.get('email')
        try:
            user=User.objects.get(id=user_id,email=email)
        except User.DoesNotExist:
            return None
        else:
            return user



def get_user_by_account(account):
    """
        通过账号获取账号
        :param account:用户名或者手机号
        :return:user
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # username为手机号
            user = User.objects.get(mobile=account)
        else:
            # username为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

def get_super_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # username为手机号
            user = User.objects.get(mobile=account,is_staff=True)
        else:
            # username为用户名
            user = User.objects.get(username=account,is_staff=True)
    except User.DoesNotExist:
        return None
    else:
        return user




class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户客户端"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写用户认证的方法
        :param request:
        :param username:用户名或者手机号
        :param password:密码明文
        :param kwargs:额外参数
        :return:user
        """
        # 校验username参数是否是用户名还是手机号
        # 如果request不为空，则前台登录
        if request:
            # 使用普通账号查询用户
            user=get_user_by_account(username)
        else:
            # 如果request为空，则后台登录
            user = get_super_user_by_account(username)
        # 如果可以查询到用户，以便于需要校验密码是否正确
        if user and user.check_password(password):
            return user
        else:
            return None
