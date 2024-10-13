#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,Float,Integer,ForeignKey,event,Text
from extends import db


class Goods(db.Model):
	__tablename__ = 'goods'
	
	id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
	name:Mapped[str]=mapped_column(String(128),nullable=False)
	price:Mapped[float]=mapped_column(Float,nullable=False)
	description:Mapped[str]=mapped_column(Text,nullable=True)
	# backref: 反向引用
	# secondary: 指定中间表
	users = relationship('User', backref='goods',secondary='user_goods_association')
	
	def __str__(self):
		return self.name
	
	
class UserGoodsAssociation(db.Model):
	
	def __init__(self,user_id,goods_id,quantity):
		self.goods_id=goods_id
		self.user_id=user_id
		self.quantity=quantity
	
	__tablename__='user_goods_association'
	
	id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
	user_id:Mapped[int]=mapped_column(Integer,ForeignKey('user.id'))
	goods_id:Mapped[int]=mapped_column(Integer,ForeignKey('goods.id'))
	quantity:Mapped[int]=mapped_column(Integer,default=0)
	# 总价
	total_price:Mapped[float]=mapped_column(Float,nullable=False)
	
# 事件监听器，用于自动计算 total_price
@event.listens_for(UserGoodsAssociation, 'before_insert')
@event.listens_for(UserGoodsAssociation, 'before_update')
def calculate_total_price(mapper, connection, target):
	"""
	计算总价
	:param mapper:表示映射器对象
	:param connection:表示数据库连接
	:param target:表示要监听的模型对象
	:return:
	"""
	# 获取商品实例
	goods=db.session.query(Goods).get(target.goods_id)
	if goods:
		target.total_price=goods.price*target.quantity