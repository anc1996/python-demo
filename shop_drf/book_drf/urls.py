#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from rest_framework import routers

from . import views
from .BasicAPIView import apiview,GenericAIPView
from .GenericAPI_Mixin import Generic_modelmixin,Child_ModelMixinAPIView
from .BasicViewSet import viewset,Generic_Viewset
from .ExtendedModelViewSet import modelviewset,ReadOnly_Modelviewset
from .CustomViewSet import DefineViewSet
from .multifunction import AuthPermit,OtherFeatures
from .Pagination import PageNumber_ViewSet,LimitOff_ViewSet
from .CustomExceptions import exception_view



urlpatterns = [
    # 普通序列化视图操作
    re_path(r'^books/$', views.Books.as_view()),
    re_path(r'^book/(?P<pk>\d+)/$', views.Book.as_view()),
    re_path(r'^booksmodel/$', views.BookmodelView.as_view()),

    #  BasicAPIView包
    # APIView是REST framework提供的所有视图的基类，继承自Django的View父类。
    re_path(r'^apibooks/$', apiview.Books.as_view()),
    re_path(r'^apibook/(?P<pk>\d+)/$', apiview.BookView.as_view()),
    # GenericAPIView，继承自APIVIew，增加了对于列表视图和详情视图可能用到的通用支持方法。
    re_path(r'^Gapibooks/$', GenericAIPView.Books.as_view()),
    re_path(r'^Gapibook/(?P<pk>\d+)/$', GenericAIPView.BookView.as_view()),

    # GenericAPI_Mixin包
    # GenericAPIView搭配一个或多个Mixin扩展类的子类视图
    re_path(r'^modelmixinview/$', Generic_modelmixin.Books.as_view()),
    re_path(r'^modelmixinview/(?P<pk>\d+)/$', Generic_modelmixin.BookView.as_view()),
    # 继承GenericAPIView和多个Mixin扩展类的子类视图。
    re_path(r'^childmixinview/$', Child_ModelMixinAPIView.Books.as_view()),
    re_path(r'^childmixinview/(?P<pk>\d+)/$', Child_ModelMixinAPIView.BookView.as_view()),

    # BasicViewSet包
    # ViewSet继承自APIView,它可以需要我们自己实现action方法。
    re_path(r'^viewset/$', viewset.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^viewset/(?P<pk>\d+)/$', viewset.Books.as_view({'get': 'retrieve','put':'update','delete': 'destroy'})),
    # GenericViewSet,继承自GenericAPIView与ViewSetMixi。作用也与GenericAPIVIew类似，它可以需要我们自己实现action方法。
    re_path(r'^GenericViewSet/$',Generic_Viewset.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^GenericViewSet/(?P<pk>\d+)/$', Generic_Viewset.Books.as_view({'get': 'retrieve','put':'update','delete':'destroy'})),

    # ExtendedModelViewSet包
    # ModelViewSet,继承自GenericAPIVIew与5个ModelMixin扩展类的子类视图集，它可以实现自己action方法。
    re_path(r'^ModelViewSet/$', modelviewset.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^ModelViewSet/(?P<pk>\d+)/$', modelviewset.Books.as_view({'get':'retrieve','put':'update','delete': 'destroy'})),
    # ReadOnlyModelViewSet,,继承自GenericAPIVIew与2个只能读取扩展类的子类视图集，它可以需要我们自己实现action方法。
    re_path(r'^ReadonlyModelviewset/$', ReadOnly_Modelviewset.Books.as_view({'get': 'list'})),
    re_path(r'^ReadonlyModelviewset/(?P<pk>\d+)/$', ReadOnly_Modelviewset.Books.as_view({'get': 'retrieve'})),
    
    # 看下面的router的urls
    
    # mutifunction包
    re_path(r'^AuthPermit/$', AuthPermit.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^AuthPermit/(?P<pk>\d+)/$', AuthPermit.Books.as_view({'get':'retrieve','put':'update','delete': 'destroy'})),
    re_path(r'^OtherFeatures/$',OtherFeatures.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^OtherFeatures/(?P<pk>\d+)/$', OtherFeatures.Books.as_view({'get':'retrieve','put':'update','delete': 'destroy'})),

    # Pagination包
    re_path(r'^PageNumber_ViewSet/$',PageNumber_ViewSet.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^PageNumber_ViewSet/(?P<pk>\d+)/$', PageNumber_ViewSet.Books.as_view({'get':'retrieve','put':'update','delete': 'destroy'})),
    re_path(r'^LimitOff_ViewSet/$',LimitOff_ViewSet.Books.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^LimitOff_ViewSet/(?P<pk>\d+)/$', LimitOff_ViewSet.Books.as_view({'get':'retrieve','put':'update','delete': 'destroy'})),

]

# 方法一：可以通过SimpleRouter，
# 该路由器包括标准集合list, create, retrieve, update, partial_update 和 destroy 动作的路由。
# 视图集中还可以使用 @detail_route 或 @list_route 装饰器标记要被路由的其他方法。
simplerouter=routers.SimpleRouter()
'''
router.register(prefix,viewset, basename=None)
    prefix - 用于这组路由的 URL 前缀。
    viewset -必须是 viewset 类。
    basename - 用于创建的 URL名称的基。如果未设置，则将根据视图集的 queryset 属性（如果有）自动生成 basename。
                请注意，如果视图集不包含属性， queryset 则必须在注册视图集时进行设置 basename 。
    prefix：{prefix}/  GET、POST      basename：{basename}-list
    prefix：{prefix}/{lookup}/  GET、PUT、PATCH、DELETE    basename：{basename}-detail
'''

# BasicViewSet包
simplerouter.register(r'SimpleRouter-ViewSet', viewset.Books,basename='SimpleRouter-ViewSet')
simplerouter.register(r'SimpleRouter-GenericViewSet', Generic_Viewset.Books, basename='SimpleRouter-GenericViewSet')
# ExtendedModelViewSet包
# 这里：book_drf/SimpleRouter-ModelViewSet/，^SimpleRouter-ModelViewSet/(?P<pk>[^/.]+)/$
simplerouter.register(r'SimpleRouter-ModelViewSet', modelviewset.Books,basename='SimpleRouter-ModelViewSet')
simplerouter.register(r'SimpleRouter-ReadOnlyModelViewSet', ReadOnly_Modelviewset.Books, basename='SimpleRouter-ReadOnlyModelViewSet')

# CustomViewSet包
simplerouter.register(r'SimpleRouter-DefineViewSet',DefineViewSet.Books,basename='SimpleRouter-DefineViewSet')

# multifunction包
simplerouter.register(r'SimpleRouter-AuthPermit',AuthPermit.Books,basename='SimpleRouter-AuthPermit')
simplerouter.register(r'SimpleRouter-OtherFeatures',OtherFeatures.Books,basename='SimpleRouter-OtherFeatures')
simplerouter.register(r'SimpleRouter-jvbuxianliu',OtherFeatures.BookView,basename='SimpleRouter-jvbuxianliu')

# Pagination包
simplerouter.register(r'SimpleRouter-PageNumber_ViewSet',PageNumber_ViewSet.Books,basename='SimpleRouter-PageNumber_ViewSet')
simplerouter.register(r'SimpleRouter-LimitOff_ViewSet',LimitOff_ViewSet.Books,basename='SimpleRouter-LimitOff_ViewSet')

# print('simplerouter的urls:',simplerouter.urls)
urlpatterns+=simplerouter.urls

# 方法二：DefaultRouter继承SimpleRouter，
# 除了SimpleRouter生成的默认URL配置外，DefaultRouter还额外提供了一个根URL“/”以及一个路由名为“api-root”的根视图。这个根视图可以用于显示API的入口点，并提供了一个浏览API的交互式界面。
# 它还为可选的 .json 样式格式后缀生成路由。
defaultrouter=routers.DefaultRouter()
# BasicViewSet包
defaultrouter.register(r'DefaultRouter-ViewSet', viewset.Books,basename='DefaultRouter-ViewSet')
defaultrouter.register(r'DefaultRouter-GenericViewSet', Generic_Viewset.Books, basename='DefaultRouter-GenericViewSet')

# ExtendedModelViewSet包
defaultrouter.register(r'DefaultRouter-ModelViewSet', modelviewset.Books,basename='DefaultRouter-ModelViewSet')
defaultrouter.register(r'DefaultRouter-ReadOnlyModelViewSet', ReadOnly_Modelviewset.Books, basename='DefaultRouter-ReadOnlyModelViewSet')

# CustomViewSet包
'''/DefaultRouter-DefineViewSet/<function你定义的函数>/  ^DefaultRouter-DefineViewSet/(?P<pk>[^/.]+)/<function你定义的函数>/$'''
defaultrouter.register(r'DefaultRouter-DefineViewSet',DefineViewSet.Books,basename='DefaultRouter-DefineViewSet')

# multifunction包
defaultrouter.register(r'DefaultRouter-AuthPermit',AuthPermit.Books,basename='DefaultRouter-AuthPermit')
defaultrouter.register(r'DefaultRouter-OtherFeatures',OtherFeatures.Books,basename='DefaultRouter-OtherFeatures')
defaultrouter.register(r'DefaultRouter-jvbuxianliu',OtherFeatures.BookView,basename='DefaultRouter-jvbuxianliu')

# Pagination包
defaultrouter.register(r'DefaultRouter-PageNumber_ViewSet',PageNumber_ViewSet.Books,basename='DefaultRouter-PageNumber_ViewSet')
defaultrouter.register(r'DefaultRouter-LimitOff_ViewSet',LimitOff_ViewSet.Books,basename='DefaultRouter-LimitOff_ViewSet')

# CustomExceptions包
defaultrouter.register(r'DefaultRouter-exception_view',exception_view.Books,basename='DefaultRouter-exception_view')
# print('defaultrouter的urls:',defaultrouter.urls)
urlpatterns+=defaultrouter.urls