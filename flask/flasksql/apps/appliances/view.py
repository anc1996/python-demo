#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_restful import  Resource, marshal_with, Api, marshal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from apps.appliances.Requestparser import GetApplianceParser, PostApplianceParser, PostPartParser, GetPartParser
from apps.appliances.fields import page_appliance_fields, message_appliance_fields, appliance_fields, page_part_fields, \
	part_fields
from apps.appliances.model import Appliance, Part
from config import db

appliance_bp = Blueprint('appliances', __name__, url_prefix='/appliance')
appliance_api=Api(appliance_bp)



class ApplianceList(Resource):
    def __init__(self):
        self.get_parser = GetApplianceParser()
        self.post_parser = PostApplianceParser()

    @marshal_with(page_appliance_fields)
    def get(self):
        """获取家电列表"""
        # 查询家电分页
        args = self.get_parser.parse_args()
        page = args.get('page', 1)
        # 主查询
        base_appliances = Appliance.query.paginate(page=page, per_page=10)
        return base_appliances

    @marshal_with(message_appliance_fields)  # 统一使用 message_appliance_fields
    def post(self):
        """新建家电"""
        args = self.post_parser.parse_args()
        name = args.get('name')
        model = args.get('model')
        description = args.get('description')
        price = args.get('price')
        country = args.get('country')
        stock = args.get('stock')

        # 判断是否存在
        appliance = Appliance.query.filter_by(model=model).first()
        if appliance:
            return {'message': '家电已存在', 'error': '家电已存在'}, 400

        # 添加家电
        appliance = Appliance(
            name=name,model=model,description=description,
            price=price,country=country,stock=stock
        )

        try:
            db.session.add(appliance)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {'message': '数据插入失败，可能违反唯一性约束', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': '数据库操作失败', 'error': str(e)}, 500

        # 返回成功信息，将 appliance 放入 items 字段
        return {
            'message': '家电创建成功',
            'items': marshal(appliance, appliance_fields)  # 将 appliance 放入 items 字段
        }, 201


class ApplianceDetail(Resource):
	
	def __init__(self):
		self.get_parser=GetApplianceParser()
		self.post_parser=PostApplianceParser()
	
	@marshal_with(message_appliance_fields)
	def get(self,id):
		"""获取家电详情"""
		# 查询家电详情
		appliance=Appliance.query.get(id)
		if not appliance:
			return {'message': '家电不存在','error':'家电不存在'},404
		return {'message': '家电详情', 'items': marshal(appliance, appliance_fields)}, 200
		
		
	def put(self,id):
		"""更新家电"""
		# 获取请求参数
		args=self.post_parser.parse_args()
		# 判断是否存在
		appliance=Appliance.query.get(id)
		
		if appliance:
			# 如果 name 不为空，则更新 name
			if args.get('name') is not None:
				appliance.name = args.get('name')
			# 如果 model 不为空，则更新 model
			if args.get('model') is not None:
				appliance.model = args.get('model')
			# 如果 description 不为空，则更新 description
			if args.get('description') is not None:
				appliance.description = args.get('description')
			# 如果 price 不为空，则更新 price
			if args.get('price') is not None:
				appliance.price = args.get('price')
			# 如果 country 不为空，则更新 country
			if args.get('country') is not None:
				appliance.country = args.get('country')
			# 如果 stock 不为空，则更新 stock
			if args.get('stock') is not None:
				appliance.stock = args.get('stock')
			try:
				db.session.commit()
			except SQLAlchemyError as e:
				db.session.rollback()
				return {'message': '数据库操作失败', 'error': str(e)}, 500
			return marshal({'message': '家电更新成功', 'items': marshal(appliance, appliance_fields)}, message_appliance_fields), 200
		return {'message': '家电不存在'}, 404
		
	@marshal_with(message_appliance_fields)
	def delete(self,id):
		"""删除家电"""
		# 查询家电详情
		appliance=Appliance.query.get(id)
		if appliance:
			db.session.delete(appliance)
			db.session.commit()
			return {'message': '家电删除成功'}, 200
		return {'message': '家电不存在'}, 404


class PartList(Resource):
	
	def __init__(self):
		self.get_parser=GetPartParser()
		self.post_parser=PostPartParser()
	
	@marshal_with(page_part_fields)
	def get(self):
		"""获取零件列表"""
		# 查询零件分页
		args=self.get_parser.parse_args()
		page=args.get('page',1)
		# 主查询
		base_parts=Part.query.paginate(page=page,per_page=10)
		return base_parts
	
	@marshal_with(message_appliance_fields)
	def post(self):
		"""新建零件"""
		args=self.post_parser.parse_args()
		name=args.get('name')
		description=args.get('description')
		appliance_id=args.get('appliance_id')
		
		# 判断家电是否存在
		appliance=Appliance.query.get(appliance_id)
		if not appliance:
			return {'message': '家电不存在','error':'家电不存在'},404
		
		# 添加零件
		part=Part(name=name,description=description,appliance_id=appliance_id)
		try:
			db.session.add(part)
			db.session.commit()
		except IntegrityError as e:
			db.session.rollback()
			return {'message': '数据插入失败，可能违反唯一性约束', 'error': str(e)}, 400
		except SQLAlchemyError as e:
			db.session.rollback()
			return {'message': '数据库操作失败', 'error': str(e)}, 500
		return {
			'message': '零件创建成功',
			'items': marshal(part, part_fields)
		}, 201

# 添加家电资源路由
appliance_api.add_resource(ApplianceList, '/appliances/')
appliance_api.add_resource(ApplianceDetail, '/appliances/<int:id>/')

# 添加零件资源路由
appliance_api.add_resource(PartList, '/parts/')
