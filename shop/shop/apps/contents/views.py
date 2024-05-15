from collections import OrderedDict

from django.shortcuts import render
from django.views import View

from contents.utils import get_categories, get_content

# Create your views here.
class IndexView(View):
    '''
    首页广告
    '''
    def get(self,request):
        '''提供首页广告页面'''

        # """1、查询并展示商品分类"""
        categories=get_categories()

        """2、查询首页广告数据"""
        contents=get_content()

        context={'categories':categories,'contents':contents}
        return render(request,'index.html',context=context)