#!/user/bin/env python3
# -*- coding: utf-8 -*-
from crypt import methods

from flask import Blueprint, render_template, request, jsonify

from apps.user.model import User
from apps.goods.model import Goods, UserGoodsAssociation
from extends import db

# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
# 用户找商品
@goods_bp.route('/find_goods',methods=['GET'],endpoint='find_goods')
def find_goods():
	good=Goods.query.get(request.args.get('id'))
	if not good:
		return render_template('goods/goods_purchased_users.html',error_message='商品不存在')
	return render_template('goods/goods_purchased_users.html',good=good)


# 商品找用户
@goods_bp.route('/find_users',methods=['GET'],endpoint='find_users')
def find_users():
	return 'user'

# 用户购买商品
@goods_bp.route('/buy_goods',methods=['GET','POST'],endpoint='buy_goods')
def buy_goods():
	users = User.query.filter(User.is_deleted == False).all()
	goods = Goods.query.all()
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		goods_id = request.form.get('goods_id')
		quantity = request.form.get('quantity')
		# 验证user_id,goods_id,quantity是否为空
		if not all([user_id,goods_id,quantity]):
			return jsonify({'status': 400, 'message': '都不能为空'}), 400
		# 验证user_id是否存在
		user = User.query.get(user_id)
		good=Goods.query.get(goods_id)
		if not user or not good:
			return jsonify({'status': 400, 'message': '用户和商品不存在'}), 400
		try:
			quantity = int(quantity)
			if quantity <= 0:
				raise ValueError
		except ValueError as e:
			return jsonify({'status': 400, 'message': '专门搞乱的'}), 400
		# 创建用户购买商品记录
		user_goods = UserGoodsAssociation(user_id=user_id, goods_id=goods_id, quantity=quantity)
		# 添加到数据库
		db.session.add(user_goods)
		db.session.commit()
		# 返回json数据
		message='用户{}购买了{}件{}'.format(user.username,quantity,good.name)
		return jsonify({'status': 200, 'message': str(message)}), 200
	# 返回用户购买商品页面
	return render_template('goods/buy_goods.html',users=users,goods=goods)