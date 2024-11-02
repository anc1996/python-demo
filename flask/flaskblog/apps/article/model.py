#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import DATETIME, String, Integer, ForeignKey, Boolean,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
import re
from sqlalchemy.orm import validates

from extends import db
from datetime import datetime


# 文章分类
class ArticleType(db.Model):
    
    def __init__(self, type_name):
        self.type_name = type_name
    
    __tablename__ = 'article_type'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment="主键")
    type_name: Mapped[str] = mapped_column(String(20), nullable=False,comment="分类名称")
    # 文章分类的外键,自反
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('article_type.id'), nullable=True,comment="父分类")
    
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
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='主键')
    title: Mapped[str] = mapped_column(String(128),nullable=False,comment='标题')
    description: Mapped[str] = mapped_column(String(128), nullable=True,comment="文章描述")
    content: Mapped[str] = mapped_column(Text,nullable=False,comment='文章内容')
    publish_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow, comment='发布时间')
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否删除')
    read_count: Mapped[int] = mapped_column(Integer, default=0,comment="阅读次数")
    collect_count: Mapped[int] = mapped_column(Integer, default=0,comment="收藏次数")
    comment_count: Mapped[int] = mapped_column(Integer, default=0,comment="评论次数")
    like_count: Mapped[int] = mapped_column(Integer, default=0, comment="点赞次数")
    comment_status: Mapped[bool] = mapped_column(Boolean, default=True, comment="评论状态")  # 评论状态，是否允许评论
    background_image: Mapped[str] = mapped_column(String(128), nullable=True, comment="背景图片路径")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False,comment="用户ID")
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('article_type.id'), nullable=True,comment="分类ID")
    
    # backref: 在 Comment 模型中自动创建一个反向引用，使得你可以从 Comment 实例访问相关的 Article 实例。
    comments=relationship('Comment',backref='article')
    files=relationship('ArticleFile',backref='article')
    # 定义自引用关系
    replies = relationship("Comment", backref=backref('comment_parent', remote_side=[id]), lazy='dynamic')
    
    
    def __str__(self):
        return self.title



class ArticleFile(db.Model):
    """
    表示与文章关联的文件，例如图像、视频、链接或表格。
    """
    __tablename__ = 'article_file'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
    file_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="文件名")
    file_path: Mapped[str] = mapped_column(String(128), nullable=False, comment="文件路径")
    file_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="文件类型")
    file_size: Mapped[int] = mapped_column(Integer, nullable=True, comment="文件大小")
    upload_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow, comment="上传时间")
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('article.id'), nullable=False, comment="文章ID")
    content_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="附件类型")

    @validates('file_name')
    def validate_file_name(self, key, file_name):
        if not file_name.strip():
            raise ValueError("文件名不能为空或空格")
        return file_name

    @validates('file_path')
    def validate_file_path(self, key, file_path):
        if not file_path.strip():
            raise ValueError("文件路径不能为空或空格")
        return file_path

    @validates('content_type')
    def validate_content_type(self, key, content_type):
        valid_types = ["image", "video", "link", "table"]
        if content_type not in valid_types:
            raise ValueError(f"内容类型无效。必须是以下之一 {valid_types}")
        return content_type

    def __str__(self):
        return f"<ArticleFile {self.file_name}>"

# 评论
class Comment(db.Model):
    
    def __init__(self, content,user_id,article_id,parent_id=None):
        self.content = content
        self.user_id=user_id
        self.article_id=article_id
        self.parent_id=parent_id
    
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='主键')
    content: Mapped[str] = mapped_column(Text, nullable=False, comment='评论内容')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('article.id'), nullable=False, comment='文章ID')
    comment_time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow, comment='评论时间')
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否删除')
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('comment.id'), nullable=True, comment='父评论ID')
    
    # 定义自引用关系
    replies = relationship("Comment", backref=backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __str__(self):
        return self.content
    
    
    
    