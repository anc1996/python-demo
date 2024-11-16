#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask_restful import fields

# 新闻输出
news_fields={
	'id':fields.Integer,
	'title':fields.String(attribute='title'),
	'content':fields.String(attribute='content'),
	'news_type_id':fields.Integer(attribute='news_type_id'),
	'update_time':fields.DateTime(attribute='update_time')
}

# 新闻类型输出
newstypes_fields={
	'id':fields.Integer,
	'type_name':fields.String(attribute='type_name'),
	'parent_id':fields.Integer(attribute='parent_id'),
	'update_time':fields.DateTime(attribute='update_time'),
	'is_deleted':fields.Boolean(attribute='is_deleted'),
	'news':fields.List(fields.Nested({
		'id':fields.Integer,
		'title':fields.String(attribute='title'),
		# 限制返回内容100字以内。
		'short_content': fields.String(attribute=lambda x: x.short_content if hasattr(x, 'short_content') else ''),
		'news_type_id':fields.Integer(attribute='news_type_id'),
		'update_time':fields.DateTime(attribute='update_time'),
		# Url将端点名称作为其第一个参数。如果要生成绝对URL，可以使用absolute=True参数。
		'url':fields.Url('news.news_detail',absolute=True) # 生成新闻详情的URL.
	}))
}

message_news_fields={
	'message':fields.String,
	'error':fields.String,
}

# 分页输出
page_fields={
	'page':fields.Integer, # 当前页
	'per_page':fields.Integer, # 每页显示的数量
	'total':fields.Integer, # 总数量
	'pages':fields.Integer, # 总页数
	'has_next':fields.Boolean, # 是否有下一页
	'has_prev':fields.Boolean, # 是否有上一页
	'items':fields.List(fields.Nested(newstypes_fields))
}
