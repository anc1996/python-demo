# 创建文件: utils/mongodb.py

import json
from bson import json_util
from django.core.serializers.json import DjangoJSONEncoder
from wagtail.blocks.stream_block import StreamValue


class MongoDBStreamFieldAdapter:
	"""处理StreamField与MongoDB之间的转换"""
	
	@staticmethod
	def to_mongodb(stream_value):
		"""将StreamField的值转换为适合MongoDB存储的格式"""
		if isinstance(stream_value, StreamValue):
			# 将StreamValue转换为可序列化的字典列表
			return json.loads(json.dumps(stream_value.raw_data, cls=DjangoJSONEncoder))
		return stream_value
	
	@staticmethod
	def from_mongodb(data):
		"""从MongoDB格式转换回Python对象"""
		if isinstance(data, list) and all(
				isinstance(item, dict) and 'type' in item and 'value' in item for item in data):
			# 这是StreamField数据的标记
			return data
		return data