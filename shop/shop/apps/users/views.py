import json
import re,logging

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.backends.base import UpdateError
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.db import DatabaseError
from django_redis import get_redis_connection
from django.urls.base import reverse

from carts.utils import merge_cart_cookie_to_redis
from goods.models import SKU
from shop.utils.views import LoginRequiredJSONMixin
from .constants import USER_ADDRESS_COUNTS_LIMIT, USER_BROWSING_HISTORY_COUNTS_LIMIT, USER_BROWSING_HISTORY_EXPIRES
from .models import User, Address
from shop.utils.response_code import RETCODE,err_msg
from .utils import generate_verify_email_url, check_verify_email_token
from celery_tasks.email.tasks import send_verify_email

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
            redis_conn.delete('sms_%s' % mobile)
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
        try:
            redis_conn.delete('sms_%s' % mobile)
        except Exception as e:
            logger.error(f"从 Redis 中删除 SMS 验证码时出错: {e}")
        
        # 判断用户名是否存在
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
        """
        在请求中保留用户 ID 和后端。这样，用户就不必对每个请求重新进行身份验证。请注意，匿名会话期间的数据集将在用户登录时保留
        该方法包含状态保持
            request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
            request.session[BACKEND_SESSION_KEY] = backend
            request.session[HASH_SESSION_KEY] = session_auth_hash
        这里的backend默认，指定你settings.py中的AUTHENTICATION_BACKENDS中的第一个认证后端
        """
        login(request, user)

        # 5.响应结果：重定向首页
        response=redirect(reverse('contents:index'))
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 用户登录成功，合并cookie购物车到redis购物车
        response=merge_cart_cookie_to_redis(request=request, user=user, response=response)
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
        # 1.接收参数
        username=request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        
        # 2.校验参数
        if not all([username, password]):
            return HttpResponseForbidden('登录时缺少必传参数，响应错误信息，403')
        # 用户名是5-20个字符，[a-zA-Z0-9_-]
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否相同，且密码是否是8-20个字符
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')

        # 3.认证登录用户：使用账号查询用户是否存在，如果用户存在，再校验密码是否正确
        # 这里的request可以判断是否是前台登录和后台登录，转到user.utils.py中制定的UsernameMobileAuthBackend
        # 要在settings.py中指定认证后端
        user=authenticate(username=username,password=password,request=request)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 4.使用remembered，确定状态保持周期
        login(request, user)
        if remembered!='on':
            # 用户没有记住登录：状态保持浏览器会话结束后消失，value单位为秒
            # 如果value为0, the user's session cookie will expire when the user's web browser is closed.
            request.session.set_expiry(0)
        # 记住登录：状态保持信息为保持2周
        else:
            # 如果value为None，那么session有效期将采用系统默认值， 默认为两周,
            request.session.set_expiry(None)

        # 5.响应结果
        # 用户展示：在响应结果之前，先取出next
        next_value=request.GET.get('next')
        # 响应结果
        if next_value:
            # 重定向到next
            response=redirect(next_value)
        else:
            # 重定向到首页
            response = redirect(reverse('contents:index'))

        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中,有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 用户登录成功，合并cookie购物车到redis购物车
        response=merge_cart_cookie_to_redis(request=request, user=user, response=response)
        return response


class LogoutView(View):
    """用户退出登录"""
    def get(self,request):
        """实现用户退出逻辑"""
        # 清楚状态信息
        logout(request)
        # 响应结果,并删除cookie内容
        response=redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class UserInfoView(LoginRequiredMixin,View):
    """用户中心"""

    '''
    LoginRequiredMixin:
        如果一个视图使用了这个混合类，所有非经过身份验证的用户的请求将被重定向到登录页面或显示
         HTTP 403 禁止访问的错误，这取决于 raise_exception 参数的设置。
    '''
    
    def get(self,request):
        """提供用户中心的页面"""
        
        # 判断用户是否登录
        # 你可以设置 AccessMixin 的任何参数来自定义未经授权用户的处理方式：
        # LoginRequiredMixin用法
        # login_url ='/login/'
        # 默认传：login_url = self.login_url or settings.LOGIN_URL==>LOGIN_URL = "/accounts/login/"
        # redirect_field_name = 'redirect_to' # 默认：==> REDIRECT_FIELD_NAME = "next"，回到起点

        # 如果LoginRequiredMixin，判断用户已登录，那么request.user就是登录用户对象
        context={
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return render(request, 'user_center_info.html',context=context)


class EmailView(LoginRequiredJSONMixin,View):
    
    """添加邮箱"""
    
    # LoginRequiredJSONMixin判断用户是否登录
    def put(self,request):
        
        # 1、接受参数
        json_str=request.body.decode() # body类型是bytes类型
        json_dict=json.loads(json_str) # json.loads()将bytes类型转成字典类型
        email=json_dict.get('email')
        
        # 2、校验参数
        if not email:
            return HttpResponseForbidden('缺少email参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return HttpResponseForbidden('参数email有误')

        # 3、将用户传入的邮箱保持到user数据库的email字段中
        try:
            request.user.email=email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':RETCODE.DBERR,'errmsg':'添加邮箱失败'})
        
        # 4、生成密文链接码
        user_id=request.user.id
        verify_url=generate_verify_email_url(user_id,email)
        
        # 5、发送邮箱验证邮件
        send_verify_email.delay(to_email=email,verify_url=verify_url)
        
        # 6、响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class VerifyEmailView(View):
    
    """验证邮箱"""

    def get(self,request):
        
        # 1、接受参数
        token=request.GET.get('token')
        
        # 2、校验参数
        if not token:
            return HttpResponseForbidden('缺少token验证信息')
        # 3、从token中提前用户信息user_id=>user
        user=check_verify_email_token(token)
        
        if not user:
            return HttpResponseBadRequest('无效的请求token')
        
        # 4、将用户的email_active设置为True
        try:
            user.email_active=True
            user.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError('激活邮件失败')
        
        # 5、响应结果：重定向到用户中心
        return redirect(reverse('users:info'))


class CreateAddressView(LoginRequiredJSONMixin, View):
    """新增地址"""

    def post(self,request):
        """实现新增地址逻辑"""
        # 判断是否超过地址上限：最多20个
        # 写法一
        # count=Address.objects.filter(user=request.user,is_deleted=False).count()
        # 写法二
        count=request.user.addresses.filter(is_deleted=False).count()  # 一查多 related_name='addresses'查询
        if count>=USER_ADDRESS_COUNTS_LIMIT:
            return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})
        
        # 接收参数
        json_dict=json.loads(request.body.decode())
        
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')
        
        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg':err_msg[RETCODE.NECESSARYPARAMERR]})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': RETCODE.MOBILEERR, 'errmsg': err_msg[RETCODE.MOBILEERR]})
        if tel and not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
            return JsonResponse({'code': RETCODE.TELERR, 'errmsg': err_msg[RETCODE.TELERR]})
        if email and not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': RETCODE.EMAILERR, 'errmsg': err_msg[RETCODE.EMAILERR]})

        # 保存用户传入的地址信息
        try:
            address=Address.objects.create(
                user=request.user,title=receiver,# 标题默认收货人
                receiver=receiver,province_id=province_id,
                city_id=city_id,district_id=district_id,
                place=place,mobile=mobile,
                tel=tel,email=email)

            # 如果用户没有默认的地址，我们需要指定默认地址
            if not request.user.default_address:
                request.user.default_address=address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
        }
        # 响应新增地址结果：需要将新增的地址返回给前端渲染
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功','address':address_dict})

class AddressView(LoginRequiredMixin,View):
    """展示用户地址页面"""

    def get(self,request):
        """查询并展示用户地址信息"""
        
        login_user=request.user
        # 将模型列表转成字典列表：因为Vue.js不认识模型类型，只有Django和jinja2模板引擎认识
        addresses=Address.objects.filter(user=login_user,is_deleted=False)
        address_list=[]
        for address in addresses:
            address_dict={
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_list.append(address_dict)
            
        # 构造上下文
        context={
            'default_address_id': login_user.default_address_id or '0',
            'addresses': address_list,
        }
        
        return render(request,'user_center_site.html',context=context)

class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):

    def put(self,request,address_id):
        """修改地址"""
        
        # 接收参数
        json_dict = json.loads(request.body.decode())
        required_fields = ["receiver", "province_id", "city_id", "district_id", "place", "mobile"]
        optional_fields = ["tel", "email"]
        
        # 提取必需参数和可选参数，构造字典
        address_data = {key: json_dict.get(key) for key in required_fields + optional_fields}

        # 验证所需参数
        if not all(address_data[key] for key in required_fields):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': err_msg[RETCODE.NECESSARYPARAMERR]})

        # 验证电话设备
        if not re.match(r'^1[3-9]\d{9}$', address_data["mobile"]):
            return JsonResponse({'code': RETCODE.MOBILEERR, 'errmsg': err_msg[RETCODE.MOBILEERR]})

        # 验证可选字段
        if address_data["tel"] and not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', address_data["tel"]):
            return JsonResponse({'code': RETCODE.TELERR, 'errmsg': err_msg[RETCODE.TELERR]})
        if address_data["email"] and not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', address_data["email"]):
            return JsonResponse({'code': RETCODE.EMAILERR, 'errmsg': err_msg[RETCODE.EMAILERR]})


        # 判断地址是否存在,并更新地址信息
        # 使用最新的地址信息覆盖指定的旧的地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=address_data["receiver"],
                **address_data
            )
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新地址失败'})
        
        # 响应新的地址信息给前端渲染
        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查询地址失败'})
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 实现设置地址的逻辑删除：is_delete=True
            address=Address.objects.get(id=address_id)
            address.is_deleted=True
            address.save()
        except Address.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除数据不存在'})
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除数据库失败'})
        # 响应删除地址结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


class DefaultAddressView(LoginRequiredJSONMixin, View):
    """设置默认地址"""

    def put(self,request,address_id):
        """实现设置默认地址的信息"""
        try:
            # 1、接收参数,查询地址
            address = Address.objects.get(id=address_id)
            if address.is_deleted or not address: # 如果地址已经被删除或者地址不存在
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '地址已失效'})
            # 2、设置地址为默认地址
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})

            # 响应设置默认地址结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})

class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    """更新地址标题"""

    def put(self, request, address_id):
        """实现更新受人地址标题的信息"""
        # 接受title信息
        json_str=request.body.decode()
        json_dict=json.loads(json_str)
        title=json_dict.get('title')
        # 校验参数
        if not title:
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少title参数'})
        # 查询当前要更新的地址
        try:
            Address.objects.filter(id=address_id).update(title=title)
        except UpdateError as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置地址标题失败'})
        
        # 响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '设置地址标题成功'})


class ChangePasswordView(LoginRequiredMixin, View):
    """修改密码"""

    def get(self,request):
        """展示修改密码界面"""
        return render(request, 'user_center_pass.html')

    def post(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        # 校验参数
        if not all([old_password, new_password, new_password2]):
            return HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return HttpResponseForbidden('请输入8-20位的密码')
        if new_password!=new_password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        
        # 检验数据库密码
        try:
            request.user.check_password(old_password)
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'origin_password_errmsg': '原始密码错误'})

        # 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_password_errmsg': '修改密码失败'})

        # 清理状态保持信息
        logout(request)
        response = redirect(reverse('users:login'))
        response.delete_cookie('username')
        # 响应密码修改结果：重定向到登录界面
        return response

class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用户浏览记录"""

    def post(self, request):
        """保存用户浏览记录"""
        
        # 1、接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        user_id=request.user.id
        
        # 2、校验参数
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '商品不存在'})
        
        # 3、保存sku_id到redis
        redis_conn = get_redis_connection('history')
        pl = redis_conn.pipeline()  # 管道一次性操作
        """先去重,用于从列表 key 中删除前 count 个值等于 element 的元素。"""
        
        #  lrem(self, name: str, count: int, value: str)
            # count > 0: 从头到尾删除值为 value 的元素。
            # count = 0: 移除所有值为 value 的元素。
        pl.lrem('history_%s' % user_id, 0, sku.id) # 移除所有值为 sku.id 的元素。
        
        # 再存储,将一个或多个值插入到列表 key 的头部。
        # LPUSH mylist a b c，返回的列表是 c 为第一个元素， b 为第二个元素， a 为第三个元素。
        pl.lpush('history_%s' % user_id, sku.id)
        
        # 最后截取,用于修剪(trim)一个已存在的 list，这样 list 就会只包含指定范围的指定元素。
        pl.ltrim('history_%s' % user_id, 0, USER_BROWSING_HISTORY_COUNTS_LIMIT) # 保留最新的5个浏览记录
        
        # 设置history_user_id键的过期时间为6个月
        pl.expire('history_%s' % user_id, USER_BROWSING_HISTORY_EXPIRES)
        pl.execute()
        
        # 4、响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


    def get(self, request):
        """获取用户浏览记录"""
        '''
        {
            "code": "0",
            "errmsg": "OK",
            "skus": [
                {
                    "id": 6,
                    "name": "Apple iPhone 8 Plus (A1864) 256GB 深空灰色 移动联通电信4G手机",
                    "default_image_url": "****/group1/M00/00/02/CtM3BVrRbI2ARekNAAFZsBqChgk3141998",
                    "price": "7988.00"
                },
                ......
            ]
        }
        '''
        user_id=request.user.id
        # 获取Redis存储的sku_id列表信息
        redis_conn = get_redis_connection('history')
        # 从Redis中获取用户的历史浏览记录
        # 返回列表中指定区间内的元素，区间以偏移量 START 和 END 指定。
        # 其中 0 表示列表的第一个元素， -1 表示列表的最后第一个元素
        sku_id_list=redis_conn.lrange('history_%s' % user_id, 0,-1)
        # 根据sku_ids列表数据，查询出商品sku信息
        sku_list = []
        for sku_id in sku_id_list:
            try:
                sku=SKU.objects.get(id=sku_id)
                sku_list.append(
                    {
                        "id": sku.id,
                        "name": sku.name,
                        "default_image_url": sku.default_image.url,
                        "price": sku.price
                    })
            except Exception as e:
                logger.error(e)
                # 如果sku_id不存在，删除sku_id
                redis_conn.lrem('history_%s' % user_id, 0, sku_id)
                
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': sku_list})


