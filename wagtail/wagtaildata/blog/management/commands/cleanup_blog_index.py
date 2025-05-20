# blog/management/commands/cleanup_blog_index.py

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
	help = '清理wagtailsearch_indexentry表中的博客全文内容'
	
	def handle(self, *args, **options):
		self.stdout.write("开始清理博客索引...")
		
		with connection.cursor() as cursor:
			# 首先备份现有数据
			self.stdout.write("创建索引备份...")
			cursor.execute("""
                CREATE TABLE IF NOT EXISTS wagtailsearch_indexentry_backup
                SELECT * FROM wagtailsearch_indexentry
            """)
			
			# 更新所有BlogPage(content_type_id=34)的记录，清空body字段但保留其他字段
			self.stdout.write("清理BlogPage内容...")
			cursor.execute("""
                UPDATE wagtailsearch_indexentry
                SET body = ''
                WHERE content_type_id = 34
            """)
			
			# 统计清理的记录数
			cursor.execute("""
                SELECT COUNT(*) FROM wagtailsearch_indexentry
                WHERE content_type_id = 34
            """)
			count = cursor.fetchone()[0]
		
		self.stdout.write(self.style.SUCCESS(f"成功清理 {count} 条博客页面索引记录。"))
		self.stdout.write("请确保已经正确设置了MongoDB索引:")
		self.stdout.write("python manage.py setup_mongodb_indexes")