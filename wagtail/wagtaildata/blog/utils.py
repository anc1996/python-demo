import json,os,logging
from bson import ObjectId
from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage

# 这个文件主要用于处理与MinIO和MongoDB的交互

# 设置日志记录器
logger = logging.getLogger(__name__)


# 确保在Django启动时禁用代理
def disable_proxy():
	"""完全禁用代理设置"""
	import os
	
	# 保存一个全局变量，记录原始代理设置
	global _original_proxy_settings
	_original_proxy_settings = {
		'HTTP_PROXY': os.environ.pop('HTTP_PROXY', None),
		'HTTPS_PROXY': os.environ.pop('HTTPS_PROXY', None),
		'http_proxy': os.environ.pop('http_proxy', None),
		'https_proxy': os.environ.pop('https_proxy', None),
		'NO_PROXY': os.environ.get('NO_PROXY', ''),
	}
	
	# 设置NO_PROXY为通配符，确保所有连接跳过代理
	os.environ['NO_PROXY'] = '*'


# 在应用程序启动时调用此函数
disable_proxy()


class CustomS3Boto3Storage(S3Boto3Storage):
	"""
	自定义S3存储后端，在需要时禁用代理连接到MinIO
	"""
	location = ''  # 不添加前缀，保持文件路径结构
	file_overwrite = False  # 不覆盖同名文件
	
	def __init__(self, *args, **kwargs):
		# 在初始化时就禁用代理
		import os
		self._original_proxy = {
			'HTTP_PROXY': os.environ.pop('HTTP_PROXY', None),
			'HTTPS_PROXY': os.environ.pop('HTTPS_PROXY', None),
			'http_proxy': os.environ.pop('http_proxy', None),
			'https_proxy': os.environ.pop('https_proxy', None),
		}
		os.environ['NO_PROXY'] = '*'
		super().__init__(*args, **kwargs)
	
	def get_valid_name(self, name):
		"""保持原始文件名，不进行Django默认的文件名清理"""
		return name
	
	def _get_connection(self):
		"""
		重写连接方法以禁用代理
		"""
		if self._connection is None:
			# 创建没有代理的连接
			import boto3
			from django.conf import settings
			
			# 创建连接（禁用代理）
			self._connection = boto3.resource(
				's3',
				endpoint_url=self.endpoint_url,
				use_ssl=self.use_ssl,
				region_name=settings.AWS_S3_REGION_NAME,
				config=self.config,
				verify=self.verify,
				aws_access_key_id=self.access_key,
				aws_secret_access_key=self.secret_key,
				aws_session_token=self.security_token,
			)
		
		return self._connection
	
	def _save(self, name, content):
		"""确保目录结构存在后保存文件"""
		try:
			# 提取目录部分并创建"目录"
			directory = os.path.dirname(name)
			if directory:
				# 确保目录以斜杠结尾
				if not directory.endswith('/'):
					directory += '/'
				
				try:
					# 尝试创建"目录"
					self.connection.meta.client.put_object(
						Bucket=self.bucket_name,
						Key=directory,
						Body=''
					)
				except Exception as e:
					# 记录错误但继续尝试上传文件
					logger.warning(f"无法创建目录 {directory}: {e}")
			
			# 调用父类方法上传文件
			return super()._save(name, content)
		except Exception as e:
			logger.error(f"保存文件到MinIO时出错: {e}")
			raise


def get_mongo_db():
	"""
	获取MongoDB连接

	尝试从settings模块中直接获取mongo_db全局变量，
	如果不存在则根据设置创建新的连接

	Returns:
		MongoDB数据库连接对象，如果连接失败则返回None
	"""
	import sys
	
	try:
		# 尝试从settings模块中直接获取mongo_db
		settings_module = sys.modules[settings.SETTINGS_MODULE]
		if hasattr(settings_module, 'mongo_db'): # 检查是否已经存在mongo_db
			return settings_module.mongo_db
		
		# 如果方法1失败，则使用配置手动创建连接
		import pymongo
		mongo_client = pymongo.MongoClient(
			host=settings.MONGO_DB['HOST'],
			port=settings.MONGO_DB['PORT']
		)
		return mongo_client[settings.MONGO_DB['NAME']]
	except Exception as e:
		logger.error(f"获取MongoDB连接失败: {e}")
		return None


def sync_to_mongodb(blog_page):
	"""
	同步博客内容到MongoDB
	将博客的详细内容存储到MongoDB以减轻MySQL负担
	Args:
		blog_page: BlogPage实例，需要同步的博客页面

	Returns:
		str: MongoDB文档ID，如果同步失败则返回None
	"""
	print(f"开始同步博客到MongoDB: ID={blog_page.id}, 标题={blog_page.title}")
	mongo_db = get_mongo_db() # 获取MongoDB连接
	print(f"MongoDB连接: {mongo_db}")
	
	if mongo_db is None:
		logger.error("无法连接到MongoDB，内容同步失败")
		return None
	
	blog_collection = mongo_db['blog_contents']
	
	try:
		# 处理StreamField数据
		stream_data = extract_stream_data(blog_page.body)
		
		# 构建存储数据
		content_data = {
			'page_id': blog_page.id,
			'title': blog_page.title,
			'stream_data': stream_data,
			'created_at': blog_page.first_published_at.isoformat() if blog_page.first_published_at else None,
			'updated_at': blog_page.last_published_at.isoformat() if blog_page.last_published_at else None,
		}
		
		# 更新或创建MongoDB记录
		if blog_page.mongo_content_id:
			return update_mongo_document(blog_collection, blog_page, content_data)
		else:
			return create_mongo_document(blog_collection, blog_page, content_data)
	except Exception as e:
		logger.error(f"同步到MongoDB失败: {e}")
		return None


def extract_stream_data(body):
	"""
	从StreamField中提取数据，确保数据可以被MongoDB存储和搜索
	Args:
		body: 博客的body字段，StreamField类型

	Returns:
		适合存储在MongoDB的数据结构
	"""
	try:
		# 将StreamField中的每个块转换为可序列化的字典
		result = []
		for block in body:
			# 基本信息
			block_dict = {
				'type': block.block_type,
				'id': block.id
			}
			
			# 处理不同类型的块，提取可搜索的文本
			if block.block_type == 'heading':
				# 标题块
				block_dict['value'] = str(block.value)
			elif block.block_type == 'paragraph':
				# 段落块 - 富文本
				if hasattr(block.value, 'source'):
					block_dict['value'] = block.value.source
				else:
					block_dict['value'] = str(block.value)
			elif block.block_type == 'code':
				# 代码块
				if hasattr(block.value, 'code'):
					block_dict['value'] = f"Code: {block.value.code}"
				else:
					block_dict['value'] = str(block.value)
			elif block.block_type == 'math_formula':
				# 数学公式块
				if hasattr(block.value, 'formula'):
					block_dict['value'] = f"Formula: {block.value.formula}"
				else:
					block_dict['value'] = str(block.value)
			elif block.block_type == 'markdown':
				# Markdown块
				block_dict['value'] = str(block.value)
			elif block.block_type == 'image':
				# 图片块 - 保存替代文本或标题
				if hasattr(block.value, 'title'):
					block_dict['value'] = f"Image: {block.value.title}"
				else:
					block_dict['value'] = f"Image: {block.value}"
			elif block.block_type == 'video':
				# 视频块
				block_dict['value'] = f"Video: {block.value}"
			elif block.block_type == 'quote':
				# 引用块
				if hasattr(block.value, 'text'):
					block_dict['value'] = f"Quote: {block.value.text}"
				else:
					block_dict['value'] = str(block.value)
			else:
				# 其他类型
				block_dict['value'] = str(block.value)
			
			result.append(block_dict)
		return result
	except Exception as e:
		logger.error(f"提取StreamField数据时出错: {e}")
		# 最后的备选方案，转为字符串
		return str(body)

def update_mongo_document(collection, blog_page, content_data):
    """
    更新MongoDB中的文档
    Args:
        collection: MongoDB集合
        blog_page: 博客页面
        content_data: 要存储的数据

    Returns:
        str: MongoDB文档ID
    """
    try:
        mongo_id = ObjectId(blog_page.mongo_content_id) # 获取MongoDB ID
        collection.update_one(
            {'_id': mongo_id},
            {'$set': content_data}
        )
        logger.info(f"更新MongoDB博客内容: {blog_page.id} -> {mongo_id}")
        return str(mongo_id)
    except Exception as e:
        logger.error(f"MongoDB更新失败: {e}")
        # 如果更新失败，尝试创建新文档
        try:
            # 删除旧文档（如果存在）
            collection.delete_one({'page_id': blog_page.id})
            # 创建新文档
            return create_mongo_document(collection, blog_page, content_data)
        except Exception as inner_e:
            logger.error(f"MongoDB恢复创建失败: {inner_e}")
            return None

def sync_to_mongodb(blog_page):
	"""
	同步博客内容到MongoDB
	将博客的详细内容存储到MongoDB以减轻MySQL负担
	Args:
		blog_page: BlogPage实例，需要同步的博客页面

	Returns:
		str: MongoDB文档ID，如果同步失败则返回None
	"""
	logger.info(f"开始同步博客到MongoDB: ID={blog_page.id}, 标题={blog_page.title}")
	mongo_db = get_mongo_db()  # 获取MongoDB连接
	
	if mongo_db is None:
		logger.error("无法连接到MongoDB，内容同步失败")
		return None
	
	blog_collection = mongo_db['blog_contents']
	
	try:
		# 处理StreamField数据
		stream_data = extract_stream_data(blog_page.body)
		
		# 提取纯文本以便于全文搜索
		plain_text = []
		for block in stream_data:
			if 'value' in block:
				plain_text.append(str(block['value']))
		
		# 构建存储数据
		content_data = {
			'page_id': blog_page.id,
			'title': blog_page.title,
			'intro': blog_page.intro,
			'stream_data': stream_data,
			'plain_text': ' '.join(plain_text),  # 添加纯文本字段用于全文搜索
			'created_at': blog_page.first_published_at.isoformat() if blog_page.first_published_at else None,
			'updated_at': blog_page.last_published_at.isoformat() if blog_page.last_published_at else None,
		}
		
		# 更新或创建MongoDB记录
		if blog_page.mongo_content_id:
			return update_mongo_document(blog_collection, blog_page, content_data)
		else:
			return create_mongo_document(blog_collection, blog_page, content_data)
	except Exception as e:
		logger.error(f"同步到MongoDB失败: {e}")
		return None


def create_mongo_document(collection, blog_page, content_data):
	"""
	在MongoDB中创建新文档

	Args:
		collection: MongoDB集合
		blog_page: 博客页面
		content_data: 要存储的数据

	Returns:
		str: MongoDB文档ID
	"""
	try:
		result = collection.insert_one(content_data) # 插入数据
		mongo_id = result.inserted_id
		# 更新博客页面的MongoDB ID引用
		blog_page.mongo_content_id = str(mongo_id)
		blog_page.save(update_fields=['mongo_content_id'])
		logger.info(f"创建MongoDB博客内容: {blog_page.id} -> {mongo_id}")
		return str(mongo_id)
	except Exception as e:
		logger.error(f"MongoDB插入失败: {e}")
		return None


def get_blog_content_from_mongodb(mongo_content_id):
	"""
	从MongoDB获取博客内容

	Args:
		mongo_content_id: MongoDB文档ID

	Returns:
		dict: MongoDB中存储的博客内容，如果获取失败则返回None
	"""
	if not mongo_content_id:
		return None
	
	mongo_db = get_mongo_db()
	if mongo_db is None:
		logger.error("无法连接到MongoDB，获取博客内容失败")
		return None
	
	blog_collection = mongo_db['blog_contents']
	
	try:
		content = blog_collection.find_one({'_id': ObjectId(mongo_content_id)})
		return content
	except Exception as e:
		logger.error(f"MongoDB查询失败: {e}")
		return None


def cache_blog_content(blog_page):
	"""
	使用Redis缓存博客内容
	将博客的基本信息缓存到Redis中，提高读取速度

	Args:
		blog_page: BlogPage实例
	Returns:
		bool: 操作是否成功
	"""
	try:
		from django.core.cache import cache
		
		# 生成缓存键
		cache_key = f"blog_content_{blog_page.id}"
		
		# 准备缓存数据
		cache_data = {
			'id': blog_page.id,
			'title': blog_page.title,
			'intro': blog_page.intro,
			'date': blog_page.date.isoformat(),
			'last_updated': blog_page.last_published_at.isoformat() if blog_page.last_published_at else None,
			'url': blog_page.url,
		}
		
		# 设置缓存，有效期1小时
		cache.set(cache_key, json.dumps(cache_data), 3600)
		
		return True
	except Exception as e:
		logger.error(f"缓存博客内容失败: {e}")
		return False


def get_cached_blog(blog_id):
	"""
	从缓存中获取博客内容
	Args:
		blog_id: 博客ID

	Returns:
		dict: 缓存中的博客内容，如果不存在则返回None
	"""
	try:
		from django.core.cache import cache
		
		cache_key = f"blog_content_{blog_id}"
		cached_data = cache.get(cache_key)
		
		if cached_data:
			return json.loads(cached_data)
		return None
	except Exception as e:
		logger.error(f"获取缓存博客内容失败: {e}")
		return None