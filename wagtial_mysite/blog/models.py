from django import forms  # 导入 django.forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.http import Http404
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail.images.models import Image
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from django.utils.translation import gettext_lazy as _  # 用于翻译
from wagtail.snippets.models import register_snippet

# New imports added for ClusterTaggableManager, TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class BlogIndexPage(Page):
	intro = RichTextField(blank=True)
	
	content_panels = Page.content_panels + [
		FieldPanel('intro')
	]
	
	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)  # 获取父类的上下文
		# get_children() 方法用于获取当前页面的所有子页面。
		# 获取BlogIndexPage的所有子页面，也就是BlogPage列表，并按发布时间降序排列
		blogpages = self.get_children().live().order_by('-first_published_at')
		# 添加分页功能
		page = request.GET.get('page')
		paginator = Paginator(blogpages, 5)
		try:
			blogpages = paginator.page(page)
		except PageNotAnInteger:
			blogpages = paginator.page(1)
		except EmptyPage:
			blogpages = paginator.page(paginator.num_pages)
		
		context['blogpages'] = blogpages
		return context


# 将标签链接到 BlogPage 的新模型
class BlogPageTag(TaggedItemBase):
    """通过中间表将标签添加到BlogPage模型"""
    # 通过 ParentalKey 将 BlogPageTag 连接到 BlogPage 模型
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )



class BlogPage(Page):
    """博客文章页面模型"""
    
    date = models.DateField("Post date")  # 日期字段
    intro = models.CharField(max_length=250)  # 简介字段
    body = RichTextField(blank=True)  # 博客文章的正文内容，使用 RichTextField 支持富文本编辑。
	
    # 新增：作者字段
    # ParentalManyToManyField：
    authors = ParentalManyToManyField('blog.Author', blank=True)
    
    categories = ParentalManyToManyField(
        'blog.BlogCategory',
        blank=True,
        help_text=_("Select a category for this post"),
    )  # 多对多关系，允许选择多个分类
    
    # 添加 main_image 字段
    main_image = models.ForeignKey(
        Image,  # 使用 Wagtail 的 Image 模型
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # 如果图片被删除，则将 main_image 设置为 null
        related_name='+'  # 表示不需要反向关系
    )
    
    # Add this: 标签
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]  # 定义可以被搜索的字段，这里包括 intro 和 body。
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),  # 添加作者字段到面板中
            FieldPanel("tags"),  # 添加标签
        ], heading="Blog Post Information"),  # 将date和authors字段放到一个面板中
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),  # 添加分类字段到面板中
        InlinePanel('gallery_images', label="Gallery images"),  # 添加 gallery_images
        FieldPanel('main_image'),  # 添加 main_image 字段到面板中
    ]
    
    # 定义一个 slug 字段，用于 URL 中的分类标识符。
    parent_page_types = ['blog.BlogIndexPage']  # 限定父页面类型
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # 尝试获取 BlogTagIndexPage 页面
        tag_page = self.get_parent().specific.get_children().type(BlogTagIndexPage).live().first()

        if tag_page is None:
            #  如果找不到页面，抛出 404 错误
            raise Http404("BlogTagIndexPage not found")

        context['tag_page'] = tag_page
        context['categories'] = self.categories.all()  # 将所有分类传递到模板
        return context



# 使用wagtail.snippets.models.register_snippet将BlogCategory注册为一个 Snippet。
# 这使你可以在 Wagtail 管理界面中创建和管理BlogCategory对象，并且这些对象可以被添加到你的页面模型中，比如BlogPage。
@register_snippet
class BlogCategory(models.Model):
	""""""
	
	name = models.CharField(max_length=100)  # 分类名称
	slug = models.SlugField(
		verbose_name=_("slug"),
		allow_unicode=True,
		max_length=255,
		help_text=_("A slug to identify posts by this category"),
		unique=True,  # 确保每个分类的 slug 是唯一的
	)
	
	# 定义一个 slug 字段，用于 URL 中的分类标识符。
	panels = [
		FieldPanel('name'),
		FieldPanel('slug'),
	]
	
	class Meta:
		verbose_name = _("Blog Category")  # 在管理界面中显示的名称
		verbose_name_plural = _("Blog Categories")  # 复数形式
		ordering = ['name']  # 按名称排序
	
	def __str__(self):
		return self.name
	
	# 根据BlogCategory的slug查找对应的CategoryPage。
	def get_page(self):
		return CategoryPage.objects.filter(slug=self.slug).first()  # 获取与当前分类关联的CategoryPage对象


class CategoryIndexPage(Page):
	"""这是一个标准的 Wagtail Page 模型，作为所有分类页面的父页面。"""
	
	intro = RichTextField(blank=True)  # 简介字段
	
	content_panels = Page.content_panels + [FieldPanel('intro')]  # 添加简介字段到面板中
	
	# 只允许BlogIndexPage作为父页面
	parent_page_types = ['blog.BlogIndexPage']  # 限定父页面类型
	
	# 定义获取上下文的方法
	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		# 获取所有已经有对应CategoryPage
		categories = CategoryPage.objects.live().filter()
		context['categories'] = categories
		return context


class CategoryPage(Page):
	""" 这是一个 Page 模型，每个页面对应一个分类。它的 get_context 方法获取属于该分类的所有博客文章。"""
	
	# 定义一个分类页面，用于显示特定分类下的文章
	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		# 获取当前分类的slug
		category_slug = self.slug
		# 获取所有博客文章
		blogpages = BlogPage.objects.live()
		# 过滤出属于当前分类的文章
		blogpages = blogpages.filter(categories__slug=category_slug)
		# 将文章列表添加到上下文中
		context['blogpages'] = blogpages
		return context
	
	# 定义父页面类型
	parent_page_types = ['blog.CategoryIndexPage']  # 限定父页面类型
	
	template = 'blog/category_page.html'  # 指定模板文件


class BlogPageGalleryImage(Orderable):
	""" """
	# 从Orderable继承会向模型添加一个sort_order字段，以跟踪图库中图像的顺序。
	# BlogPage的ParentalKey将图库图像附加到特定页面。ParentalKey工作方式与ForeignKey类似，但它还将BlogPageGalleryImage
	# 定义为BlogPage模型的“子级”，因此在提交审核和跟踪修订历史等操作中，它被视为页面的基本部分。
	page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
	
	# image是Wagtail内置Image模型的ForeignKey，用于存储实际图像。这在页面编辑器中显示为一个弹出界面，用于选择现有图像或上传新图像。
	# 这在页面和图像之间建立了多对多关系。
	image = models.ForeignKey(
		'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
	)
	# 将InlinePanel添加到BlogPage.content_panels使得图库图像可以在BlogPage的编辑界面上使用。
	caption = models.CharField(blank=True, max_length=250)
	panels = [
		FieldPanel('image'),
		FieldPanel('caption'),
	]


@register_snippet
class Author(models.Model):
	"""作者模型"""
	
	name = models.CharField(max_length=255)  # 作者名称
	author_image = models.ForeignKey(
		Image,
		null=True,  # 允许为空
		blank=True,  # 允许在表单中为空
		on_delete=models.SET_NULL,  # 删除图片时设置为空
		related_name='+'  # 不需要反向关系
	)  # 作者图片
	
	# 列表中的每个元素都定义了在Wagtail管理后台中显示的一个字段。 panels列表决定了哪些字段将出现在Snippet的编辑界面中。
	# 您在这里使用的是panels而不是content_panels；由于片段通常不需要诸如slug或发布日期之类的字段，
	# 因此它们的编辑界面不会分为单独的“内容”/“推广”/“设置”选项卡。因此无需区分“内容面板”和“推广面板”。
	panels = [
		FieldPanel('name'),
		FieldPanel('author_image'),
	]  # 在管理界面中显示的字段
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'Authors'  # 复数形式


# 新增 BlogTagIndexPage 模型
class BlogTagIndexPage(Page):
	"""
    用于显示特定标签的所有博客文章的页面
    """
	
	def get_context(self, request, *args, **kwargs):
		"""
        修改上下文，添加带有特定标签的博客文章
        """
		# 获取请求中的 'tag' 参数
		tag = request.GET.get('tag')
		# 根据标签过滤博客文章
		blogpages = BlogPage.objects.live().filter(tags__name=tag)
		
		# 更新模板上下文
		context = super().get_context(request, *args, **kwargs)
		context['blogpages'] = blogpages
		return context
	
	class Meta:
		verbose_name = "Blog Tag Index Page"
		verbose_name_plural = "Blog Tag Index Pages"
	
