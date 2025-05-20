"""
Management command to reindex all blog content in MongoDB and rebuild search indices
"""

import time
import logging
from django.core.management.base import BaseCommand
from blog.models import BlogPage
from blog.utils import sync_to_mongodb, get_mongo_db

logger = logging.getLogger(__name__)


class Command(BaseCommand):
	help = '将所有博客内容重新索引到MongoDB，并重建MySQL索引'
	
	def add_arguments(self, parser):
		parser.add_argument(
			'--skip-mysql',
			action='store_true',
			help='跳过MySQL索引重建',
		)
		parser.add_argument(
			'--skip-mongo',
			action='store_true',
			help='跳过MongoDB索引重建',
		)
	
	def handle(self, *args, **options):
		skip_mysql = options['skip_mysql']
		skip_mongo = options['skip_mongo']
		
		start_time = time.time()
		self.stdout.write(self.style.SUCCESS('开始重建博客索引...'))
		
		# 获取所有博客页面
		blog_pages = BlogPage.objects.all()
		total_pages = blog_pages.count()
		self.stdout.write(f'找到 {total_pages} 篇博客文章')
		
		# 清除MongoDB中现有的博客内容（可选）
		if not skip_mongo:
			try:
				mongo_db = get_mongo_db()
				if mongo_db:
					blog_collection = mongo_db['blog_contents']
					deleted = blog_collection.delete_many({})
					self.stdout.write(f'已从MongoDB中删除 {deleted.deleted_count} 条博客记录')
			except Exception as e:
				self.stdout.write(self.style.ERROR(f'删除MongoDB记录时出错: {e}'))
		
		# 重建索引
		success_count = 0
		mongo_success = 0
		mysql_success = 0
		
		for i, page in enumerate(blog_pages, 1):
			self.stdout.write(f'处理 [{i}/{total_pages}] {page.title}')
			
			# 同步到MongoDB
			if not skip_mongo:
				try:
					mongo_id = sync_to_mongodb(page)
					if mongo_id:
						mongo_success += 1
						self.stdout.write(f'  MongoDB同步成功: {mongo_id}')
					else:
						self.stdout.write(self.style.WARNING(f'  MongoDB同步失败'))
				except Exception as e:
					self.stdout.write(self.style.ERROR(f'  MongoDB同步出错: {e}'))
			
			# 更新MySQL索引
			if not skip_mysql:
				try:
					from wagtail.search.backends import get_search_backend
					search_backend = get_search_backend()
					search_backend.add(page)
					mysql_success += 1
					self.stdout.write(f'  MySQL索引更新成功')
				except Exception as e:
					self.stdout.write(self.style.ERROR(f'  MySQL索引更新出错: {e}'))
			
			if (not skip_mongo and mongo_id) or (not skip_mysql and mysql_success > 0) or (skip_mongo and skip_mysql):
				success_count += 1
		
		# 总结
		total_time = time.time() - start_time
		self.stdout.write(self.style.SUCCESS(f'重建索引完成! 耗时: {total_time:.2f} 秒'))
		self.stdout.write(f'成功处理 {success_count}/{total_pages} 篇博客')
		
		if not skip_mongo:
			self.stdout.write(f'MongoDB同步成功: {mongo_success}/{total_pages}')
		
		if not skip_mysql:
			self.stdout.write(f'MySQL索引更新成功: {mysql_success}/{total_pages}')