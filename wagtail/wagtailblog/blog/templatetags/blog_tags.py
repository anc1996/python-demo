from django import template
import re
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value):
	"""将 Markdown 转换为 HTML"""
	# 使用更多Markdown扩展
	extensions = [
		'markdown.extensions.fenced_code',
		'markdown.extensions.tables',
		'markdown.extensions.toc',
		'markdown.extensions.codehilite',
		'markdown.extensions.extra',
		'markdown.extensions.nl2br',
		'markdown.extensions.smarty',
	]
	
	extension_configs = {
		'markdown.extensions.codehilite': {
			'linenums': False,
			'css_class': 'highlight',
		}
	}
	
	# 转换 Markdown 为 HTML
	html = markdown.markdown(value, extensions=extensions, extension_configs=extension_configs)
	
	# 处理LaTeX数学公式
	if '$$' in html:
		html = f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">\n{html}'
		html += '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>'
		html += '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>'
	
	return html


@register.filter(name='youtube_embed_url')
def youtube_embed_url(url):
	"""将 YouTube URL 转换为嵌入 URL"""
	# 匹配 YouTube 链接格式
	regex = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)'
	match = re.search(regex, url)
	if match:
		return f'https://www.youtube.com/embed/{match.group(1)}'
	return url


@register.filter(name='bilibili_embed_url')
def bilibili_embed_url(url):
	"""将 Bilibili URL 转换为嵌入 URL"""
	# 匹配 Bilibili 链接格式
	regex = r'(?:https?:\/\/)?(?:www\.)?bilibili\.com\/video\/([^\/]+)'
	match = re.search(regex, url)
	if match:
		return f'//player.bilibili.com/player.html?bvid={match.group(1)}'
	return url


@register.filter(name='vimeo_embed_url')
def vimeo_embed_url(url):
	"""将 Vimeo URL 转换为嵌入 URL"""
	# 匹配 Vimeo 链接格式
	regex = r'(?:https?:\/\/)?(?:www\.)?vimeo\.com\/(\d+)'
	match = re.search(regex, url)
	if match:
		return f'https://player.vimeo.com/video/{match.group(1)}'
	return url