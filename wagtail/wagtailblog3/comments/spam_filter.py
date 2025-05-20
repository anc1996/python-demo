# comments/spam_filter.py
import re
from django.conf import settings


class SpamFilter:
	"""简单的垃圾评论过滤器"""
	
	@staticmethod
	def is_spam(content, user=None, ip_address=None):
		"""检查评论是否为垃圾评论"""
		# 获取配置中的垃圾关键词
		spam_keywords = getattr(settings, 'COMMENT_SPAM_KEYWORDS', [])
		
		# 转换为小写进行检查
		content_lower = content.lower()
		
		# 检查关键词
		for keyword in spam_keywords:
			if keyword.lower() in content_lower:
				return True
		
		# 检查URL数量
		url_pattern = r'https?://[^\s]+'
		urls = re.findall(url_pattern, content)
		if len(urls) > 3:  # 如果包含超过3个URL，可能是垃圾评论
			return True
		
		# 检查内容长度与重复模式
		if len(content) > 1000 and len(set(content)) / len(content) < 0.2:
			# 内容很长但字符多样性低，可能是垃圾
			return True
		
		return False