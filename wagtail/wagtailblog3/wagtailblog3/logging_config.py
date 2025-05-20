import os
from django.conf import settings


# 确保日志目录存在
def ensure_log_dirs():
	log_dir = getattr(settings, 'LOG_DIR', os.path.join(settings.BASE_DIR, 'logs'))
	
	# 创建日志主目录
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	# 创建模块子目录
	for subdir in ['blog', 'comments', 'search', 'archive', 'system']:
		subdir_path = os.path.join(log_dir, subdir)
		if not os.path.exists(subdir_path):
			os.makedirs(subdir_path)
	
	return log_dir


# 基础日志配置（只关注warning及以上级别）
def get_logging_config(modules_filter=None):
	log_dir = ensure_log_dirs()
	
	config = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'verbose': {
				'format': '[{asctime}] {levelname} [{name}:{funcName}:{lineno}] {message}',
				'style': '{',
				'datefmt': '%Y-%m-%d %H:%M:%S',
			},
			'simple': {
				'format': '[{levelname}] {message}',
				'style': '{',
			},
			'colored': {
				'()': 'colorlog.ColoredFormatter',
				'format': '%(log_color)s[%(levelname)s] %(name)s: %(message)s',
				'log_colors': {
					'WARNING': 'yellow',
					'ERROR': 'red',
					'CRITICAL': 'bold_red',
				},
			},
		},
		'handlers': {
			'console': {
				'level': 'WARNING',
				'class': 'logging.StreamHandler',
				'formatter': 'colored',
			},
			'blog_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'blog/blog_error.log'),
				'maxBytes': 10485760,  # 10MB
				'backupCount': 5,
				'formatter': 'verbose',
			},
			'comments_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'comments/comments_error.log'),
				'maxBytes': 10485760,
				'backupCount': 5,
				'formatter': 'verbose',
			},
			'search_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'search/search_error.log'),
				'maxBytes': 10485760,
				'backupCount': 5,
				'formatter': 'verbose',
			},
			'archive_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'archive/archive_error.log'),
				'maxBytes': 10485760,
				'backupCount': 5,
				'formatter': 'verbose',
			},
			'system_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'system/error.log'),
				'maxBytes': 10485760,
				'backupCount': 5,
				'formatter': 'verbose',
			},
			'wagtail_error_file': {
				'level': 'WARNING',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': os.path.join(log_dir, 'system/wagtail_error.log'),
				'maxBytes': 10485760,
				'backupCount': 5,
				'formatter': 'verbose',
			},
		},
		'loggers': {
			'django': {
				'handlers': ['console', 'system_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'wagtail': {
				'handlers': ['console', 'wagtail_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'blog': {
				'handlers': ['console', 'blog_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'search': {
				'handlers': ['console', 'search_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'comments': {
				'handlers': ['console', 'comments_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'archive': {
				'handlers': ['console', 'archive_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
			'wagtailblog3': {
				'handlers': ['console', 'system_error_file'],
				'level': 'WARNING',
				'propagate': False,
			},
		}
	}
	
	# 如果提供了模块过滤器
	if modules_filter:
		config['filters'] = {
			'module_filter': {
				'()': 'wagtailblog3.logging_filters.ModuleFilter',
				'modules': modules_filter,
			}
		}
		
		# 添加过滤器到控制台处理器
		config['handlers']['console']['filters'] = ['module_filter']
	
	return config