# blog/management/commands/rebuild_mongodb_indexes.py
from django.core.management.base import BaseCommand
from wagtailblog3.mongo import MongoManager

# 指令：python manage.py rebuild_mongodb_indexes
class Command(BaseCommand):
	help = '删除现有MongoDB索引并重建优化的中文搜索索引'
	
	def handle(self, *args, **options):
		mongo = MongoManager()
		
		self.stdout.write('开始重建MongoDB索引...')
		
		# 获取现有索引
		try:
			indexes = list(mongo.blog_content.list_indexes())
			self.stdout.write(f'发现 {len(indexes)} 个现有索引')
			
			# 删除全文索引
			for index in indexes:
				index_info = index.to_dict()
				if 'weights' in index_info:  # 识别文本索引
					index_name = index_info.get('name')
					self.stdout.write(f'删除全文索引: {index_name}')
					mongo.blog_content.drop_index(index_name)
			
			# 创建新的全文索引
			self.stdout.write('创建新的全文索引...')
			mongo.blog_content.create_index([
				("title_tokens", "text"),
				("intro_tokens", "text"),
				("body_text", "text")
			], weights={
				"title_tokens": 10,
				"intro_tokens": 5,
				"body_text": 1
			})
			
			self.stdout.write(self.style.SUCCESS('成功重建MongoDB索引！'))
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'重建索引时出错: {e}'))