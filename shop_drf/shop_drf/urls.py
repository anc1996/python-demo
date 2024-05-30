"""
URL configuration for shop_drf project.

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
from django.urls import path, re_path,include
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    # 具体定义详见 [Swagger/OpenAPI 规范](https://swagger.io/specification/#infoObject)
    # 该对象用于定义API的元数据, 如API的标题, 版本, 描述, 联系方式, 许可证等信息
    openapi.Info(
        title="Shop_drf API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # public 表示文档完全公开, 无需针对用户鉴权
    public=True,
    # 可以传递 drf 的 BasePermission
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^book/', include('book.urls')),
    re_path(r'^books/', include('books.urls')),
    re_path(r'^book_drf/', include('book_drf.urls')),

    # drf认证：用于用户认证
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # coreapi 接口文档
    re_path(r'^coreapi/', include_docs_urls(title='django-drf title')),

    # drf_yasg
    # SchemaView.without_ui(cache_timeout, cache_kwargs): 返回无UI的视图函数, 该函数可以返回json/yaml格式的swagger文档
        # cache_timeout: 用于指定缓存的生存时间
        # cache_kwargs: 用于指定缓存的参数
    # 例如：http://192.168.20.2:8000/swagger.json
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-spec'),
    # SchemaView.with_ui(renderer, cache_timeout, cache_kwargs): 返回使用指定UI渲染器的视图函数, 可选的UI渲染器有: swagger, redoc。

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger-docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
