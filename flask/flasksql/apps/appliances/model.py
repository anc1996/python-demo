#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Float, Integer

from apps import db

class Appliance(db.Model):
	
	__tablename__ = 'tb_appliance'

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='家电ID')
	name: Mapped[str] = mapped_column(String(50), nullable=False, comment='家电名称')
	model: Mapped[str] = mapped_column(String(50), nullable=False, comment='家电型号')
	description: Mapped[str] = mapped_column(String(255), nullable=True, comment='家电描述')
	price: Mapped[float] = mapped_column(Float, nullable=True, comment='家电价格')
	country: Mapped[str] = mapped_column(String(50), nullable=True, comment='产地')
	stock: Mapped[int] = mapped_column(Integer, nullable=True, comment='库存')
	
	# 定义关系
	parts=relationship('Part',back_populates='appliance',lazy='select')
	
	def __repr__(self):
		return f'<Appliance id={self.id} name={self.name} model={self.model} description={self.description}>'

class Part(db.Model):
	
	__tablename__='tb_part'
	
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='配件ID')
	name: Mapped[str] = mapped_column(String(50), nullable=False, comment='配件名称')
	description: Mapped[str] = mapped_column(String(255), nullable=True, comment='配件描述')
	appliance_id: Mapped[int] = mapped_column(ForeignKey('tb_appliance.id'), nullable=True, comment='家电ID')
	
	# 定义关系
	appliance=relationship('Appliance',back_populates='parts',lazy='select')
	
	def __repr__(self):
		return f'<Part id={self.id} name={self.name} description={self.description}>'
	