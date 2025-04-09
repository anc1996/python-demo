"""
URL 配置 for shop 项目.

`urlpatterns` 列表将 URL 路由到视图函数。 更多信息请查阅:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
例子:
Function views (函数视图)
    1. 添加一个导入:  from my_app import views
    2. 将 URL 添加到 urlpatterns:  path('', views.home, name='home')
Class-based views (基于类的视图)
    1. 添加一个导入:  from other_app.views import Home
    2. 将 URL 添加到 urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf (包含另一个 URLconf)
    1. 导入 include() 函数: from django.urls import include, path
    2. 将 URL 添加到 urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    # users：用户
    re_path(r'^',include(('users.urls','users'),namespace='users')),
    # contents:广告
    re_path(r'^', include(('contents.urls', 'contents'), namespace='contents')),
    # verifications：图形验证码
    re_path(r'^', include(('verifications.urls','verifications'),namespace='verifications')),
    # oauth:第三方登录
    re_path(r'^', include(('oauth.urls','oauth'),namespace='oauth')),
    # areas，区域
    re_path(r'^', include(('areas.urls','areas'), namespace='areas' )),
    # goods，商品模块
    re_path(r'^', include(('goods.urls','goods'), namespace='goods')),
    # haystack，搜索模块
    re_path(r'^search/',include('haystack.urls')),
    # carts，购物车模块
    re_path(r'^', include(('carts.urls', 'goods'), namespace='carts')),
    # orders，订单模块
    re_path(r'^', include(('orders.urls', 'orders'), namespace='orders')),
    # payment，支付模块
    re_path(r'^', include(('payment.urls', 'payment'), namespace='payment')),
    # shop_admin
    re_path(r'^shop_admin/', include(('shop_admin.urls','shop_admin'),namespace='shop_admin')),

]
