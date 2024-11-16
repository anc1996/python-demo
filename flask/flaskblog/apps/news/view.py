#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource, marshal_with, marshal
from sqlalchemy.exc import SQLAlchemyError

from apps.news.fields import newstypes_fields, page_fields, news_fields, message_news_fields
from apps.news.model import NewsType, News
from apps.news.parser import GetNewsParser, PostNewsParser, PutNewsParser
from extends import db

# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
news_bp=Blueprint('news',__name__,url_prefix='/news')
news_api=Api(news_bp) # 由蓝图初始化flask-restful对象


class NewsTypeApi(Resource):
	
	def __init__(self):
		self.get_parser=GetNewsParser()
		self.post_parser=PostNewsParser()
		
	# 重写get方法,返回所有新闻类型
	@marshal_with(page_fields)
	def get(self):
		# 查询新闻类型,分页
		args=self.get_parser.parse_args()
		page=args.get('page',1)
		parent_id=args.get('parent_id',None)
		
		# 主查询
		base_query = NewsType.query.filter_by(parent_id=parent_id,is_deleted=0)
		# print("Generated SQL:", str(base_query.statement.compile()))
		page_type = base_query.paginate(page=page, per_page=10)
		return page_type
	
	# 重写post方法,添加新闻类型
	def post(self):
		# 获取请求参数
		"""
		是body中的参数,www-form-urlencoded格式
		:param
		:return:
		"""
		args=self.post_parser.parse_args()
		type_name=args.get('type_name')
		parent_id=args.get('parent_id')
		# 判断是否存在
		type=NewsType.query.filter_by(type_name=type_name).first()
		if type:
			# return {'message': '新闻类型已存在'}, 400
			return marshal({'message': '新闻类型已存在','error':'新闻类型已存在'},message_news_fields), 400
		# 添加新闻类型
		newstype=NewsType(type_name=type_name,parent_id=parent_id)
		try:
			db.session.add(newstype)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return marshal({'message': '数据库操作失败', 'error': str(e)},message_news_fields), 500
		return  marshal(newstype,newstypes_fields), 200


class NewsSimpleTypeApi(Resource):
	
	def __init__(self):
		self.put_parser = PutNewsParser()
		self.patch_parser = PutNewsParser()  # 可以使用相同的解析器，因为它们需要的参数相同
	
	# 重写get方法,返回所有新闻类型
	@marshal_with(newstypes_fields)
	def get(self, id):
		# 查询新闻类型，且这个新闻类型没有被删除
		type = NewsType.query.filter(NewsType.id == id, NewsType.is_deleted == 0).first()
		return type
	
	# 重写put方法,完全替换新闻类型
	def put(self, id):
		# 获取请求参数
		args = self.put_parser.parse_args()
		type_name = args.get('type_name')
		parent_id = args.get('parent_id')
		is_deleted = args.get('is_deleted')
		
		# 查询新闻类型
		type = NewsType.query.get(id)
		if not type:
			return marshal({'message': '新闻类型不存在'}, message_news_fields), 404
		
		# 完全替换新闻类型的属性
		type.type_name = type_name
		type.parent_id = parent_id
		type.is_deleted = is_deleted
		
		try:
			db.session.add(type)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return marshal({'message': '数据库操作失败', 'error': str(e)}, message_news_fields), 500
		
		return marshal(type, newstypes_fields), 200
	
	# 重写patch方法,部分更新新闻类型
	def patch(self, id):
		# 获取请求参数
		args = self.patch_parser.parse_args()
		type_name = args.get('type_name')
		parent_id = args.get('parent_id')
		is_deleted = args.get('is_deleted')
		
		# 查询新闻类型
		type = NewsType.query.get(id)
		if not type:
			return marshal({'message': '新闻类型不存在'}, message_news_fields), 404
		
		# 使用 lambda 表达式简化属性赋值
		update_field = lambda field, value: setattr(type, field, value) if value is not None else None
		
		update_field('type_name', type_name)
		update_field('parent_id', parent_id)
		update_field('is_deleted', is_deleted)
		
		try:
			db.session.add(type)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return marshal({'message': '数据库操作失败', 'error': str(e)}, message_news_fields), 500
		
		return marshal(type, newstypes_fields), 200
	
	# 重写delete方法,删除新闻类型
	@marshal_with(message_news_fields)
	def delete(self, id):
		type = NewsType.query.get(id)
		if not type:
			return {'message': '新闻类型不存在'}, 404
		type.is_deleted = 1
		try:
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return {'message': '数据库操作失败', 'error': str(e)}, 500
		return {'message': '删除成功'}, 200


class NewsDetailApi(Resource):
	
	# 重写get方法,返回新闻详情
	@marshal_with(news_fields)
	def get(self,id):
		# 查询新闻
		news=News.query.get(id)
		return news
	
	# 重写delete方法,删除新闻
	@marshal_with(message_news_fields)
	def delete(self,id):
		news = News.query.filter_by(id=id,is_delete=False).first()
		if not news:
			return {'message': '新闻不存在'}, 404
		try:
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return {'message': '数据库操作失败', 'error': str(e)}, 500
		return {'message': '删除成功'}, 200
		


# 添加资源
news_api.add_resource(NewsTypeApi,'/types',endpoint='newstype')
news_api.add_resource(NewsSimpleTypeApi,'/types/<int:id>',endpoint='newsimpletype')
news_api.add_resource(NewsDetailApi,'/detail/<int:id>',endpoint='news_detail')