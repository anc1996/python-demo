# wagtailblog3/urls.py

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from blog.views import test_search_backend

urlpatterns = [
    path("django-admin/", admin.site.urls),  # Django 管理后台路由
    path("admin/", include(wagtailadmin_urls)),  # Wagtail 管理后台路由
    path("documents/", include(wagtaildocs_urls)),  # Wagtail 文档路由
    path('search/', include('search.urls', namespace='search')),  # 使用 include 而不是直接引用视图
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # 在开发服务器上提供静态文件和媒体文件
    urlpatterns += staticfiles_urlpatterns()  # 添加静态文件路由
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加媒体文件路由

urlpatterns = urlpatterns + [
    path('test-search/', test_search_backend, name='test_search_backend'),
    path('comments/', include('comments.urls', namespace='comments')),
    # 添加博客API URLs
    path('blog/', include('blog.urls', namespace='blog')),
    # 添加归档API URLs
    path('archive/', include('archive.urls')),
    # 对于上面更具体规则没有捕获的任何内容，交由 Wagtail 的页面服务机制处理
    # 这应该是列表中的最后一个模式：
    path("", include(wagtail_urls)),
    # 或者，如果您希望 Wagtail 页面从站点的子路径而不是站点根目录提供：
    #    path("pages/", include(wagtail_urls)),
]