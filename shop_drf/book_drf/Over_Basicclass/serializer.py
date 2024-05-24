#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from books.models import BookInfo,PeopleInfo



class PeopleInfoSerializer(serializers.Serializer):
    # 字段选项验证，里面的参数对数据验证，给与通过。
    id = serializers.IntegerField(label='ID', read_only=True)
    gender_text = serializers.SerializerMethodField(help_text='性别')
    name=serializers.CharField(label='英雄名称',max_length=20, help_text='英雄名称')
    description = serializers.CharField(max_length=200, allow_null=True, label='描述信息', help_text='人物描述')

    # 方法一：PrimaryKeyRelatedField，此字段将被序列化为关联对象的主键。返回 是id
    # 包含read_only=True参数时，该字段将不能用作反序列化使用
    # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)

    # 方法二：此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    book=serializers.StringRelatedField()

    is_delete = serializers.BooleanField(default=False, label='人物是否删除')

    # get_gender_text 方法会根据 gender 字段的值从 GENDER_CHOICES 中获取对应的文本，并将其返回。
    def get_gender_text(self, obj):
        return dict(PeopleInfo.GENDER_CHOICES).get(obj.gender, 'unknown')


class BookSerializer(serializers.Serializer):
    # 自定义book序列化器
    """
        read_only:表明该字段仅用于序列化输出，默认False
        write_only:表明该字段仅用于反序列化输入，默认False
        required:表明该字段在反序列化时必须输入，默认True
        default:反序列化时使用的默认值
        allow_null:表明该字段是否允许传入None，默认False
        validators:该字段使用的验证器
        error_messages:包含错误编号与错误信息的字典
        label:用于HTML展示API页面时，显示的字段名称
        help_text:用于HTML展示API页面时，显示的字段帮助提示信息
    """
    # 序列化返回字段
    """注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。"""
    id=serializers.IntegerField(label='ID',required=False, read_only=True)
    name=serializers.CharField(label='名称',max_length=20,help_text='图书名称')
    pub_date=serializers.DateField(label='发布日期',required=False,help_text='发布日期')
    readcount=serializers.IntegerField(label='阅读量',required=False,default=0,help_text='阅读量')
    commentcount=serializers.IntegerField(label='评论量',required=False,default=0,help_text='评论量')
    is_delete=serializers.BooleanField(label='逻辑删除',required=False,default=False)

    # 方法一：返回所关联的人物id read_only只能读取数据，不能修改数据。many=True表示这个字段可以处理多个关联对象
    '''
        "peopleinfo_set": [20,21,22,23]
    '''
    # peopleinfo_set=serializers.PrimaryKeyRelatedField(read_only=True,many=True)

    # 方法二：返回关联人物模型类__str__方法值:模型类定义了：return self.name
    '''
            "peopleinfo_set": ["郭靖","黄蓉","黄药师", "欧阳锋","梅超风"]
    '''
    # peopleinfo_set=serializers.StringRelatedField(read_only=True,many=True)

    # 方法三：返回人物模型类的对象所有属性，
    # 每个BookInfo对象关联的英雄HeroInfo对象可能有多个，只是在声明关联字段时，多补充一个many=True参数即可。
    peopleinfo_set=PeopleInfoSerializer(many=True,required=False,help_text='人物集')


    # 单一字段验证,固定方法,attrs的参数可以随便写,validate_<field_name>,对<field_name>字段进行验证，
    def validate_name(self,value):
        if 'django' in value.lower():
            raise serializers.ValidationError('图书是关于Django的')
        return value


    # 多个字段验证，attrs是一个字典，包含了所有的字段的值
    def validate(self, attrs):
        if attrs['readcount']<attrs['commentcount']:
            raise serializers.ValidationError('readcount<commentcount,可能存在假评论')
        return attrs

    def create(self, validated_data):
        # 字典拆包处理，
        book=BookInfo.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        # 更新数据
        instance.name = validated_data.get('name')
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.readcount = validated_data.get('readcount', instance.readcount)
        instance.commentcount = validated_data.get('commentcount', instance.commentcount)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        # 保存更新后的数据
        instance.save()

        # 返回更新后的实例
        return instance

def about_django(value):
    print('外面的函数验证')

class BookModelSerializer(serializers.ModelSerializer):
    '''
    如果我们想要使用序列化器对应的是Django的模型类，DRF为我们提供了ModelSerializer模型类序列化器来帮助我们快速创建一个Serializer类。
    ModelSerializer与常规的Serializer相同，但提供了
        一、基于模型类自动生成一系列字段
        二、基于模型类自动为Serializer生成validators，比如unique_together
        三、包含默认的create()和update()的实现，帮助实现
    '''

    # 可以向 ModelSerializer 添加额外的字段，也可以通过在类上声明字段来覆盖默认字段，
    readcount=serializers.IntegerField(min_value=20,help_text='阅读量')
    # 短信验证码,validators表示对sms_code执行about_django函数验证
    sms_code=serializers.CharField(max_length=6,min_length=6,validators=[about_django],required=False)
    peopleinfo_set = PeopleInfoSerializer(many=True, required=False,help_text='人物集')
    class Meta:
        # 指定生成字段的模型类
        model=BookInfo

        # 第一种：指定生成字段的模型类
        # fields=('name','readcount','sms_code')
        # 第二种：指定模型类中生成所有的字段
        # fields='__all__'
        # 第三种：指定模型类中除了is_delete字段生成的字段，
        exclude = ('is_delete',)

        # 可以通过read_only_fields指明只读字段，即仅用于序列化输出的字段
        read_only_fields = ('id',)
        # 还可以对字段进行添加和修改
        extra_kwargs={
            'readcount': {'min_value': 10},
            'commentcount':{'min_value':5}
        }

    # 单一字段验证,固定方法,attrs的参数可以随便写,validate_<field_name>,对<field_name>字段进行验证，
    def validate_name(self, value):
        if 'django' in value.lower():
            raise serializers.ValidationError('图书是关于Django的')
        return value

    # 多个字段验证
    def validate(self, attrs):
        if attrs['readcount'] < attrs['commentcount']:
            raise serializers.ValidationError('readcount<commentcount,可能存在假评论')
        return attrs