#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_restful import fields

# 定义家零件型输出字段
part_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'description': fields.String
}


# 定义家电输出字段
appliance_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'model': fields.String,
    'description': fields.String,
	'price': fields.Float,
	'country': fields.String,
	'stock': fields.Integer,
    'parts': fields.List(fields.Nested(part_fields))
}

# 定义家电分页输出字段
page_appliance_fields = {
	'page': fields.Integer,
	'per_page': fields.Integer,
	'total': fields.Integer,
	'pages': fields.Integer,
	'has_next': fields.Boolean,
	'has_prev': fields.Boolean,
	'items': fields.List(fields.Nested(appliance_fields))
}

# 定义零件分页输出字段
page_part_fields = {
	'page': fields.Integer,
	'per_page': fields.Integer,
	'total': fields.Integer,
	'pages': fields.Integer,
	'has_next': fields.Boolean,
	'has_prev': fields.Boolean,
	'items': fields.List(fields.Nested(part_fields))
}


# 对更新和创建字段返回信息
message_appliance_fields = {
    'message': fields.String,
    'error': fields.String(default=None, attribute=lambda obj: obj.get('error') if obj.get('error') else None),
    'items': fields.Raw(default=None, attribute=lambda obj: obj.get('items') if obj.get('items') else None)
}

