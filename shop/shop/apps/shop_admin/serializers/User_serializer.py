import re

from rest_framework.serializers import ModelSerializer,ValidationError

from users.models import User


class UserSerializer(ModelSerializer):
    # 查看用户序列号器
    class Meta:
        model=User
        fields=('id','username','mobile','email')


class UserAddSerializer(ModelSerializer):


    # 增加用户序列号器
    class Meta:
        model=User
        # id 默认是read-only，不参与序列号操作
        fields=('id','username','mobile','email','password')
        #  username字段增加长度限制，password字段只参与保存，不在返回给前端，增加write_only选项参数
        extra_kwargs = {
            'username': {'max_length': 20,'min_length': 5},
            'password': {'max_length': 20,'min_length': 8,'write_only': True},
        }

    # 手机验证
    def validate_mobile(self,vaule):
        if not re.match(r'^1[3-9]\d{9}$', vaule):
            raise ValidationError('手机号格式不匹配')
        return vaule

    # 邮箱验证
    def validate_email(self, value):
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', value):
            raise ValidationError('邮箱格式不匹配')
        return value

    # 由于父类没有加密密码，重写ModelSerializer的create方法
    def create(self, validated_data):
        # 保存用户数据并对密码加密
        # 方法一
        user = User.objects.create_user(**validated_data)
        return user

        # 方法二：
        # # 调用父类的create方法，根据validated_data创建一个用户对象。
        # user=super().create(validated_data)
        # # 将用户密码进行加密存储。
        # user.set_password(validated_data['password'])
        # user.save()
        # return user
