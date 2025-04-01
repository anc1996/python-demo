"""
URL configuration for bookmanager project.

'urlpatterns' 列表将 URL 路由到视图。有关更多信息，请参阅：
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
例子：
函数视图
    1. 添加导入：从my_app导入视图
    2. 向 urlpatterns 添加 URL：path（''， views.home， name='home'）
基于类的视图
    1. 添加导入：from other_app.views import Home
    2. 向 urlpatterns 添加一个 URL：path（''， Home.as_view（）， name='home'）
包含另一个 URLconf
    1. 导入 include（） 函数： from django.urls import include， path
    2. 向 urlpatterns 添加 URL：path（'blog/'， include（'blog.urls'））
"""
# Django 项目的 URL 声明，就像你网站的“目录”。这个文件是 Django 项目的 URL 配置文件。
from django.contrib import admin
from django.urls import path,re_path,include
"""
1.urlpatterns 是固定写法. 它的值是列表
2.我们在浏览器中输入的路径和会 urlpatterns中的每一项顺序进行匹配
    如果匹配成功,则直接引导到相应的模块.
    如果匹配不成功(把urlpatterns中的每一个都匹配过了),则直接返回404.
3.urlpatterns中的元素 是 re_path
    re_path的第一个参数是: 正则
            r 转义
            ^ 严格的开始
            $ 严格的结尾
4.我们在浏览器中输入的路由 中 哪些部分参与正则匹配?
    http://ip:port/path/?key=value
    我们的http://ip:port/ 和 get、post参数不参与正则匹配

5. 如果和当前的某一项匹配成功,则引导到子应用中继续匹配
    如果匹配成功,则停止匹配返回相应的视图
    如果匹配不成功,则继承和后边的工程中的url的每一项继续匹配,直到匹配每一项,
6.
"""

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

# path(route, view, kwargs=None, name=None)
# 从 Django 3.0 开始，path() 函数已被引入。它接受四个参数，其中两个是必需的：
# route：一个匹配 URL 的字符串。当 Django 匹配到一个请求时，它会从 urlpatterns 的第一项开始，
# 逐个尝试每个模式直到找到一个匹配的。
'''
urlpatterns = [
    path("index/", views.index, name="main-view"),
    # # 这个字符串可以包含角括号（就像上面的 <username>）来捕获 URL 的一部分，并将其作为关键字参数发送给视图。
    path("bio/<username>/", views.bio, name="bio"),  
    path("articles/<slug:title>/", views.article, name="article-detail"),
    # # 角括号可以包含一个转换器规格（像 <int:section> 的 int 部分），它限制了匹配的字符，也可以改变传递给视图的变量的类型。例如，<int:section> 匹配一串十进制数字，并将值转换为 int。
    path("articles/<slug:title>/<int:section>/", views.section, name="article-section"), 
    path("blog/", include("blog.urls")),
    ...,
]
'''
urlpatterns = [
    path("admin/", admin.site.urls),
    # 转到book子应用路由

    # 两种方法：
    # 方法一：用re_path中include((urlconf_module, app_name), namespace='子应用的urls.py文件名')
    # namespace为实例命名空间，通常在创建实例，即 **path(route, include())** 函数中指定；
    # include返回  return (urlconf_module, app_name, namespace)
    re_path(r'^book/',include(('book.urls','book'),namespace='book')  ),
    # 方法二：用path
    # 转到pay子应用路由
    path('pay/',include(('pay.urls','book') ,'book')   ),



]
