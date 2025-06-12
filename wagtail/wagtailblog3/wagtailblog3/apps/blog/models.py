# blog/models.py

import traceback,logging

from django.utils import timezone  
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django import forms
from django.conf import settings
from django.db.models import Count,Sum

from django.utils.html import strip_tags  # 用于去除HTML标签
from django.utils.safestring import mark_safe  # 用于标记HTML安全

from datetime import datetime,date
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase,Tag

from wagtail.embeds.blocks import EmbedBlock
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.blocks import RichTextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.blocks.stream_block import StreamValue

from wagtailmarkdown.blocks import MarkdownBlock

from blog.blocks import AudioBlock, VideoBlock, CustomTableBlock
from wagtailblog3.mongo import MongoManager
from wagtailblog3.mongodb import MongoDBStreamFieldAdapter
from blog.markdown_helpers import MarkdownHelper

logger = logging.getLogger(__name__)


# 自定义图片模型
class BlogImage(AbstractImage):
	
	"""自定义博客图片模型"""
	caption = models.CharField(max_length=255, blank=True)
	admin_form_fields = Image.admin_form_fields + ('caption',) # 添加caption字段到后台表单
	
	@property
	def default_alt_text(self):
		# 如果没有指定alt文本，使用caption作为替代
		return self.caption or self.title


class BlogRendition(AbstractRendition):
	"""博客图片渲染模型"""
	image = models.ForeignKey(
		'BlogImage',
		on_delete=models.CASCADE,
		related_name='renditions'
	)
	
	class Meta:
		# 确保每个图片的渲染是唯一的
		unique_together = (
			('image', 'filter_spec', 'focal_point_key'),
		)



# 博客标签模型
class BlogTagIndexPage(Page):
    """
    页面用于展示按标签筛选的文章列表，或所有标签的列表。
    支持对文章标题（在特定标签下）或标签名称进行搜索和分页。
    """
    subpage_types = []  # 通常标签索引页不应有子页面
    parent_page_types = ['wagtailcore.Page', 'home.HomePage', 'blog.BlogIndexPage'] # 根据你的实际情况调整
    subpage_types = ['blog.BlogIndexPage']  # 根据你的实际情况调整

    # 通用分页设置 (可以根据需要为文章和标签设置不同的值)
    items_per_page = 50

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        tag_slug_filter = request.GET.get('tag')    # ?tag=<slug>
        search_query = request.GET.get('q', '').strip()  # ?q=<query>
        page_number = request.GET.get('page')       # ?page=<number>
        
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        context['search_query'] = search_query
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['current_tag'] = None
        context['paged_items'] = None # 将用于文章分页或标签分页
        context['mode'] = None # "tag_detail" 或 "tag_list"

        if tag_slug_filter:
            # --- 模式 A: 标签详情模式 (查看特定标签下的文章) ---
            context['mode'] = "tag_detail"
            try:
                tag_object = Tag.objects.get(slug=tag_slug_filter)
                context['current_tag'] = tag_object

                # 获取该标签下的所有已发布、公开的文章
                articles_queryset = BlogPage.objects.live().public().filter(tags=tag_object)

                # 如果有文章标题搜索词 (q)，则进一步过滤
                if search_query:
                    articles_queryset = articles_queryset.filter(title__icontains=search_query)
                    
                if start_date:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                    articles_queryset = articles_queryset.filter(date__gte=start_date_obj)
                
                if end_date:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                    articles_queryset = articles_queryset.filter(date__lte=end_date_obj)
				
                articles_queryset = articles_queryset.order_by('-date') # 或其他排序

                # 对文章列表进行分页
                paginator = Paginator(articles_queryset, self.items_per_page)
                try:
                    context['paged_items'] = paginator.page(page_number)
                except PageNotAnInteger:
                    context['paged_items'] = paginator.page(1)
                except EmptyPage:
                    context['paged_items'] = paginator.page(paginator.num_pages)

            except Tag.DoesNotExist:
                context['paged_items'] = []  # 或者设置为空列表以避免错误
        else:
            # --- 模式 B: 标签列表模式 ---
            context['mode'] = "tag_list"

            # 1. 获取所有使用过的标签的基础查询集
            #    确保只获取那些至少被一篇 BlogPage 使用的标签 (live & public)
            active_blog_pages_tags_ids = BlogPage.objects.live().public().values_list('tags', flat=True).distinct()
            used_tags_queryset = Tag.objects.filter(pk__in=active_blog_pages_tags_ids)

            # 2. 应用标签名称搜索查询 (如果存在)
            if search_query:
                used_tags_queryset = used_tags_queryset.filter(name__icontains=search_query)

            used_tags_queryset = used_tags_queryset.order_by('name')

            # 3. 为每个标签附加文章数量
            tags_with_counts = []
            for tag_item in used_tags_queryset:
                # 确保计数也只计算 live 和 public 的文章
                count = BlogPage.objects.live().public().filter(tags=tag_item).count()
                if count > 0:  # 只显示实际有文章的标签
                    tags_with_counts.append({'tag': tag_item, 'count': count})

            # 4. 对带有计数的标签列表进行分页
            paginator = Paginator(tags_with_counts, self.items_per_page)
            try:
                context['paged_items'] = paginator.page(page_number)
            except PageNotAnInteger:
                context['paged_items'] = paginator.page(1)
            except EmptyPage:
                context['paged_items'] = paginator.page(paginator.num_pages)

        return context


# 标签模型
class BlogPageTag(TaggedItemBase):
	"""博客页面标签"""
	
	# TaggedItemBase 是一个抽象模型，用于定义标签与模型的关联关系。
	
	content_object = ParentalKey(
		'BlogPage',
		related_name='tagged_items',
		on_delete=models.CASCADE
	) # 关联到BlogPage模型


# 博客分类
@register_snippet
class BlogCategory(models.Model):
    """博客分类模型"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = "博客分类"


# 博客索引页面
class BlogIndexPage(Page):
	"""博客索引页面"""
	
	date = models.DateField("发布日期", default=timezone.now)  # 添加日期字段
	intro = RichTextField("页面介绍", blank=True)
	
	featured_image = models.ForeignKey(
		'BlogImage',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)  # 特色图片
	
	
	content_panels = Page.content_panels + [
		FieldPanel('date'),
		FieldPanel('intro'),
		FieldPanel('featured_image'),
	]
	
	def get_context(self, request):
		"""更新上下文以包含当前目录下的子页面，支持搜索筛选"""
		context = super().get_context(request)
		
		# 获取搜索和过滤参数
		search_query = request.GET.get('search', '')
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		page_number = request.GET.get('page')
		
		# 只获取当前目录的直接子页面
		child_pages = self.get_children().live()
		
		# 应用搜索过滤
		if search_query:
			child_pages = child_pages.filter(title__icontains=search_query)
		
		# 将查询集转换为具体页面实例列表
		specific_child_pages = list(child_pages.specific())
		
		# 应用日期范围过滤
		if start_date or end_date:
			filtered_pages = []
			
			for page in specific_child_pages:
				# 检查页面是否有date属性
				if not hasattr(page, 'date'):
					continue
				
				include_page = True
				
				if start_date:
					start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
					if page.date < start_date_obj:
						include_page = False
				
				if end_date and include_page:
					end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
					if page.date > end_date_obj:
						include_page = False
				
				if include_page:
					filtered_pages.append(page)
			
			specific_child_pages = filtered_pages
		
		# 对结果进行排序（按日期降序，但要注意处理没有date字段的页面）
		def sort_key(page):
			if hasattr(page, 'date'):
				return page.date
			# 对于没有date字段的页面，使用发布日期或默认最早日期
			if page.first_published_at:
				return page.first_published_at.date()
			return date.min
		
		specific_child_pages.sort(key=sort_key, reverse=True)
		
		# 分页处理
		paginator = Paginator(specific_child_pages, 20)  # 每页20篇
		
		try:
			paginated_pages = paginator.page(page_number)
		except PageNotAnInteger:
			paginated_pages = paginator.page(1)
		except EmptyPage:
			paginated_pages = paginator.page(paginator.num_pages)
		
		# 将结果添加到上下文
		context['blog_pages'] = paginated_pages
		context['search_query'] = search_query
		context['start_date'] = start_date
		context['end_date'] = end_date
		
		return context
	
	class Meta:
		verbose_name = "博客索引页"
		verbose_name_plural = "博客索引页"



		
# 博客页面
class BlogPage(Page):
	"""博客页面，内容存储在 MongoDB"""

	
	date = models.DateField("发布日期") # 发布日期
	intro = models.CharField("简介", max_length=500) # 简介
	
	# 作者字段
	authors = ParentalManyToManyField('blog.Author', blank=True)
	
	# 分类
	categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
	
	# 标签
	tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
	
	featured_image = models.ForeignKey(
		'BlogImage',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	) # 特色图片

	mongo_content_id = models.CharField("MongoDB内容ID", max_length=50, blank=True, null=True)

	# StreamField定义，用于编辑界面，实际内容存储在MongoDB
	body = StreamField([
		# 富文本块 - 使用Wagtail内置编辑器
		('rich_text', RichTextBlock(
			features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic',
			          'ol', 'ul', 'hr', 'link', 'document-link', 'image',
			          'embed', 'code', 'superscript', 'subscript', 'strikethrough',
			          'blockquote'],
			label="富文本"
		)),

		# Markdown块 - 使用wagtail-markdown (包含代码高亮和数学公式支持)
		('markdown_block', MarkdownBlock(
			icon='code',
			label="Markdown"
		)),
		
		# 嵌入块 - 用于嵌入外部内容
		('embed_block', EmbedBlock(
			label="嵌入媒体",
			help_text="从YouTube、Vimeo等插入内容"
		)),
		
		# 表格块
		('table_block', CustomTableBlock(
			label="表格"
		)),
		
		# 原始HTML - 高级用户使用
		('raw_html', RawHTMLBlock(
			label="原始HTML",
			help_text="适用于高级用户的HTML代码插入"
		)),

		# 媒体文件
		('document_block', DocumentChooserBlock(icon='doc-full', label="文档块")),
		('image_block', ImageChooserBlock(icon='image', label="图片块")),
		('audio_block', AudioBlock(icon='media', label="音频块")),
		('video_block', VideoBlock(icon='media', label="视频块")),
	], use_json_field=True, blank=True, null=True)


	# 索引字段
	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.FilterField('date'),
		index.FilterField('tags'),
		index.FilterField('categories'),
	]

	# 后台编辑面板
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('date'),
			FieldPanel('tags'),
			FieldPanel("authors", widget=forms.CheckboxSelectMultiple),  # 添加作者字段到面板中
			FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
		], heading="博客信息"),
		FieldPanel('intro'),
		FieldPanel('featured_image'),
		FieldPanel('body'),
		InlinePanel('gallery_images', label="Gallery images"),
	]
	
	# FieldPanel： FieldPanel 用于在 Wagtail 后台编辑界面中显示和编辑单个字段。这个字段通常是直接定义在当前模型上的 Django 模型字段。
	# InlinePanel： 用于在 Wagtail 后台编辑界面中管理与当前模型实例有关联的一组子级模型实例。它通常用于管理通过 ParentalKey 建立的父子关系。
	
	class Meta:
		verbose_name = "博客页面"
		verbose_name_plural = "博客页面"
		indexes = [
			models.Index(fields=['date']),  # 为博客发布日期添加索引，优化时间筛选查询
		]
	
	def delete(self, *args, **kwargs):
		"""重写删除方法，同时删除 MongoDB 中的内容"""
		if self.mongo_content_id:
			mongo_manager = MongoManager()
			mongo_manager.delete_blog_content(self.mongo_content_id)
		super().delete(*args, **kwargs)
	
	# 在BlogPage类中
	def save(self, *args, **kwargs):
		"""重写保存方法，将内容存储到MongoDB，同时保留基本元数据在MySQL"""
		
		is_new = self.pk is None
		# 保存StreamField内容的副本
		temp_body = self.body
		
		# 保存到MySQL (不含body内容)
		# 临时清空body以避免存储到MySQL
		temp_body_raw = None
		if hasattr(self.body, 'raw_data'):
			temp_body_raw = self.body.raw_data
			self.body = []
		
		# 调用父类的save方法保存元数据到MySQL
		super().save(*args, **kwargs)
		
		# 恢复body以便处理
		if temp_body_raw is not None:
			
			self.body = StreamValue(self.body.stream_block, temp_body_raw, is_lazy=True)
		else:
			self.body = temp_body
		
		# 准备MongoDB内容数据
		mongo_manager = MongoManager()
		
		# 构建完整的内容对象
		content_data = {
			'page_id': self.pk,
			'title': self.title,
			'intro': self.intro,
			'last_updated': self.last_published_at.isoformat() if self.last_published_at else None,
		}
		
		# 获取body内容的JSON表示
		try:
			
			from blog.markdown_helpers import MarkdownHelper
			
			# 核心改进：确保body有效
			if hasattr(self.body, 'raw_data') and self.body.raw_data:
				# 处理Markdown块
				raw_data = self.body.raw_data
				for block in raw_data:
					if isinstance(block, dict) and block.get('type') == 'markdown_block' and 'value' in block:
						block['value'] = MarkdownHelper.process_markdown_for_storage(block['value'])
				
				content_data['body'] = raw_data
			else:
				# 使用适配器处理
				content_data['body'] = MongoDBStreamFieldAdapter.to_mongodb(self.body)
		
		except Exception as e:
			logger.error(f"转换StreamField数据出错: {e}")
			logger.error(traceback.format_exc())
			# 尝试使用原始raw_data
			if temp_body_raw is not None:
				content_data['body'] = temp_body_raw
		
		# 保存到MongoDB
		content_id = mongo_manager.save_blog_content(content_data, self.mongo_content_id)
		
		# 更新mongo_content_id (如果有变化)
		if is_new or not self.mongo_content_id or self.mongo_content_id != content_id:
			self.mongo_content_id = content_id
			# 直接更新数据库，避免递归调用save
			type(self).objects.filter(pk=self.pk).update(mongo_content_id=content_id, body=[])
	
	def get_content_from_mongodb(self):
		"""从MongoDB获取内容并转换为适合编辑器的格式"""
		
		if not self.mongo_content_id:
			logger.warning(f"页面没有 mongo_content_id: 页面ID={self.id}")
			return None
		
		try:
			mongo_manager = MongoManager()
			content = mongo_manager.get_blog_content(self.mongo_content_id)
			
			if not content:
				logger.warning(f"MongoDB中未找到内容: mongo_content_id={self.mongo_content_id}")
				return None
			
			if 'body' not in content:
				logger.warning(f"从MongoDB获取的内容缺少body字段: {list(content.keys())}")
				return None
			
			# 验证内容格式
			if not isinstance(content['body'], list):
				logger.warning(f"MongoDB中的body不是列表格式: {type(content['body'])}")
				# 尝试转换
				if isinstance(content['body'], str):
					import json
					try:
						content['body'] = json.loads(content['body'])
					except:
						logger.error("无法将字符串格式的body转换为列表")
						return None
				else:
					return None
			
			# 确保所有块都有必要的字段
			for i, block in enumerate(content['body']):
				if isinstance(block, dict):
					# 确保有类型字段
					if 'type' not in block:
						logger.warning(f"块 #{i} 缺少type字段")
						continue
					
					# 确保有ID字段
					if 'id' not in block or not block['id']:
						import uuid
						block['id'] = str(uuid.uuid4())
					
					# 确保有value字段
					if 'value' not in block:
						logger.warning(f"块 #{i} 缺少value字段，添加空值")
						block['value'] = ""
					
					# 特殊处理markdown块
					if block['type'] == 'markdown_block':
						
						block['value'] = MarkdownHelper.process_markdown_for_editor(block['value'])
			
			return content
		except Exception as e:
			logger.error(f"从MongoDB获取内容时出错: {e}")
			logger.error(traceback.format_exc())
			return None
	
	def serve(self, request):
		"""重写serve方法以确保展示MongoDB中的内容"""
	
		# 获取MongoDB内容
		mongo_content = self.get_content_from_mongodb()
		
		if mongo_content and 'body' in mongo_content:
			# 临时保存原始body
			original_body = self.body
			
			try:
				# 设置MongoDB中的body内容
				# 使用MongoDBStreamFieldAdapter处理转换
				try:
					self.body = MongoDBStreamFieldAdapter.from_mongodb(mongo_content['body'], self.body.stream_block)
				except Exception as e:
					logger.error(f"使用适配器创建StreamValue失败: {e}")
					# 回退到简单方法
					self.body = StreamValue(self.body.stream_block, mongo_content['body'], is_lazy=True)
			
			except Exception as e:
				logger.error(f"设置MongoDB内容到StreamField时出错: {e}")
				logger.error(traceback.format_exc())
				# 恢复原始body
				self.body = original_body
		else:
			logger.warning(f"未能从MongoDB获取页面内容，使用数据库中的body")
		
		# 调用父类的serve方法渲染页面
		return super().serve(request)

	def get_prev_post(self):
		"""获取同类别的上一篇文章"""
		if not self.categories.exists():
			# 没有分类时，按时间获取
			return BlogPage.objects.live().filter(
				first_published_at__lt=self.first_published_at
			).order_by('-first_published_at').first()
		# 获取当前文章的分类
		category_ids = self.categories.values_list('id', flat=True)
		# 同类别且发布日期早于当前文章的最新一篇
		return BlogPage.objects.live().filter(
			categories__id__in=category_ids,
			first_published_at__lt=self.first_published_at
		).distinct().order_by('-first_published_at').first()
	
	
	def get_next_post(self):
		"""获取同类别的下一篇文章"""
		if not self.categories.exists():
			# 没有分类时，按时间获取
			return BlogPage.objects.live().filter(
				first_published_at__gt=self.first_published_at
			).order_by('first_published_at').first()
		# 获取当前文章的分类
		category_ids = self.categories.values_list('id', flat=True)
		# 同类别且发布日期晚于当前文章的最早一篇
		return BlogPage.objects.live().filter(
			categories__id__in=category_ids,
			first_published_at__gt=self.first_published_at
		).distinct().order_by('first_published_at').first()
	
	def get_related_posts_by_tags(self, max_posts=5):
		"""根据标签获取相关文章"""
		# 获取当前文章的所有标签
		if not self.tags.exists():
			return BlogPage.objects.none()
		
		tag_ids = [tag.tag_id for tag in self.tagged_items.all()]
		
		# 查找至少有一个相同标签的其他文章
		related_posts = BlogPage.objects.live().filter(
			tagged_items__tag_id__in=tag_ids
		).exclude(
			id=self.id  # 排除当前文章
		).distinct()
		
		# 按相同标签数量和发布日期排序
		related_posts = related_posts.annotate(
			same_tags=models.Count('tagged_items', filter=models.Q(tagged_items__tag_id__in=tag_ids))
		).order_by('-same_tags', '-first_published_at')[:max_posts]
		
		return related_posts
	
	# 在BlogPage类中添加这些方法
	def get_view_count(self):
		"""获取页面的访问量统计"""
		
		
		today = date.today()
		
		# 尝试从数据库获取今日数据
		try:
			view_count = PageViewCount.objects.get(page=self, date=today)
			count = view_count.count
			unique_count = view_count.unique_count
		except PageViewCount.DoesNotExist:
			# 从Redis检查是否有今日计数
			try:
				import redis
				from django.conf import settings
				
				# 使用Redis连接
				redis_client = redis.Redis(
					host=getattr(settings, 'REDIS_HOST', 'localhost'),
					port=getattr(settings, 'REDIS_PORT', 6379),
					password=getattr(settings, 'REDIS_PASSWORD', None),
					db=getattr(settings, 'REDIS_DB', 0)
				)
				
				# 获取今日数据
				count = int(redis_client.get(f"page_views:{self.id}") or 0)
				unique_count = redis_client.scard(f"page_unique_views:{self.id}:{today.isoformat()}")
			except Exception:
				count = 0
				unique_count = 0
		
		# 获取总计数（历史累计）
		total_counts = PageViewCount.objects.filter(page=self).aggregate(
			total=Sum('count'),
			total_unique=Sum('unique_count')
		)
		
		total_count = total_counts.get('total') or 0
		total_unique_count = total_counts.get('total_unique') or 0
		
		# 添加Redis中可能未同步的计数
		total_count += count
		total_unique_count += unique_count
		
		return {
			'today': count,
			'today_unique': unique_count,
			'total': total_count,
			'total_unique': total_unique_count
		}
	
	def get_reactions(self):
		"""获取页面的反应统计"""
		
		# 获取所有反应类型
		reaction_types = ReactionType.objects.all()
		
		# 获取该页面的反应计数
		reaction_counts = Reaction.objects.filter(page=self).values(
			'reaction_type'
		).annotate(
			count=Count('id')
		)
		
		# 转换为字典格式
		counts = {r['reaction_type']: r['count'] for r in reaction_counts}
		
		# 构建完整结果
		result = []
		for rt in reaction_types:
			result.append({
				'id': rt.id,
				'name': rt.name,
				'icon': rt.icon,
				'count': counts.get(rt.id, 0)
			})
		
		return result
	
	def user_has_reacted(self, request):
		"""检查当前用户是否对页面有反应"""
		if request.user.is_authenticated:
			return Reaction.objects.filter(
				page=self,
				user=request.user
			).values_list('reaction_type_id', flat=True).first()
		elif request.session.session_key:
			return Reaction.objects.filter(
				page=self,
				session_key=request.session.session_key
			).values_list('reaction_type_id', flat=True).first()
		return None


class BlogPageGalleryImage(Orderable):
	"""博客页面画廊图片模型"""
	
	# Orderable 是 Wagtail 提供的一个 Mixin 类。Mixin 是一种在 Python 中复用代码的方式，您可以将一个或多个 Mixin 类与其他类一起继承，从而将 Mixin 中的功能“混合”到您的类中。
	# Orderable Mixin 的主要作用是为您的模型添加一个 sort_order 字段。这个字段是一个整数，用于记录模型实例的排序顺序。
	
	# 关联到BlogPage
	page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
	
	# 关联您自定义的图片模型
	image = models.ForeignKey(
	    'blog.BlogImage', # <-- 使用您自定义的图片模型
	    on_delete=models.CASCADE,
	    related_name='+'
	)
	caption = models.CharField(blank=True, max_length=250)
	
	panels = [
	    FieldPanel('image'),
	    FieldPanel('caption'),
	]

# 页面访问记录模型
@register_snippet
class PageView(models.Model):
	
	
	page = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, related_name='page_views')
	session_key = models.CharField(max_length=100, blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
	ip_address = models.GenericIPAddressField()
	user_agent = models.CharField(max_length=255, blank=True)
	viewed_at = models.DateTimeField(auto_now_add=True)
	is_unique = models.BooleanField(default=False)
	
	class Meta:
		verbose_name = "页面访问记录"
		verbose_name_plural = "页面访问记录"
		indexes = [
			models.Index(fields=['page', 'viewed_at']),
			models.Index(fields=['viewed_at']),
		]


# 访问统计聚合模型
@register_snippet
class PageViewCount(models.Model):
	page = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, related_name='view_counts')
	date = models.DateField()
	count = models.PositiveIntegerField(default=0)  # 总访问量
	unique_count = models.PositiveIntegerField(default=0)  # 唯一访问量
	
	class Meta:
		verbose_name = "页面访问统计"
		verbose_name_plural = "页面访问统计"
		unique_together = ('page', 'date')
	
	def __str__(self):
		return f"{self.page.title} - {self.date} - {self.count}次访问"


# 反应类型模型
@register_snippet
class ReactionType(models.Model):
	
	name = models.CharField("反应名称", max_length=50)
	icon = models.CharField("图标CSS类", max_length=50)
	display_order = models.PositiveSmallIntegerField("显示顺序", default=0)
	
	class Meta:
		verbose_name = "反应类型"
		verbose_name_plural = "反应类型"
		ordering = ['display_order']
	
	def __str__(self):
		return self.name


	
# 用户反应模型
@register_snippet
class Reaction(models.Model):
	
	page = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, related_name='reactions')
	reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE, related_name='reactions')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
	session_key = models.CharField(max_length=100, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name = "用户反应"
		verbose_name_plural = "用户反应"
		unique_together = (
			('page', 'user'),  # 每个用户对每个页面只能有一个反应
			('page', 'session_key', 'ip_address')  # 对于匿名用户，按会话和IP限制
		)
	
	def __str__(self):
		user_str = self.user.username if self.user else f"匿名({self.session_key[:10]})"
		return f"{user_str} - {self.reaction_type.name} - {self.page.title}"


@register_snippet
class Author(models.Model):
	"""作者模型"""
	
	name = models.CharField(max_length=255)  # 作者名称
	author_image = models.ForeignKey(
		'blog.BlogImage',
		null=True,  # 允许为空
		blank=True,  # 允许在表单中为空
		on_delete=models.SET_NULL,  # 删除图片时设置为空
		related_name='+'  # 不需要反向关系
	)  # 作者图片
	
	# 使用 RichTextField 允许在后台编辑时使用富文本格式
	bio = StreamField([
		('paragraph', RichTextBlock(
			features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic',
			          'ol', 'ul', 'hr', 'link', 'document-link', 'image',
			          'embed', 'code', 'superscript', 'subscript', 'strikethrough',
			          'blockquote'],
			label="段落",icon="pilcrow"
		)),
		('image', ImageChooserBlock(icon="image", label="图片")),  # <-- 添加图片选择块
	],
		use_json_field=True,  # 推荐为新的 StreamFields 使用 JSON 存储
		blank=True,
		verbose_name="个人简介"
	)
	
	# 列表中的每个元素都定义了在Wagtail管理后台中显示的一个字段。 panels列表决定了哪些字段将出现在Snippet的编辑界面中。
	# 您在这里使用的是panels而不是content_panels；由于片段通常不需要诸如slug或发布日期之类的字段，
	# 因此它们的编辑界面不会分为单独的“内容”/“推广”/“设置”选项卡。因此无需区分“内容面板”和“推广面板”。
	panels = [
		FieldPanel('name'),
		FieldPanel('author_image'),
		FieldPanel('bio', heading="个人简介"),  # 使用 StreamFieldPanel 显示富文本简介
	]  # 在管理界面中显示的字段
	
	def __str__(self):
		return self.name
	
	# 在 Author 类中添加这个方法
	def get_bio_preview(self, word_limit=3):
		"""获取简介的预览版本，限制字数"""
		if not self.bio:
			return ""
		
		preview_text = ""
		word_count = 0
		
		for block in self.bio:
			if block.block_type == 'paragraph':
				# 处理段落块
				block_text = strip_tags(str(block.value))
				
				# 分割单词并计算
				words = block_text.split()
				remaining_words = word_limit - word_count
				
				if remaining_words <= 0:
					break
				
				if len(words) <= remaining_words:
					preview_text += block_text + " "
					word_count += len(words)
				else:
					preview_text += " ".join(words[:remaining_words]) + "..."
					break
		
		# 忽略图片块，只处理文本
		
		return preview_text.strip()
	
	def get_bio_preview_html(self, word_limit=3):
		"""获取带HTML格式的简介预览"""
		if not self.bio:
			return ""
		
		preview_html = ""
		word_count = 0
		
		for block in self.bio:
			if block.block_type == 'paragraph':
				block_html = str(block.value)
				block_text = strip_tags(block_html)
				
				words = block_text.split()
				remaining_words = word_limit - word_count
				
				if remaining_words <= 0:
					break
				
				if len(words) <= remaining_words:
					preview_html += f"<p>{block_html}</p>"
					word_count += len(words)
				else:
					# 截断HTML内容
					truncated_text = " ".join(words[:remaining_words]) + "..."
					preview_html += f"<p>{truncated_text}</p>"
					break
		
		return mark_safe(preview_html)
	
	class Meta:
		verbose_name = '作者'
		verbose_name_plural = '作者列表'