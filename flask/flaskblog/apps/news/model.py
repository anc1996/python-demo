#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String, Integer, ForeignKey,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.news import BaseModel

class NewsType(BaseModel):
	
    __tablename__ = 'news_type'
    
    type_name:Mapped[str]=mapped_column(String(50), nullable=False,comment='新闻类型名称')
    parent_id:Mapped[int]=mapped_column(Integer,ForeignKey('news_type.id'),nullable=True,comment='父级id')
    # 新闻类型的外键,自反
    news = relationship('News',backref='news_type',uselist=True)
    
    def __repr__(self):
        return f'{self.type_name}'
    
    
class News(BaseModel):
    
    __tablename__ = 'news'
    
    title:Mapped[str]=mapped_column(String(100), nullable=False,comment='新闻标题')
    content:Mapped[str]=mapped_column(Text, nullable=False,comment='新闻内容')
    news_type_id:Mapped[int]=mapped_column(Integer, ForeignKey('news_type.id'),comment='新闻类型id')

    def __repr__(self):
        return f'{self.title}'
    
    @property
    def short_content(self):
        return self.content[:100] if self.content else ''
    
    