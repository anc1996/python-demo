# blog/urls.py
from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('search/', views.search, name='search'), # 搜索功能
    path('advanced-search/', views.advanced_search_view, name='advanced_search'), # 高级搜索功能
    path('api/search/', views.api_search, name='api_search'), # API搜索功能
    path('category/<slug:category_slug>/', views.BlogCategoryView.as_view(), name='category'), # 分类视图
    path('tag/<str:tag>/', views.BlogTagView.as_view(), name='tag'), # 标签视图
    path('archive/', views.BlogArchiveView.as_view(), name='archive'), # 归档视图
    path('archive/<int:year>/<int:month>/', views.BlogArchiveView.as_view(), name='archive_month'), # 按月归档视图
]