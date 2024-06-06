#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path,re_path,include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from shop_admin.views import statistical, UsersView, SpecsViewSet, imageViewSet, SkuViewSet, ChannelsViewSet, \
    BrandsViewSet, SpusViewSet, OptionsViewSet, OrdersViewSet, PermissionViewSet, GroupViewSet,AdminViewSet

urlpatterns = [
    # 后台登录，由于django4.1版本In this file, replace ugettext with --> gettext
    re_path(r'^authorizations/$', obtain_jwt_token),
    # 数据统计-用户总量
    re_path(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    # 数据统计-当日增用户统计
    re_path(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    # 数据统计-当日活跃用户统计
    re_path(r'^statistical/day_active/$', statistical.UserActiveCountView.as_view()),
    # 数据统计-当日下单用户量统计
    re_path(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    # 数据统计-当月每天注册的用户量
    re_path(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 数据统计-当日每天用户访问商品分类的量
    re_path(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),

    # 用户管理
    re_path(r'^users/$', UsersView.UserView.as_view()),

    # 商品管理-新增商品规格
    re_path(r'^goods/simple/$', SpecsViewSet.SpecsView.as_view({'get': 'simple'})),
    # # 商品管理-新增SKU图片
    re_path(r'^skus/simple/$', imageViewSet.ImagesView.as_view({'get': 'simple'})),

    # 商品管理-获取SPU商品规格信息
    re_path(r'^goods/(?P<pk>\d+)/specs/$', SkuViewSet.SKUView.as_view({'get': 'specs'})),

    # 商品频道组
    re_path(r'^goods/channel_types/$', ChannelsViewSet.ChannelTypesView.as_view()),
    # 商品频道对应一级分类
    re_path(r'^goods/categories/$', ChannelsViewSet.ChannelCategoriesView.as_view()),

    # spu商品功能-查询所有品牌
    re_path(r'^goods/brands/simple/$', SpusViewSet.SPUGoodsView.as_view({'get': 'brand'})),

    # spu商品功能-查询一级分类
    re_path(r'^goods/channel/categories/$', SpusViewSet.SPUGoodsView.as_view({'get': 'channel'})),

    # spu商品功能-查询二级分类
    re_path(r'^goods/channel/categories/(?P<pk>\d+)/$', SpusViewSet.SPUGoodsView.as_view({'get': 'SecondChannel'})),

    # spu商品功能-上传图片
    re_path(r'^goods/images/$', SpusViewSet.SPUGoodsView.as_view({'post': 'image'})),

    # 规格选项-获取规格信息
    re_path(r'^goods/specs/simple/$', OptionsViewSet.Optionsimple.as_view()),

    # 权限管理-获取权限类型
    re_path(r'^permission/content_types/$', PermissionViewSet.PermissionView.as_view({'get': 'content_types'})),

    # 分组管理-保存分组表权限数据
    re_path(r'^permission/simple/$', GroupViewSet.GroupView.as_view({'get': 'simple'})),
    # 管理员管理-获取分组表数据
    re_path(r'^permission/groups/simple/$', AdminViewSet.AdminView.as_view({'get': 'simple'})),
]

# --规格表路由---
# --规格表路由---
router=DefaultRouter()
# 商品管理-规格管理
router.register('goods/specs',SpecsViewSet.SpecsView,basename='specs')

# 商品管理-SKU图片管理
router.register('skus/images',imageViewSet.ImagesView,basename='images')

# 商品管理-SKU表管理
router.register('skus',SkuViewSet.SKUView,basename='skus')

# 商品管理-频道管理
router.register('goods/channels', ChannelsViewSet.ChannelViewSet, basename='channels')

# 品牌管理
router.register('goods/brands', BrandsViewSet.BrandViewSet, basename='brands')

# spu管理
router.register('goods', SpusViewSet.SPUGoodsView, basename='spu')

# 规格选项功能
router.register('specs/options', OptionsViewSet.OptionViewSet, basename='options')

# orders订单管理
router.register('orders', OrdersViewSet.OrderViewSet, basename='orders')

# 用户管理权限
router.register('permission/perms', PermissionViewSet.PermissionView, basename='perms')
# 分组表管理
router.register('permission/groups', GroupViewSet.GroupView, basename='groups')
# 管理员管理
router.register('permission/admins', AdminViewSet.AdminView, basename='admin')

print(router.urls)
# 添加到urlpatterns
urlpatterns+=router.urls

