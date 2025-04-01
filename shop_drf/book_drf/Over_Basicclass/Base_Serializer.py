#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.exceptions import ValidationError

# 这个是了解整个原理
class BaseSerialier(object):
    """
    BaseSerialier 是一个基本的序列化程序类，它提供了用于验证和保存数据的方法。
        它可以用作其他序列化程序的基类。
    属性：
            instance：要序列化的对象的实例。
            data：要序列化的数据。
    """

    def __init__(self,instance=None,data=None):
        """
        使用实例和数据初始化序列化程序。
        参数：
            instance：要序列化的对象的实例。
            data：要序列化的数据。
        """
        self.instance=instance
        self.data=data

    def validate(self,attrs):
        """
        验证给定属性。此方法应由子类重写，以提供自定义验证。
        参数： attrs：要验证的属性。
        返回：已验证的属性。
        """
        return attrs

    def is_valid(self,raise_exception=False):
        """
        检查数据是否有效。
            参数：raise_exception：如果为 True，则在数据无效时将引发 ValidationError。
            返回：如果数据有效，则为 True，否则为 False。
        """
        data=self.validate(attrs=self.data)
        self.data=data
        if raise_exception and self.errors:
            raise ValidationError(self.errors)
        return not bool(self.errors)

    def save(self):
        """
            保存实例。如果实例已存在，则会对其进行更新。否则，将创建一个新实例。
        """
        if self.instance is not None:
            self.instance=self.update(instance=self.instance,validated_data=self.validated_data)
        else:
            self.instance=self.create(validated_data=self.validated_data)

    def update(self,instance,validated_data):
        """
            使用已验证的数据更新给定实例。此方法应由子类重写，以提供自定义更新逻辑。
            Args:
                instance: The instance to be updated.
                validated_data: The validated data to update the instance with.
        """
        pass

    def create(self,validated_data):
        """
            使用已验证的数据创建新实例。此方法应由子类重写，以提供自定义创建逻辑。
            Args:
                validated_data: The validated data to create the new instance with.
        """
        pass

    @property
    def data(self):
        """
        返回序列化后的数据。
        """
        return self.validated_data

class GenericAPIView(object):

    # 1、要指定当前类视图使用的查询数据
    queryset = None
    # 2、要指定当前视图使用的序列化器
    serializer_class = None

    def get_queryset(self):
        """获取所有查询集"""
        return self.queryset

    def get_object(self):
        """返回视图显示的单一对象。"""
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field


    def get_serializer(self,*args, **kwargs):
        """返回应用于验证和反序列化输入，并用于序列化输出。"""
        
        serializer_class = self.get_serializer_class()
        kwargs = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
            返回用于序列化器的类。
            默认使用“self.serializer_class”。
        """

        return self.serializer_class