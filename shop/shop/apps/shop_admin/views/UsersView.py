from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from shop_admin.serializers import User_serializer
from shop_admin.serializers.PageNum import PageNum
from users.models import User


class UserView(ListCreateAPIView):
    """用户管理"""
    # 权限指定
    permission_classes = [IsAdminUser,]

    # 指定分页器，会调用ModelMixin的list方法
    pagination_class = PageNum

    # 1、要指定当前类视图使用的查询数据
    # 重写get_queryset方法，根据前端是否传递keyword值返回不同查询结果
    def get_queryset(self):
        """查询数据"""
        # 获取前端传递的keyword值
        keyword = self.request.query_params.get('keyword')
        if keyword is None or keyword is '':
            return User.objects.all()
        else:
            return User.objects.filter(username__icontains=keyword)

    # 2、要指定当前视图使用的序列化器
    # serializer_class =User_serializer.UserSerializer
    def get_serializer_class(self):
        # 请求方式是GET，则是获取用户数据返回UserSerializer
        if self.request.method == 'GET':
            return User_serializer.UserSerializer
        else:
            # POST请求，完成保存用户，返回UserAddSerializer
            return User_serializer.UserAddSerializer



