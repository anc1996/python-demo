#!/user/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Mapped
from flask import abort

from extends import db


class Person(db.Model):
	
	
    __tablename__ = "person"
	# 主键
    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键")
    # 姓名
    name: Mapped[str] = db.Column(db.String(50), nullable=False, comment="姓名")
    # 年龄
    age: Mapped[int] = db.Column(db.Integer, nullable=False, comment="年龄")
    # 性别
    email: Mapped[str] = db.Column(db.String(128), nullable=False, unique=True, comment="邮箱地址")

    @classmethod
    def query_all(cls):
        return cls.query.all()

    @classmethod
    def get_or_404(cls, id):
        person = cls.query.get(id)
        if not person:
	        # 如果找不到该用户，返回404错误
            abort(404)
        return person

    @classmethod
    def create(cls, data):
        new_person = cls(**data)
        db.session.add(new_person)
        db.session.commit()
        return new_person

    @classmethod
    def update(cls, id, data):
        person = cls.get_or_404(id)
        for key, value in data.items():
            setattr(person, key, value)
        db.session.commit()
        return person

    @classmethod
    def delete(cls, id):
        person = cls.get_or_404(id)
        db.session.delete(person)
        db.session.commit()