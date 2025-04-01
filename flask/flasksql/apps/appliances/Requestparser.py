#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_restful import reqparse

def length_validator(max_length):
    """
    自定义长度验证器工厂函数
    """
    def validate(value, name):
        if len(value) > max_length:
            raise ValueError(f"{name} 长度不能超过 {max_length} 个字符")
        return value
    return validate

class BaseApplianceParser(reqparse.RequestParser):
	
    def __init__(self):
        super(BaseApplianceParser, self).__init__()
        self.add_argument(
            'name',
            type=length_validator(50),
            help='家电名称不能为空',
            required=True,
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'model',
            type=length_validator(50),
            help='家电型号不能为空',
            required=True,
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'description',
            type=length_validator(255),
            help='家电描述',
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'price',
            type=float,
            help='家电价格',
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'country',
            type=length_validator(50),
            help='产地',
            location=['json','args'],
        )
        self.add_argument(
            'stock',
            type=int,
            help='库存',
            location=['json','args'],
        )

# GET请求解析器
class GetApplianceParser(BaseApplianceParser):
    def __init__(self):
        super(GetApplianceParser, self).__init__()
        self.add_argument('page', type=int, help='分页参数', location='args')
        self.remove_argument('name')
        self.remove_argument('model')
        self.remove_argument('description')
        self.remove_argument('price')
        self.remove_argument('country')
        self.remove_argument('stock')
        
        
# POST请求解析器、
class PostApplianceParser(BaseApplianceParser):
    def __init__(self):
        super(PostApplianceParser, self).__init__()

# PUT请求解析器
class PutNewsParser(BaseApplianceParser):
    def __init__(self):
        super(PutNewsParser, self).__init__()
        # 修改 name 和 model 字段为可选
        self.replace_argument(
            'name',type=length_validator(50),help='家电名称',required=False,location=['json','args'],trim=True
        )
        self.replace_argument(
            'model',type=length_validator(50), help='家电型号',required=False,location=['json','args'],trim=True
        )
        
        
class BasePartParser(reqparse.RequestParser):
    def __init__(self):
        super(BasePartParser, self).__init__()
        self.add_argument(
            'name',
            type=length_validator(50),
            help='配件名称不能为空',
            required=True,
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'description',
            type=length_validator(255),
            help='配件描述',
            location=['json','args'],
            trim=True
        )
        self.add_argument(
            'appliance_id',
            type=int,
            help='家电ID',
            location=['json','args'],
        )
        
# GET请求解析器
class GetPartParser(BasePartParser):
    def __init__(self):
        super(GetPartParser, self).__init__()
        self.add_argument('page', type=int, help='分页参数', location='args')
        self.remove_argument('name')
        self.remove_argument('description')
        self.remove_argument('appliance_id')
        
# POST请求解析器
class PostPartParser(BasePartParser):
    def __init__(self):
        super(PostPartParser, self).__init__()
        
# PUT请求解析器
class PutPartParser(BasePartParser):
    def __init__(self):
        super(PutPartParser, self).__init__()
        self.replace_argument(
            'name',type=length_validator(50),help='件名称',required=False,location=['json','args'],trim=True
        )
        self.replace_argument(
            'description',type=length_validator(255),help='配件描述',required=False,location=['json','args'],trim=True
        )
        self.replace_argument(
            'appliance_id',type=int,help='家电ID',required=False,location=['json','args']
        )