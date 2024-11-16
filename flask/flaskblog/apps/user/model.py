#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import DATETIME, String, Integer, SmallInteger, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
import re
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from extends import db
from datetime import datetime

from extends.minio_bucket import flask_bucket


class User(db.Model):
	
	def __init__(self, username: str, password: str, email: str, phone: str, icon: str = None):
		self.username = username
		self.password = password  # 这里会自动调用 password 的 setter 方法进行哈希
		self.email = email
		self.phone = phone
		self.icon = icon
	
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
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
	username: Mapped[str] = mapped_column(String(128), unique=True,comment="用户名")
	email: Mapped[str] = mapped_column(String(128),comment="邮箱", unique=True)
	_password: Mapped[str] = mapped_column("password", String(255), nullable=False, comment="密码")
	phone: Mapped[str] = mapped_column(String(11), unique=True, comment="手机号")
	register_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.now,comment="注册时间")
	# 头像：表示用户头像，这是一个字符串类型的字段，用于存储头像的路
	icon: Mapped[str] = mapped_column(String(255), nullable=True, comment="头像")
	# is_deleted：表示是否删除，这是一个布尔类型的字段，用于标记记录是否被删除。
	is_deleted: Mapped[bool] = mapped_column(Boolean, default=False,comment="是否删除")
	
	
	userinfo: Mapped["UserInfo"] = relationship("UserInfo", back_populates="user", uselist=False)
	# 添加article,反向引用，定义 User 和 Article 的一对多关系
	# 双向关系: 这意味着当你在 User 实例中访问 article 时，SQLAlchemy 会自动填充 Article 实例中的 user 属性，反之亦然。
	# article: Mapped["Article"] = relationship("Article", back_populates="user")
	# 这个参数用于在 Article 模型中自动创建一个反向引用。它会在 Article 模型中添加一个名为 user 的属性，该属性指向 User 模型。
	# 意味着当你在 User 实例中访问 articles 时，SQLAlchemy 会自动填充 Article 实例中的 user 属性。
	articles: Mapped["Article"] = relationship("Article", backref="user")
	comments: Mapped["Comment"] = relationship("Comment", backref="user")
	
	
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
	
	@property
	def url(self):
		# 返回头像的 URL
		if not self.icon:
			return None
		return flask_bucket.get_Url(bucket_file=self.icon)
	
	def __str__(self):
		"""返回对象的可读字符串表示"""
		return f"<User {self.username}>"


class UserInfo(db.Model):
	__tablename__ = 'userinfo'
	
	def __init__(self, user_id, realname, age,sex):
		self.user_id = user_id
		self.realname = realname
		self.age = age
		self.sex=sex
	
	# 定义表字段
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
	# 定义外键，关联到 User 表的 id
	# 一个外键列，在数据库的 UserInfo 表中创建一个名为 user_id 的列。
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True, nullable=False,comment="用户ID")
	realname: Mapped[str] = mapped_column(String(64), nullable=False, comment="真实姓名")
	age: Mapped[int] = mapped_column(Integer, comment="年龄")
	sex: Mapped[int] = mapped_column(SmallInteger,comment="性别")
	content: Mapped[str] = mapped_column(String(255), nullable=False, comment="关于我内容")
	publish_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.now, comment="发布时间")
	
	# 反向引用，定义 User 和 UserInfo 的一对一关系
	# 这是ORM 关系属性，在 Python 层面上表示 UserInfo 类中的 user 属性与 User 类相关联。
	user: Mapped["User"] = relationship('User', back_populates='userinfo', uselist=False)
	
	@validates('age')
	def validate_age(self, key, age):
		# 验证年龄是否在合理范围内
		if age < 0 or age > 150:
			raise ValueError("Invalid age")
		return age
	
	SEX_MAP = ("男", "女", "保密")
	
	@property
	def sex_str(self):
		return self.SEX_MAP[self.sex] if 0 <= self.sex <= 2 else "未知"
	
	def __str__(self):
		return f"<UserInfo {self.realname}>"


class UserAlbum(db.Model):
	"""
        表示包含图像的用户相册。
    """
	
	__tablename__ = 'user_album'

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
	name: Mapped[str] = mapped_column(String(128), nullable=False,comment="相册名称")
	path: Mapped[str] = mapped_column(String(255), nullable=False,comment="相册路径")
	description: Mapped[str] = mapped_column(String(255),nullable=True,comment="相册描述") # 描述
	album_datetime: Mapped[datetime] = mapped_column(DATETIME, default=datetime.now,comment="创建时间")
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False,comment="用户ID")
	
	# 在附加表中声明相关属性
	user = relationship("User",uselist=False,
	                    backref=backref('albums', lazy='dynamic',uselist=True))
	
	
	@validates('name')
	def validate_name(self, key, name):
	    if not name.strip():
	        raise ValueError("相册名称不能为空或空格")
	    return name
	
	@validates('path')
	def validate_path(self, key, path):
	    if not path.strip():
	        raise ValueError("相册路径不能为空或空格")
	    return path
	
	@property
	def url(self):
		# 返回相册的 URL
		if not self.path:
			return None
		return flask_bucket.get_Url(bucket_file=self.path)
	
	def __str__(self):
	    return f"<UserAlbum {self.name}>"


