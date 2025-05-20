import os,uuid,logging

from datetime import datetime

from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from blog.models import BlogCategory, BlogPage

# 这个文档是用来处理Wagtail的钩子函数的

logger = logging.getLogger(__name__)


@hooks.register('before_create_document')
def set_unique_document_filename(document, request):
	"""
	在文档创建前为文件设置唯一文件名
	"""
	if document.file:
		# 获取原始文件名和扩展名
		original_path = document.file.name
		dir_name, file_name = os.path.split(original_path)
		file_root, file_ext = os.path.splitext(file_name)
		
		# 生成新的唯一文件名（保留原文件名+时间戳+随机字符串）
		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		random_str = uuid.uuid4().hex[:6]
		new_filename = f"{file_root}_{timestamp}_{random_str}{file_ext}"
		
		# 构建新的文件路径
		new_path = os.path.join(dir_name, new_filename)
		
		# 更新文件路径
		document.file.name = new_path
		
		logger.info(f"设置唯一文档文件名: {original_path} -> {new_path}")



# 富文本编辑器自定义功能
@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
	"""为富文本编辑器添加代码块功能"""
	feature_name = 'code-block'
	
	# 设置Draftail配置
	features.register_editor_plugin(
		'draftail', feature_name,
		draftail_features.BlockFeature({
			'type': 'code-block',
			'icon': 'code',
			'description': '代码块',
		})
	)
	
	# 设置转换器
	features.register_converter_rule('contentstate', feature_name, {
		'from_database_format': {'pre[class=code-block]': BlockElementHandler('code-block')},
		'to_database_format': {'block_map': {'code-block': {'element': 'pre', 'props': {'class': 'code-block'}}}}
	})
	
	# 在默认功能集中添加此功能
	features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_math_formula_feature(features):
	"""为富文本编辑器添加数学公式功能"""
	feature_name = 'math-formula'
	
	# 设置Draftail配置
	features.register_editor_plugin(
		'draftail', feature_name,
		draftail_features.BlockFeature({
			'type': 'math-formula',
			'icon': 'superscript',
			'description': '数学公式',
		})
	)
	
	# 设置转换器
	features.register_converter_rule('contentstate', feature_name, {
		'from_database_format': {'div[class=math-formula]': BlockElementHandler('math-formula')},
		'to_database_format': {'block_map': {'math-formula': {'element': 'div', 'props': {'class': 'math-formula'}}}}
	})
	
	# 在默认功能集中添加此功能
	features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_markdown_feature(features):
	"""为富文本编辑器添加Markdown功能"""
	feature_name = 'markdown'
	
	# 设置Draftail配置
	features.register_editor_plugin(
		'draftail', feature_name,
		draftail_features.BlockFeature({
			'type': 'markdown',
			'icon': 'pilcrow',
			'description': 'Markdown',
		})
	)
	
	# 设置转换器
	features.register_converter_rule('contentstate', feature_name, {
		'from_database_format': {'div[class=markdown-block]': BlockElementHandler('markdown')},
		'to_database_format': {'block_map': {'markdown': {'element': 'div', 'props': {'class': 'markdown-block'}}}}
	})
	
	# 在默认功能集中添加此功能
	features.default_features.append(feature_name)


# 添加自定义CSS和JS到管理后台
@hooks.register('insert_global_admin_css')
def global_admin_css():
	"""添加自定义CSS到管理后台"""
	return format_html(
		'<link rel="stylesheet" href="{}">',
		static('css/admin.css')
	)


@hooks.register('insert_global_admin_js')
def global_admin_js():
	"""添加自定义JS到管理后台"""
	return format_html(
		'<script src="{}"></script>',
		static('js/admin.js')
	)


# 博客分类管理
class BlogCategoryViewSet(SnippetViewSet):
	model = BlogCategory
	icon = 'tag'
	list_display = ('name', 'slug')
	search_fields = ('name',)


register_snippet(BlogCategoryViewSet)


# 在后台主页添加博客统计信息
@hooks.register('construct_homepage_panels')
def add_blog_stats_panel(request, panels):
	"""添加博客统计信息到管理后台首页"""
	from wagtail.admin.ui.components import Component
	from blog.models import BlogPage
	
	class BlogStatsPanel(Component):
		name = 'blog_stats'
		template_name = 'admin/blog_stats_panel.html'
		order = 500  # 添加这一行，设置显示顺序
		
		def get_context_data(self, parent_context):
			context = super().get_context_data(parent_context)
			context['total_posts'] = BlogPage.objects.live().count()
			context['draft_posts'] = BlogPage.objects.filter(live=False).count()
			# 近30天发布的文章
			from django.utils import timezone
			from datetime import timedelta
			thirty_days_ago = timezone.now() - timedelta(days=30)
			context['recent_posts'] = BlogPage.objects.live().filter(
				first_published_at__gte=thirty_days_ago
			).count()
			
			return context
	
	panels.append(BlogStatsPanel())


# 将编辑器内容同步到MongoDB
@hooks.register('after_edit_page')
def sync_to_mongodb_after_edit(request, page):
	"""编辑页面后将内容同步到MongoDB"""
	if isinstance(page, BlogPage):
		from blog.utils import sync_to_mongodb
		sync_to_mongodb(page)


@hooks.register('after_publish_page')
def sync_to_mongodb_after_publish(request, page):
	"""发布页面后将内容同步到MongoDB"""
	if isinstance(page, BlogPage):
		from blog.utils import sync_to_mongodb, cache_blog_content
		sync_to_mongodb(page)
		cache_blog_content(page)


