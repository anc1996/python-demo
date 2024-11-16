#!/user/bin/env python3
# -*- coding: utf-8 -*-
from werkzeug import datastructures
from flask_restful import Resource, fields, marshal_with, Api, reqparse, marshal
from flask import Blueprint, request, url_for, current_app

from apps.goods.model import Goods, UserGoodsAssociation
from extends import db
from extends.file_function import upload_file

# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
goods_api=Api(goods_bp) # 由蓝图初始化flask-restful对象


# 方法二：
def register_resource(route, endpoint):
    def decorator(resource_class):
        goods_api.add_resource(resource_class, route, endpoint=endpoint)
        return resource_class
    return decorator

class IsDeletedFiedls(fields.Raw):
	# 重新定义format方法，用于格式化字段的值
	def format(self, value):
		return '删除' if value else '未删除'

class UpdateTimeFields(fields.Raw):
	# 重新定义format方法，将时间格式化为字符串
	def format(self, value):
		return value.strftime('%Y-%m-%d %H:%M:%S')



# 用户找商品
resource_goods_fields = {
	'id': fields.Integer,
	# attribute:序列化时的字段名，default:默认值
	'good_name': fields.String(attribute='name',default='匿名'),
	'good_price': fields.Float(attribute='price',default=0.0),
	# 方法二：lambda表达式
	'good_description': fields.String(attribute=lambda obj: obj.description, default='暂无描述'),
	'update_time': UpdateTimeFields(attribute='update_time'),
	'IsDelete':IsDeletedFiedls(attribute='is_deleted',default=False),
	# 方法三：自定义字段
	'url': fields.Url('goods.single_good',absolute=True),
	'ImageUrl':fields.String(attribute='ImageUrl')
}


# 定义成功消息的字段
success_message_fields = {
    'msg': fields.String,
	# Nested:嵌套字段可以将平面数据对象转换为嵌套响应
    'good': fields.Nested(resource_goods_fields)
}

# 参数解析
parser=reqparse.RequestParser(bundle_errors=True) # 创建参数解析对象
# 添加参数,type:参数类型，required:是否必须，help:错误提示信息，location:参数位置
parser.add_argument('name',type=str,required=True,help='必须输入商品名称',location=[ 'form'])
parser.add_argument('price',type=float,required=True,help='必须输入商品价格',location=['form'])
parser.add_argument('description',type=str,required=False,help='输入商品描述',location=['form'])
parser.add_argument('image',type=datastructures.FileStorage, help='上传商品图片',location='files')

@register_resource('/all_goods', 'all_goods')
class goodsResource(Resource):
	
	@marshal_with(resource_goods_fields)
	def get(self):
		goodlist = Goods.query.all()
		# 将每个 Goods 对象序列化成字典
		return goodlist
	
	# post
	def post(self):
		args = parser.parse_args()  # 解析参数
		name=args.get('name')
		price=args.get('price')
		# 验证参数值是否存在
		if not all([name,price]):
			return {'msg': '参数不完整','good':None},400
		description=args.get('description')
		image=args.get('image')

		# 查找这个商品是否存在
		good=Goods.query.filter(Goods.name==name).first()
		if good:
			return {'msg': '商品已存在','good':None},400
		# 创建商品对象
		good=Goods(name=name,price=price,description=description)
		# 添加到数据库
		try:
			db.session.add(good)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {'msg': '商品添加失败','good':None},400
		if image:
			# 上传图片
			minio_file_path, error_msg = upload_file(image,good.id , current_app.config['IMAGE_ALLOWED_EXTENSIONS'],'goods/images','image')
			if error_msg:
				return {'msg': '{}，但good已保存，图片没保存。'.format(error_msg),'good':good},200
			good.image=minio_file_path
			db.session.add(good)
			db.session.commit()
		return marshal({'msg': '商品添加成功','good':good},success_message_fields),201
	
	# put
	def put(self):
		return {'msg': '------>put'}
	
	# delete
	def delete(self):
		return {'msg': '------>delete'}

@register_resource('/good/<int:id>', 'single_good')
class goodSimpleResource(Resource):
	
	@marshal_with(resource_goods_fields)
	def get(self, id):
		good = Goods.query.get(id)
		return good
	
		
	
	# put
	def put(self, id):
		return {'endpoint的使用': url_for('all_goods')}
	
	# delete
	def delete(self, id):
		return {'msg': '------>delete'}

# 方法一：
# goods_api.add_resource(goodsResource, '/all_goods', endpoint='all_goods')
# goods_api.add_resource(goodSimpleResource, '/good/<int:id>', endpoint='single_good')

		

