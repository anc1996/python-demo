#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wagtail-AI 交互式断点调试工具
使用 IPython 的 embed() 功能进行断点调试
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_ai_demo.settings.dev')
django.setup()

from wagtail_ai.agents.base import get_llm_service, get_provider
from wagtail_ai.ai.base import get_ai_backend
from django.conf import settings

print("""
╔══════════════════════════════════════════════════════════════╗
║         Wagtail-AI 交互式断点调试工具                         ║
╚══════════════════════════════════════════════════════════════╝

使用方法：
1. 在下面的交互式环境中，你可以逐步测试每个函数
2. 输入 'help()' 查看可用的测试函数
3. 输入 'exit' 退出

可用的变量和函数：
  - settings: Django 配置对象
  - get_provider: 获取 provider 配置
  - get_llm_service: 创建 LLM 服务
  - get_ai_backend: 创建 AI 后端
  - test_*: 各种测试函数

""")


# 定义辅助测试函数
def test_provider():
	"""测试 provider 配置"""
	print("\n🧪 测试 get_provider('default')...\n")
	try:
		result = get_provider('default')
		print("✅ 成功!")
		print("返回值:", result)
		return result
	except Exception as e:
		print(f"❌ 失败: {e}")
		import traceback
		traceback.print_exc()
		return None


def test_llm():
	"""测试 LLM 服务创建"""
	print("\n🧪 测试 get_llm_service('default')...\n")
	try:
		result = get_llm_service(alias='default')
		print("✅ 成功!")
		print("类型:", type(result))
		return result
	except Exception as e:
		print(f"❌ 失败: {e}")
		import traceback
		traceback.print_exc()
		return None


def test_backend():
	"""测试 AI 后端"""
	print("\n🧪 测试 get_ai_backend('default')...\n")
	try:
		result = get_ai_backend('default')
		print("✅ 成功!")
		print("类型:", type(result))
		print("配置:", result.config)
		return result
	except Exception as e:
		print(f"❌ 失败: {e}")
		import traceback
		traceback.print_exc()
		return None


def show_config():
	"""显示当前配置"""
	print("\n📋 WAGTAIL_AI 配置:\n")
	import json
	from django.conf import settings
	config = getattr(settings, 'WAGTAIL_AI', {})
	
	# 隐藏敏感信息
	safe_config = {}
	for key, value in config.items():
		if isinstance(value, dict):
			safe_value = {}
			for k, v in value.items():
				if isinstance(v, dict):
					safe_v = {}
					for kk, vv in v.items():
						if 'KEY' in kk.upper():
							safe_v[kk] = f"{str(vv)[:10]}...{str(vv)[-5:]}" if vv else None
						else:
							safe_v[kk] = vv
					safe_value[k] = safe_v
				else:
					safe_value[k] = v
			safe_config[key] = safe_value
		else:
			safe_config[key] = value
	
	print(json.dumps(safe_config, indent=2, ensure_ascii=False))


def trace_function(func):
	"""追踪函数调用"""
	import functools
	import inspect
	
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		print(f"\n📞 调用 {func.__name__}")
		print(f"   参数: args={args}, kwargs={kwargs}")
		
		try:
			result = func(*args, **kwargs)
			print(f"✅ 成功返回: {type(result)}")
			return result
		except Exception as e:
			print(f"❌ 异常: {type(e).__name__}: {e}")
			raise
	
	return wrapper


# 包装关键函数以追踪调用
original_get_provider = get_provider
traced_get_provider = trace_function(original_get_provider)


def help():
	"""显示帮助信息"""
	print("""
可用的测试函数：
  test_provider()  - 测试 provider 配置
  test_llm()       - 测试 LLM 服务
  test_backend()   - 测试 AI 后端
  show_config()    - 显示当前配置

直接调用函数：
  get_provider('default')
  get_llm_service(alias='default')
  get_ai_backend('default')

追踪函数调用：
  traced_get_provider('default')  - 显示详细调用信息

查看源代码：
  import inspect
  print(inspect.getsource(get_provider))

设置断点：
  在代码中任意位置添加：
  from IPython import embed; embed()
    """)


# 启动交互式 shell
try:
	from IPython import embed
	
	# 准备命名空间
	namespace = {
		'settings': settings,
		'get_provider': get_provider,
		'get_llm_service': get_llm_service,
		'get_ai_backend': get_ai_backend,
		'test_provider': test_provider,
		'test_llm': test_llm,
		'test_backend': test_backend,
		'show_config': show_config,
		'traced_get_provider': traced_get_provider,
		'help': help,
	}
	
	# 启动交互式环境
	embed(user_ns=namespace, colors='neutral')

except ImportError:
	print("\n⚠️  IPython 未安装，将使用标准 Python shell")
	print("安装命令: pip install ipython\n")
	
	import code
	
	code.interact(local={
		'settings': settings,
		'get_provider': get_provider,
		'get_llm_service': get_llm_service,
		'get_ai_backend': get_ai_backend,
		'test_provider': test_provider,
		'test_llm': test_llm,
		'test_backend': test_backend,
		'show_config': show_config,
		'help': help,
	})