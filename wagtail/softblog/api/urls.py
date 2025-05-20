"""
API URL 配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .viewsets import BlogIndexPageViewSet, BlogPageViewSet

# 创建 API 路由器
router = DefaultRouter()
router.register(r'blog-indexes', BlogIndexPageViewSet)
router.register(r'blogs', BlogPageViewSet)

# API 文档配置
schema_view = get_schema_view(
	openapi.Info(
		title="技术博客 API",
		default_version='v1',
		description="基于 Wagtail 的技术博客系统 API",
		terms_of_service="https://www.example.com/terms/",
		contact=openapi.Contact(email="contact@example.com"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	# API 路由
	path('', include(router.urls)),
	
	# JWT 认证
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	
	# API 文档
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]