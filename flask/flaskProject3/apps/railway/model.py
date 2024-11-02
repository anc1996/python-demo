#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Mapped, backref

from extends import db



class Passenger(db.Model):
	
	__tablename__ = "db_passenger"
	
	id:Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键")
	name:Mapped[str] = db.Column(db.String(15), comment="姓名")
	age:Mapped[int] = db.Column(db.Integer, comment="年龄")
	sex:Mapped[str] = db.Column(db.String(1), comment="性别")
	email:Mapped[str] = db.Column(db.String(128), comment="邮箱地址")
	
	# secondary 参数用于定义多对多关系中的中间表（关联表）。
	# 多对多关系通常涉及两个模型类，它们之间通过一个中间表来关联。secondary 参数允许你指定这个中间表的名称或模型类。
	tickets = db.relationship("Train", secondary="db_passenger_ticket",
	                         backref=backref("passengers", lazy="dynamic"), lazy="dynamic")
	
	
class Train(db.Model):
	
	__tablename__ = "db_train"
	
	id:Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键")
	train_name:Mapped[str] = db.Column(db.String(15), comment="列车名称")
	train_type:Mapped[str] = db.Column(db.String(15), comment="列车类型")
	

class passenger_ticket(db.Model):
	
	__tablename__ = "db_passenger_ticket"
	
	id:Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键")
	passenger_id:Mapped[int] = db.Column(db.Integer, db.ForeignKey("db_passenger.id"), comment="乘客id")
	train_id:Mapped[int] = db.Column(db.Integer, db.ForeignKey("db_train.id"), comment="列车id")


