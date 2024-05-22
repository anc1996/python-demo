#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from books.models import BookInfo
# class PeopleInfoSerializer(serializers.Serializer):
#     GENDER_CHOICES = ((0, 'male'),(1, 'female'))
#     # 1、一种方法字段选项验证
#     id = serializers.IntegerField(label='ID', read_only=True)
#     name=serializers.CharField(label='书名',max_length=20, help_text='书名')
#     description = serializers.CharField(max_length=200, allow_null=True, label='描述信息', help_text='图书介绍')
#     # PrimaryKeyRelatedField，此字段将被序列化为关联对象的主键。
#     # 包含read_only=True参数时，该字段将不能用作反序列化使用
#     # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
#     # 此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
#     book=serializers.StringRelatedField()
#     is_delete = serializers.BooleanField(default=False, label='逻辑删除')
#
# def about_django(value):
#     print('外面的函数验证')

class BookSerializer(serializers.Serializer):
    # 自定义book序列化器


    # 序列化返回字段
    """注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。"""
    id=serializers.IntegerField(label='ID', read_only=True)
    name=serializers.CharField(label='名称',max_length=20)
    pub_date=serializers.DateField(label='发布日期')
    readcount=serializers.IntegerField(label='阅读量', required=False,default=0)
    commentcount=serializers.IntegerField(label='评论量', required=False,default=0)
    is_delete=serializers.BooleanField(label='逻辑删除',required=False)
    # 返回所关联的人物id
    # peopleinfo_set=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    # 返回关联人物模型类__str__方法值
    # peopleinfo_set=serializers.StringRelatedField(read_only=True,many=True)
    # 返回人物模型类的对象所有属性，
    # 每个BookInfo对象关联的英雄HeroInfo对象可能有多个，只是在声明关联字段时，多补充一个many=True参数即可。
    # peopleinfo_set=PeopleInfoSerializer(many=True,required=False)


    # 单一字段验证,固定方法,attrs的参数可以随便写,validate_<field_name>,对<field_name>字段进行验证，
    # def validate_name(self,value):
    #     if 'django' in value.lower():
    #         raise serializers.ValidationError('图书是关于Django的')
    #     return value


