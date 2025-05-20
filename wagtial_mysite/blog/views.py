from django.shortcuts import render
from .models import BlogIndexPage

def test_blog_index(request):
    blog_index_page = BlogIndexPage.objects.first()  # 获取第一个 BlogIndexPage 对象
    return render(request, 'blog/blog_index_page.html', {'page': blog_index_page})
