"""
序列化 Wagtail StreamField 内容的自定义序列化器
"""

from rest_framework import serializers
from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtailmarkdown.utils import render_markdown


class StreamFieldSerializer(serializers.BaseSerializer):
	"""
	StreamField 内容序列化基类
	"""
	
	def to_representation(self, instance):
		result = []
		for block in instance:
			block_type = block.block_type
			value = block.value
			block_data = self.serialize_block(block_type, value, block)
			result.append({
				'type': block_type,
				'value': block_data
			})
		return result
	
	def serialize_block(self, block_type, value, block):
		"""
		根据块类型序列化内容
		"""
		if block_type == 'rich_text':
			return self.serialize_rich_text(value)
		elif block_type == 'markdown':
			return self.serialize_markdown(value)
		elif block_type == 'table':
			return self.serialize_table(value)
		elif block_type in ['media', 'audio', 'video']:
			return self.serialize_media(value, block_type)
		elif block_type == 'embed':
			return self.serialize_embed(value)
		elif block_type == 'raw_html':
			return self.serialize_raw_html(value)
		else:
			return str(value)  # 默认转换为字符串
	
	def serialize_rich_text(self, value):
		"""
		序列化富文本内容
		"""
		return str(value)  # RichText 已经渲染为 HTML
	
	def serialize_markdown(self, value):
		"""
		序列化 Markdown 内容
		"""
		# 返回原始 Markdown 和渲染后的 HTML
		return {
			'raw': value,
			'html': render_markdown(value)
		}
	
	def serialize_table(self, value):
		"""
		序列化表格内容
		"""
		if hasattr(value, 'data'):
			# 直接返回表格数据
			return {
				'data': value.data,
				'first_row_is_table_header': value.first_row_is_table_header,
				'first_col_is_header': value.first_col_is_header,
			}
		return value
	
	def serialize_media(self, value, block_type):
		"""
		序列化媒体内容
		"""
		if not value:
			return None
		
		result = {
			'id': value.id,
			'title': value.title,
			'type': value.type if hasattr(value, 'type') else block_type,
		}
		
		# 添加文件 URL
		if hasattr(value, 'file') and value.file:
			result['file_url'] = value.file.url
		
		# 添加媒体源信息
		if hasattr(value, 'sources'):
			result['sources'] = value.sources
		
		return result
	
	def serialize_embed(self, value):
		"""
		序列化嵌入内容
		"""
		if hasattr(value, 'url') and value.url:
			return {
				'url': value.url,
				'html': value.html,
				'title': value.title if hasattr(value, 'title') else None,
			}
		return str(value)
	
	def serialize_raw_html(self, value):
		"""
		序列化原始 HTML
		"""
		return value  # 直接返回原始 HTML