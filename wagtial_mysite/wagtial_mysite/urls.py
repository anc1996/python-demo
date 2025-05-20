from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from blog import views as blog_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)), # Wagtail 文档管理
    path("search/", search_views.search, name="search"),
    path('testblog/', blog_views.test_blog_index, name='test_blog_index'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # 从开发服务器提供静态和媒体文件
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # 对于上述更具体规则未捕获的任何内容，请交给 Wagtail 的页面服务机制。这应该是这个列表：
    path("", include(wagtail_urls)),
    # 或者，如果您希望从网站的子路径而不是网站根目录提供 Wagtail 页面：
    # path("pages/", include(wagtail_urls)),

]
