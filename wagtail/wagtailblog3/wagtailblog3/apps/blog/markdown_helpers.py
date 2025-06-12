# blog/markdown_helpers.py
from django.apps import apps
from wagtail import hooks
import logging

logger = logging.getLogger(__name__)


class MarkdownHelper:
	"""用于增强wagtail-markdown与MongoDB集成的帮助类"""
	
	@staticmethod
	def process_markdown_for_storage(markdown_content):
		"""处理Markdown内容以便于存储"""
		# 如果内容是字典类型，可能包含额外结构信息
		if isinstance(markdown_content, dict):
			# 确保不丢失任何信息，直接返回
			return markdown_content
		# 如果内容是字符串，直接返回
		return markdown_content
	
	@staticmethod
	def process_markdown_for_editor(markdown_content):
		"""处理MongoDB中的Markdown内容以便在编辑器中显示"""
		# 如果内容是字典类型，可能包含结构信息
		if isinstance(markdown_content, dict):
			# 如果包含raw键，使用raw作为主要内容
			if 'raw' in markdown_content:
				return markdown_content['raw']
			# 尝试其他可能的键
			for key in ['content', 'value', 'text']:
				if key in markdown_content:
					return markdown_content[key]
			# 没有找到合适的键，转换整个对象为字符串
			return str(markdown_content)
		# 如果已经是字符串，直接返回
		return markdown_content
	
	@staticmethod
	def is_markdown_installed():
		"""检查wagtail-markdown是否已安装"""
		try:
			return apps.is_installed('wagtailmarkdown')
		except:
			return False
	
	@staticmethod
	def get_markdown_config():
		"""获取wagtail-markdown配置"""
		from django.conf import settings
		markdown_config = getattr(settings, 'WAGTAILMARKDOWN', {})
		return markdown_config
	
	@staticmethod
	def register_wagtail_markdown_hooks():
		"""注册wagtail-markdown相关的钩子"""
		try:
			@hooks.register('wagtailmarkdown_markdown_extensions')
			def add_markdown_extensions(extensions=None):
				"""添加自定义Markdown扩展"""
				extensions = extensions or []
				# 添加MongoDB兼容的扩展
				return extensions
			
			return True
		except Exception as e:
			logger.error(f"注册wagtail-markdown钩子失败: {e}")
			return False