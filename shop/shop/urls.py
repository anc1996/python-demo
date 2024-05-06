"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    # areas
    re_path(r'^', include(('areas.urls','areas'), namespace='areas' )),
]
