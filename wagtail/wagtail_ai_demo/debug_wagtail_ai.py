#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wagtail-AI 调试工具
用于追踪 AITitleFieldPanel 和 AIDescriptionFieldPanel 的调用流程
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


def print_section(title):
	print("\n" + "=" * 80)
	print(f"  {title}")
	print("=" * 80)


def check_settings():
	"""检查 WAGTAIL_AI 配置"""
	print_section("1. 检查 WAGTAIL_AI 配置")
	
	wagtail_ai_config = getattr(settings, 'WAGTAIL_AI', {})
	
	print("\n📋 WAGTAIL_AI 配置结构:")
	print(f"  - 是否有 PROVIDERS: {bool(wagtail_ai_config.get('PROVIDERS'))}")
	print(f"  - 是否有 BACKENDS: {bool(wagtail_ai_config.get('BACKENDS'))}")
	print(f"  - TEXT_COMPLETION_BACKEND: {wagtail_ai_config.get('TEXT_COMPLETION_BACKEND')}")
	
	if 'PROVIDERS' in wagtail_ai_config:
		print("\n  PROVIDERS 内容:")
		for key, value in wagtail_ai_config['PROVIDERS'].items():
			print(f"    - {key}: {value}")
	else:
		print("\n  ⚠️  未找到 PROVIDERS 配置")
	
	if 'BACKENDS' in wagtail_ai_config:
		print("\n  BACKENDS 内容:")
		for key, value in wagtail_ai_config['BACKENDS'].items():
			print(f"    - {key}:")
			print(f"      CLASS: {value.get('CLASS')}")
			print(f"      CONFIG keys: {list(value.get('CONFIG', {}).keys())}")
	
	return wagtail_ai_config


def test_get_provider():
	"""测试 get_provider 函数"""
	print_section("2. 测试 get_provider('default')")
	
	try:
		provider_config = get_provider('default')
		print("\n✅ get_provider('default') 成功返回:")
		for key, value in provider_config.items():
			if 'key' in key.lower():
				# 隐藏敏感信息
				print(f"  - {key}: {str(value)[:10]}...{str(value)[-5:]}")
			else:
				print(f"  - {key}: {value}")
	except Exception as e:
		print(f"\n❌ get_provider('default') 失败:")
		print(f"  错误类型: {type(e).__name__}")
		print(f"  错误信息: {e}")
		
		# 打印调用栈
		import traceback
		print("\n📍 调用栈:")
		traceback.print_exc()


def test_get_llm_service():
	"""测试 get_llm_service 函数"""
	print_section("3. 测试 get_llm_service()")
	
	try:
		llm_service = get_llm_service(alias='default')
		print("\n✅ get_llm_service('default') 成功创建")
		print(f"  类型: {type(llm_service)}")
		print(f"  Provider: {getattr(llm_service, 'provider', 'N/A')}")
	except Exception as e:
		print(f"\n❌ get_llm_service('default') 失败:")
		print(f"  错误类型: {type(e).__name__}")
		print(f"  错误信息: {e}")
		
		import traceback
		print("\n📍 调用栈:")
		traceback.print_exc()


def test_get_ai_backend():
	"""测试 get_ai_backend 函数"""
	print_section("4. 测试 get_ai_backend()")
	
	try:
		backend = get_ai_backend('default')
		print("\n✅ get_ai_backend('default') 成功创建")
		print(f"  类型: {type(backend)}")
		print(f"  配置: {backend.config}")
	except Exception as e:
		print(f"\n❌ get_ai_backend('default') 失败:")
		print(f"  错误类型: {type(e).__name__}")
		print(f"  错误信息: {e}")
		
		import traceback
		print("\n📍 调用栈:")
		traceback.print_exc()


def check_environment_variables():
	"""检查环境变量"""
	print_section("5. 检查环境变量")
	
	env_vars = [
		'DEEPSEEK_API_KEY',
		'DEEPSEEK_BASE_URL',
		'DEEPSEEK_MODEL',
		'OPENAI_API_KEY',  # 检查是否意外设置了这个
		'AI_MAX_TOKENS',
	]
	
	print("\n🔍 环境变量检查:")
	for var in env_vars:
		value = os.getenv(var)
		if value:
			if 'KEY' in var:
				print(f"  ✓ {var}: {value[:10]}...{value[-5:]}")
			else:
				print(f"  ✓ {var}: {value}")
		else:
			print(f"  ✗ {var}: 未设置")


def analyze_source_code():
	"""分析 wagtail-ai 源代码位置"""
	print_section("6. Wagtail-AI 源代码位置")
	
	try:
		import wagtail_ai
		import wagtail_ai.agents.base
		import wagtail_ai.panels
		
		print("\n📦 已安装的包路径:")
		print(f"  wagtail_ai: {wagtail_ai.__file__}")
		print(f"  wagtail_ai.agents.base: {wagtail_ai.agents.base.__file__}")
		print(f"  wagtail_ai.panels: {wagtail_ai.panels.__file__}")
		
		# 检查关键函数的源代码位置
		import inspect
		
		print("\n🔍 关键函数源代码位置:")
		print(f"  get_provider: {inspect.getfile(get_provider)}")
		print(f"  get_llm_service: {inspect.getfile(get_llm_service)}")
		print(f"  get_ai_backend: {inspect.getfile(get_ai_backend)}")
	
	except Exception as e:
		print(f"\n❌ 无法获取源代码位置: {e}")


def main():
	"""主函数"""
	print("\n" + "🔍" * 40)
	print("  Wagtail-AI 调试工具")
	print("🔍" * 40)
	
	# 1. 检查配置
	check_settings()
	
	# 2. 检查环境变量
	check_environment_variables()
	
	# 3. 测试 get_provider
	test_get_provider()
	
	# 4. 测试 get_llm_service
	test_get_llm_service()
	
	# 5. 测试 get_ai_backend
	test_get_ai_backend()
	
	# 6. 分析源代码位置
	analyze_source_code()
	
	print_section("总结")
	print("""
下一步调试建议：
1. 如果 get_provider 失败 → 需要添加 PROVIDERS 配置
2. 如果 get_llm_service 失败 → 检查 any_llm 库的要求
3. 如果 get_ai_backend 成功 → RichTextBlock 应该能用
4. 如果需要断点调试 → 使用下面的 IPython 方法
    """)


if __name__ == "__main__":
	main()