#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import DATETIME, String, Integer, ForeignKey, Boolean,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import re
from sqlalchemy.orm import validates

from extends import db
from datetime import datetime


# 评论分类
class ArticleType(db.Model):
    
    def __init__(self, type_name):
        self.type_name = type_name
    
    __tablename__ = 'article_type'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_name: Mapped[str] = mapped_column(String(20), nullable=False)
    # 文章分类的外键,自反
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('article_type.id'), nullable=True)
    articles = relationship('Article', backref='article_type')
    
    def __str__(self):
        return self.type_name




# 建立文章
class Article(db.Model):
    
    def __init__(self, title, content,user_id, type_id=None):
        self.title = title
        self.content = content
        self.user_id=user_id
        self.type_id=type_id
    
    __tablename__ = 'article'  # 表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # 主键
    title: Mapped[str] = mapped_column(String(128),nullable=False )  # 标题,不为空
    content: Mapped[str] = mapped_column(Text,nullable=False )  # 内容,不为空
    publish_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow)  # 发布时间
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否删除
    read_count: Mapped[int] = mapped_column(Integer, default=0)  # 阅读次数
    collect_count: Mapped[int] = mapped_column(Integer, default=0) # 收藏次数
    comment_count: Mapped[int] = mapped_column(Integer, default=0)  # 评论次数
    like_count: Mapped[int] = mapped_column(Integer, default=0) # 点赞次数
    comment_status: Mapped[bool] = mapped_column(Boolean, default=True)  # 评论状态，是否允许评论
    # 图片
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    
    # 用户ID,多对一关系，一个用户可以发表多个文章
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    # backref: 在 Comment 模型中自动创建一个反向引用，使得你可以从 Comment 实例访问相关的 Article 实例。
    comments=relationship('Commnet',backref='article')
    
    # 文章分类
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('article_type.id'), nullable=True)
    
    
    def __str__(self):
        return self.title


class Commnet(db.Model):
    
    def __init__(self, content,user_id,article_id):
        self.content = content
        self.user_id=user_id
        self.article_id=article_id
    
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 评论内容
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('article.id'))
    comment_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def __str__(self):
        return self.content
    
    
    