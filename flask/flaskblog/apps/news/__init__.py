#!/user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from extends import db

class BaseModel(db.Model):
	# 定义基类模型
	__abstract__ = True
	 
	id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True,comment='主键')
	is_deleted:Mapped[bool]=mapped_column(Boolean, default=False,comment='是否删除')
	update_time:Mapped[datetime]=mapped_column(DateTime, default=datetime.now, onupdate=datetime.now,comment='更新时间')
 
	def __str__(self):
		return self.name