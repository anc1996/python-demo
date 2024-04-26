#!/user/bin/env python3
# -*- coding: utf-8 -*-
from book.views import *
from django.urls import re_path,path

# re_path(route, view, kwargs=None, name=None)
    # 它包含一个与 Python 的 re 模块兼容的正则表达式。字符串通常使用原始字符串语法（r''），
    # 因此它们可以包含像 /d 这样的序列，而不需要用另一个反斜杠来转义。
    # 当进行匹配时，从正则表达式中捕获的组会被传递到视图中 ——
    # 如果组是命名的，则作为命名的参数，否则作为位置参数。值以字符串的形式传递，不进行任何类型转换。
'''
urlpatterns = [
    re_path(r"^index/$", views.index, name="index"),
    re_path(r"^bio/(?P<username>\w+)/$", views.bio, name="bio"),
    re_path(r"^blog/", include("blog.urls")),
'''

urlpatterns = [
#index/
    # url的第一参数是:正则
    # url的第二参数是:视图函数名
    re_path(r'index1/$', index1),
    # name是url的别名，我们可以通过name找到这个路由
    re_path(r'index/$', index,name='index'),
    # /1/100 位置参数，这里分组来获取正则中的数据。
    re_path(r'detail1/(\d+)/(\d+)/$',detail1,name='detail1'),# 不建议这种方法，因为位置参数不直观
    # /category_id/book_id/ 关键字参数，推荐使用
    re_path(r'detail2/(?P<category_id>\d+)/(?P<book_id>\d+)/$',detail2,name='detail2'),
    # post请求
    re_path(r'detail3/$',detail3,name='detail3'),
    # post__json请求
    re_path(r'post_json/$',post_json,name='post_json'),
    # get_header请求
    re_path(r'get_header/$',get_header,name='get_header'),
    # response返回
    re_path(r'response/$',response1,name='response1'),
    # jsonresponse返回
    re_path(r'jsonresponse/$',jsonresponse,name='jsonresponse'),
    # redirect视图重定向
    re_path(r'redirect1/$',redirect1,name='redirect1'),
    # HttpResponseRedirect视图重定向
    re_path(r'redirect2/$',redirect2,name='redirect2'),
    # set_cookie设置cookie
    re_path(r'set_cookie/$',set_cookie,name='set_cookie'),
    # get_cookie获取cookie
    re_path(r'get_cookie/$',get_cookie,name='get_cookie'),
    # del_cookie删除cookie
    re_path(r'del_cookie/$',del_cookie,name='del_cookie'),
    # set_session 设置session
    re_path(r'set_session/$', set_session, name='set_session'),
    # get_session 获取session
    re_path(r'get_session/$',get_session,name='get_session'),
    # login1  # 根据method判断请求方式
    re_path(r'login1/$',login1,name='login1'),
    # loginView 是as_view视图函数名，根据请求方法调用
    re_path(r'login/$',LoginView.as_view(),name='login'),
    # CenterView
    re_path(r'center/$',CenterView.as_view(),name='center'),
    # HomeView,django的template模板语法
    path('home/',HomeView.as_view(),name='home'),
    # JinjiaView，jinja模板语法
    path('jinja/',JinjaView.as_view(),name='jinja'),
    # vue模板
    path('vue/',VueView.as_view(),name='vue'),
]
