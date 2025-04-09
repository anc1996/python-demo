#!/user/bin/env python3
# -*- coding: utf-8 -*-
from wagtail.fields import RichTextField
from .mongodb_utils import page_content_collection
import uuid

class MongoDBRichTextField(RichTextField):
	"""自定义字段，将富文本内容存储在MongoDB中"""
	
	
	def __init__(self, *args, **kwargs):
		self.mongo_id_field_name = kwargs.pop('mongo_id_field_name', None)
		super().__init__(*args, **kwargs)
	
	def get_prep_value(self, value):
		"""准备存储到数据库的值"""
		return value
	
	def pre_save(self, model_instance, add):
		"""保存前处理，将内容存入MongoDB"""
		value = getattr(model_instance, self.attname)
		
		# 获取MongoDB的ID
		mongo_id = getattr(model_instance, self.mongo_id_field_name)
		if not mongo_id:
			mongo_id = str(uuid.uuid4())
			setattr(model_instance, self.mongo_id_field_name, mongo_id)
		
		# 存储内容到MongoDB
		page_content_collection.update_one(
			{'_id': mongo_id},
			{'$set': {'content': value}},
			upsert=True
		)
		
		# 返回一个占位符，实际内容在MongoDB中
		return f"MONGO_CONTENT_ID:{mongo_id}"
	
	def from_db_value(self, value, expression, connection):
		"""从数据库获取值时的处理"""
		if value and isinstance(value, str) and value.startswith("MONGO_CONTENT_ID:"):
			mongo_id = value.replace("MONGO_CONTENT_ID:", "")
			try:
				mongo_doc = page_content_collection.find_one({'_id': mongo_id})
				if mongo_doc:
					return mongo_doc.get('content', '')
			except Exception as e:
				print(f"从MongoDB获取内容失败: {e}")
		return value