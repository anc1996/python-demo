#!/user/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String,Float,Integer,ForeignKey,event,Text,Boolean,DateTime
from extends import db
from extends.minio_bucket import flask_bucket


class Goods(db.Model):
	__tablename__ = 'goods'
	
	id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,comment='商品id') # 商品id
	name:Mapped[str]=mapped_column(String(128),nullable=False,comment='商品名称') # 商品名称
	price:Mapped[float]=mapped_column(Float,nullable=False,comment='商品价格') # 商品价格
	description:Mapped[str]=mapped_column(Text,nullable=True,comment='商品描述') # 商品描述
	image:Mapped[str]=mapped_column(String(128),nullable=True,comment='商品图片') # 商品图片
	is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否删除')  # 是否删除
	update_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,onupdate=datetime.now, comment='更新时间')  # 更新时间
	
	# backref: 反向引用
	# secondary: 指定中间表
	users:Mapped["User"]=relationship("User",secondary='user_goods_association',
	                                  backref='goods',uselist=True)
	
	def __str__(self):
		return self.name
	
	@property
	def ImageUrl(self):
		if not self.image:
			return None
		return flask_bucket.get_Url(bucket_file=self.image)


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
	total_price:Mapped[float]=mapped_column(Float,nullable=False) # 总价
	# backref: 反向引用
	user:Mapped["User"]=relationship("User",backref=backref('association',uselist=False))
	
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