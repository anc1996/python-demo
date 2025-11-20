#!/user/bin/env python3
# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wagtail-AI 正确的调试工具
基于实际存在的 API
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_ai_demo.settings.dev')
django.setup()

from django.conf import settings


def print_section(title):
	print("\n" + "=" * 80)
	print(f"  {title}")
	print("=" * 80)


def check_imports():
	"""检查 wagtail-ai 的可用导入"""
	print_section("1. 检查 Wagtail-AI 可用的导入")
	
	imports_to_test = [
		('wagtail_ai', None),
		('wagtail_ai.agents', None),
		('wagtail_ai.agents.base', ['get_provider', 'get_llm_service']),
		('wagtail_ai.ai', None),
		('wagtail_ai.ai.openai', ['OpenAIBackend']),
		('wagtail_ai.panels', ['AITitleFieldPanel', 'AIDescriptionFieldPanel']),
	]
	
	print("\n可用的导入:")
	for module_name, attrs in imports_to_test:
		try:
			module = __import__(module_name, fromlist=attrs or [''])
			print(f"  ✅ {module_name}")
			
			if attrs:
				for attr in attrs:
					if hasattr(module, attr):
						print(f"     ✓ {attr}")
					else:
						print(f"     ✗ {attr} (不存在)")
			
			# 显示模块的所有公开属性
			if module_name in ['wagtail_ai.agents.base', 'wagtail_ai.ai']:
				public_attrs = [name for name in dir(module) if not name.startswith('_')]
				if public_attrs:
					print(f"     可用属性: {', '.join(public_attrs[:10])}")
		
		except ImportError as e:
			print(f"  ❌ {module_name}: {e}")


def check_wagtail_ai_structure():
	"""检查 wagtail_ai 的实际结构"""
	print_section("2. Wagtail-AI 包结构")
	
	try:
		import wagtail_ai
		import inspect
		
		print(f"\n📦 wagtail_ai 安装位置:")
		print(f"   {wagtail_ai.__file__}")
		
		print(f"\n📋 wagtail_ai 子模块:")
		for name in dir(wagtail_ai):
			if not name.startswith('_'):
				attr = getattr(wagtail_ai, name)
				if inspect.ismodule(attr):
					print(f"   - {name}")
	
	except Exception as e:
		print(f"❌ 无法检查结构: {e}")


def test_providers_config():
	"""测试 PROVIDERS 配置"""
	print_section("3. 测试 PROVIDERS 配置")
	
	try:
		from wagtail_ai.agents.base import get_provider
		
		wagtail_ai_config = getattr(settings, 'WAGTAIL_AI', {})
		
		if 'PROVIDERS' not in wagtail_ai_config:
			print("\n⚠️  未找到 PROVIDERS 配置")
			print("   这就是 AITitleFieldPanel 失败的原因！")
			return False
		
		print("\n✓ 找到 PROVIDERS 配置")
		
		# 测试 get_provider
		try:
			provider_config = get_provider('default')
			print("\n✅ get_provider('default') 成功:")
			for key, value in provider_config.items():
				if 'key' in key.lower():
					print(f"   - {key}: {str(value)[:10]}...{str(value)[-5:]}")
				else:
					print(f"   - {key}: {value}")
			return True
		except Exception as e:
			print(f"\n❌ get_provider('default') 失败:")
			print(f"   错误: {e}")
			import traceback
			traceback.print_exc()
			return False
	
	except ImportError as e:
		print(f"\n❌ 无法导入 get_provider: {e}")
		return False


def test_backends_config():
	"""测试 BACKENDS 配置（不使用 get_ai_backend）"""
	print_section("4. 测试 BACKENDS 配置")
	
	wagtail_ai_config = getattr(settings, 'WAGTAIL_AI', {})
	
	if 'BACKENDS' not in wagtail_ai_config:
		print("\n⚠️  未找到 BACKENDS 配置")
		return False
	
	print("\n✓ 找到 BACKENDS 配置")
	
	backends = wagtail_ai_config['BACKENDS']
	for name, config in backends.items():
		print(f"\n  Backend: {name}")
		print(f"    CLASS: {config.get('CLASS')}")
		
		# 尝试实例化后端类
		try:
			class_path = config.get('CLASS')
			if not class_path:
				print("    ❌ 未指定 CLASS")
				continue
			
			module_name, class_name = class_path.rsplit('.', 1)
			module = __import__(module_name, fromlist=[class_name])
			backend_class = getattr(module, class_name)
			
			print(f"    ✅ 类可以导入: {class_name}")
			
			# 尝试实例化
			try:
				backend_instance = backend_class(config.get('CONFIG', {}))
				print(f"    ✅ 可以实例化")
				print(f"    类型: {type(backend_instance)}")
			except Exception as e:
				print(f"    ⚠️  实例化时出错: {e}")
		
		except Exception as e:
			print(f"    ❌ 无法导入类: {e}")
	
	return True


def test_llm_service():
	"""测试 LLM Service 创建"""
	print_section("5. 测试 LLM Service")
	
	try:
		from wagtail_ai.agents.base import get_llm_service
		
		print("\n测试 get_llm_service(alias='default')...")
		
		try:
			service = get_llm_service(alias='default')
			print(f"✅ 成功创建 LLM Service")
			print(f"   类型: {type(service)}")
			return True
		except Exception as e:
			print(f"❌ 创建失败:")
			print(f"   错误: {e}")
			import traceback
			traceback.print_exc()
			return False
	
	except ImportError as e:
		print(f"❌ 无法导入 get_llm_service: {e}")
		return False


def check_environment():
	"""检查环境变量"""
	print_section("6. 环境变量检查")
	
	required_vars = {
		'DEEPSEEK_API_KEY': '必需 (用于 PROVIDERS)',
		'DEEPSEEK_BASE_URL': '必需 (用于 PROVIDERS)',
		'DEEPSEEK_MODEL': '必需 (用于 PROVIDERS)',
	}
	
	print("\n环境变量状态:")
	all_present = True
	for var, desc in required_vars.items():
		value = os.getenv(var)
		if value:
			if 'KEY' in var:
				print(f"  ✓ {var}: {value[:10]}...{value[-5:]} ({desc})")
			else:
				print(f"  ✓ {var}: {value} ({desc})")
		else:
			print(f"  ✗ {var}: 未设置 ({desc})")
			all_present = False
	
	return all_present


def suggest_fix():
	"""提供修复建议"""
	print_section("修复建议")
	
	print("""
根据检查结果，修复方法：

1. ✅ 在 base.py 中添加 PROVIDERS 配置（如果缺失）:

   WAGTAIL_AI = {
       "PROVIDERS": {
           "default": {
               "provider": "deepseek",  # ← 关键！
               "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
               "api_key": os.getenv("DEEPSEEK_API_KEY"),
               "api_base": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
           }
       },
       "BACKENDS": {
           # ... 保持现有配置
       },
       "TEXT_COMPLETION_BACKEND": "default",
   }

2. ✅ 确保 .env 文件包含必需的环境变量

3. ✅ 重启 Django 服务器

4. ✅ 测试 AITitleFieldPanel 功能
    """)


def main():
	"""主函数"""
	print("\n" + "🔍" * 40)
	print("  Wagtail-AI 正确的调试工具")
	print("  (基于实际存在的 API)")
	print("🔍" * 40)
	
	# 1. 检查可用导入
	check_imports()
	
	# 2. 检查包结构
	check_wagtail_ai_structure()
	
	# 3. 检查环境变量
	env_ok = check_environment()
	
	# 4. 测试 PROVIDERS
	providers_ok = test_providers_config()
	
	# 5. 测试 BACKENDS
	backends_ok = test_backends_config()
	
	# 6. 测试 LLM Service
	if providers_ok:
		test_llm_service()
	
	# 7. 提供修复建议
	suggest_fix()
	
	print_section("总结")
	print(f"""
检查结果:
  - 环境变量: {'✅' if env_ok else '❌'}
  - PROVIDERS 配置: {'✅' if providers_ok else '❌'}
  - BACKENDS 配置: {'✅' if backends_ok else '❌'}

关键发现:
  - AITitleFieldPanel 需要 PROVIDERS 配置
  - RichTextBlock(features=['ai']) 需要 BACKENDS 配置
  - 这是两个独立的系统！
    """)


if __name__ == "__main__":
	main()