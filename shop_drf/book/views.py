import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class Index1View(View):
    def get(self,request):
        # 前后段不分离
        return  render(request,'index.html',context={'name':'python'})


class Index2View(View):
    def get(self,request):
        return JsonResponse({'name':'python'})

class LoginView(View):

    def get(self,request):
        '''
           请求方式：GET
            请求路径：login/?username=python
            请求参数：username
            返回结果：{'message':'ok'} json
        '''
        # 查询用户名操作
        username=request.GET.get('username')
        # 返回结果，
        return JsonResponse({'message':username})

class BookView(View):

    def get(self, request,pk):
        """
            获取单一图书数据接口
            请求方式：GET
            请求路径：books/1/
            请求参数：id
            返回结果：{'btitle':西游记'} json
        """
        return JsonResponse({'btitle':'西游记','id':pk})