#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import DATETIME, String, Integer, SmallInteger, ForeignKey,Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship
import re
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from extends import db
from datetime import datetime

class User(db.Model):
	# 定义表名。如果未设置，SQLAlchemy 会自动将其类名作为表名
	__tablename__ = 'user'
	'''
		用户表
		id 主键,自增
		username 唯一
		email:
	'''
	__tablename__ = 'user'
	# Mapped：表示这是一个映射到数据库列的 Python 类型，并且能利用 Python 的类型注解功能（Type Hints）。这是为了在模型类中清晰地声明字段的类型。
	# Mapped[X] 表示这个类属性是数据库表中的一列，且类型为 X。通过这种方式，Python 的静态类型检查工具可以识别字段类型，开发者也可以在代码中更明确地知道每个字段的类型。
	# mapped_column：这是一个用来定义 SQLAlchemy 模型列的函数，类似于旧版本中的 db.Column，但它结合了新的 Mapped 类型提示，更加灵活。
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	username: Mapped[str] = mapped_column(String(128), unique=True)
	email: Mapped[str] = mapped_column(String(128), unique=True)
	_password: Mapped[str] = mapped_column("password", String(255), nullable=False)
	phone: Mapped[str] = mapped_column(String(11), unique=True)
	register_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow)
	# is_deleted：表示是否删除，这是一个布尔类型的字段，用于标记记录是否被删除。
	is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
	
	# 添加到 UserInfo,反向引用，定义 User 和 UserInfo 的一对一关系
	# back_populates：定义反向引用，表示 UserInfo 类中的 user 属性与 User 类相关联。
	userinfo: Mapped["UserInfo"] = relationship("UserInfo", back_populates="user", uselist=False)
	
	# 正则表达式
	EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
	PHONE_REGEX = r'^1[3-9]\d{9}$'
	
	@property
	def password(self):
		raise AttributeError("Password is not a readable attribute")  # 禁止直接读取密码
	
	@password.setter
	def password(self, password):
		"""设置密码时自动进行哈希"""
		self._password = generate_password_hash(password)
	
	def check_password(self, password):
		"""检查密码是否正确"""
		return check_password_hash(self._password, password)
	
	@validates('email')
	def validate_email(self, key, email):
		"""验证 email 格式"""
		if not re.match(self.EMAIL_REGEX, email):
			raise ValueError("Invalid email format")
		return email
	
	@validates('phone')
	def validate_phone(self, key, phone):
		"""验证中国大陆手机号码格式"""
		if not re.match(self.PHONE_REGEX, phone):
			raise ValueError("Invalid phone number format for China")
		return phone
	
	def __str__(self):
		"""返回对象的可读字符串表示"""
		return f"<User {self.username}>"
	
	
class UserInfo(db.Model):
	
	__tablename__='userinfo'
	
	# 定义表字段
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	# 定义外键，关联到 User 表的 id
	# 一个外键列，在数据库的 UserInfo 表中创建一个名为 user_id 的列。
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True, nullable=False)
	# 反向引用，定义 User 和 UserInfo 的一对一关系
	# 这是ORM 关系属性，在 Python 层面上表示 UserInfo 类中的 user 属性与 User 类相关联。
	user: Mapped["User"] = relationship('User', back_populates='userinfo', uselist=False)
	realname:Mapped[str] = mapped_column(String(64),nullable=False)
	age:Mapped[int] = mapped_column(Integer)
	Sex:Mapped[int] = mapped_column(SmallInteger)
	
	