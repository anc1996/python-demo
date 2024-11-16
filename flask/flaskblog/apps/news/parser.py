#!/user/bin/env python3
# -*- coding: utf-8 -*-


from flask_restful import reqparse

# 基础解析器
class BaseNewsParser(reqparse.RequestParser):
    def __init__(self):
        super(BaseNewsParser, self).__init__()
        self.add_argument('type_name', type=str, help='新闻类型名称',required=True, location=['args','form'])
        self.add_argument('parent_id', type=int, help='新闻类型父id',required=False,location=['args','form'])
        self.add_argument('type_id', type=int, help='新闻类型id', required=False,location='args')
        self.add_argument('is_deleted', type=bool, help='是否删除',required=False,location=['form'])
		
# GET请求解析器
class GetNewsParser(BaseNewsParser):
    def __init__(self):
        super(GetNewsParser, self).__init__()
        # 修改location为args
        self.add_argument('page', type=int, help='分页参数', location='args')
        self.remove_argument('type_name')
        self.remove_argument('type_id')
	    

# POST请求解析器
class PostNewsParser(BaseNewsParser):
    def __init__(self):
        super(PostNewsParser, self).__init__()
        # 修改location为form
        self.remove_argument('is_deleted')
        self.remove_argument('type_id')
        
# PUT请求解析器
class PutNewsParser(BaseNewsParser):
    def __init__(self):
        super(PutNewsParser, self).__init__()
        self.remove_argument('type_id')
        