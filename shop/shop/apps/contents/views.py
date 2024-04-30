from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexView(View):
    '''
    首页广告
    '''
    def get(self,request):
        '''提供首页广告页面'''


        # """1、查询并展示商品分类"""
        # channel_group_list=get_categories()
        #
        # """2、查询首页广告数据"""
        # # 第一步：查询所有广告类别
        # contents=OrderedDict()
        # contentCategory_list=ContentCategory.objects.all()
        # for contentCategory in contentCategory_list:
        #     # 查询未下架的广告并排序
        #     content_list=contentCategory.content_set.filter(status=True).order_by('sequence')
        #     contents[contentCategory.key]=content_list
        #     # 第二步：使用广告类别查询出该类别对应的广告内容

        # context={'categories':channel_group_list,'contents':contents}
        # print(reverse('contents:index'))
        return render(request,'index.html')