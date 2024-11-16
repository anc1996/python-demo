#!/user/bin/env python3
# -*- coding: utf-8 -*-
from hmac import compare_digest

from sqlalchemy import String,Text
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from extends import db


class automatic(db.Model):
	
	# 定义表名
	__tablename__ = 'automatic'
	
	id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,comment="主键")
	username:Mapped[str]=mapped_column(String(128),unique=True,comment="用户名")
	full_name = mapped_column(Text, nullable=False)
	password:Mapped[str]=mapped_column(String(255),nullable=False,comment="密码")
	
	@property
	def password(self):
		raise AttributeError("Password is not a readable attribute")  # 禁止直接读取密码
	
	@password.setter
	def password(self, password):
		"""设置密码时自动进行哈希"""
		"""安全地对密码进行哈希处理以进行存储。可以将密码与存储的哈希值进行比较
            使用 ：func：'check_password_hash"""
		self._password = generate_password_hash(password)
	
	def check_password(self, password):
		"""检查密码是否正确"""
			
		"""
		安全地检查之前使用
			：func：'generate_password_hash' 匹配给定的密码。
			如果方法不再被视为安全，则可能会弃用和删除这些方法。
			自迁移旧哈希值，您可能会在检查旧哈希值时生成新哈希值，或者您可能会通过链接联系用户以重置其密码。
			:p aram pwhash：哈希密码。
			:p aram password：明文密码。
		"""
		
		return check_password_hash(self._password, password)