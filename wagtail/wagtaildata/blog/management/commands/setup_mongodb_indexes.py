# blog/management/commands/setup_mongodb_indexes.py

from django.core.management.base import BaseCommand
from blog.utils import get_mongo_db


class Command(BaseCommand):
	help = '为MongoDB博客内容创建文本索引'
	
	def handle(self, *args, **options):
		mongo_db = get_mongo_db()
		
		# 更改这一行，使用"is not None"而不是布尔测试
		if mongo_db is not None:
			# 删除现有索引
			try:
				mongo_db['blog_contents'].drop_indexes()
				self.stdout.write(self.style.SUCCESS('已删除现有索引'))
			except Exception as e:
				self.stdout.write(self.style.WARNING(f'删除索引时出错: {e}'))
			
			# 创建文本索引
			try:
				mongo_db['blog_contents'].create_index(
					[
						('title', 'text'),
						('stream_data.value', 'text')
					],
					weights={
						'title': 10, # 标题权重
						'search_text': 5 # 搜索文本权重
					},
					default_language='none'
				)
				self.stdout.write(self.style.SUCCESS('成功创建MongoDB文本索引'))
			except Exception as e:
				self.stdout.write(self.style.ERROR(f'创建索引时出错: {e}'))
		else:
			self.stdout.write(self.style.ERROR('无法连接到MongoDB'))