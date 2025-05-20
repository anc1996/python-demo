from django.core.management.base import BaseCommand
from wagtail.search.backends import get_search_backend
from wagtail.models import Page


class Command(BaseCommand):
	help = '修复 Elasticsearch 7 搜索配置'
	
	def handle(self, *args, **options):
		# 获取 Elasticsearch 搜索后端
		backend = get_search_backend()
		
		# 检查是否是 Elasticsearch 后端
		if 'elasticsearch' not in backend.__class__.__module__:
			self.stdout.write(self.style.ERROR('当前搜索后端不是 Elasticsearch！请检查设置。'))
			return
		
		try:
			# 删除现有索引
			self.stdout.write('删除现有索引...')
			backend.reset_index()
			self.stdout.write(self.style.SUCCESS('已删除索引'))
			
			# 更新映射配置
			if hasattr(backend, 'es'):
				# 获取索引名称
				index_names = []
				for index in backend.es.cat.indices(format='json'):
					if index.get('index').startswith('wagtaildata'):
						index_names.append(index.get('index'))
				
				self.stdout.write(f"找到索引: {', '.join(index_names)}")
				
				# 确保映射正确包含fields
				for index_name in index_names:
					# 获取现有映射
					self.stdout.write(f"正在更新索引 {index_name} 的映射...")
					
					# 使用put_mapping更新映射
					try:
						# 更新索引设置，确保source字段可用
						backend.es.indices.put_settings(
							index=index_name,
							body={
								"index": {
									"query": {
										"default_field": "_all"
									}
								}
							}
						)
					except Exception as e:
						self.stdout.write(self.style.WARNING(f"更新索引设置时出错: {e}"))
			
			# 重新索引所有页面
			self.stdout.write('重新索引所有页面...')
			all_pages = Page.objects.all()
			count = 0
			
			for page in all_pages:
				try:
					backend.add(page)
					count += 1
				except Exception as e:
					self.stdout.write(self.style.ERROR(f"为页面 {page.id} 创建索引时出错: {e}"))
			
			self.stdout.write(self.style.SUCCESS(f"已为 {count} 个页面重建索引"))
			self.stdout.write(self.style.SUCCESS('Elasticsearch 索引配置已更新!'))
		
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'发生错误: {e}'))