#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wagtail-AI 源代码追踪工具
帮助理解 AITitleFieldPanel 和 RichTextBlock 的不同调用路径
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_ai_demo.settings.dev')
django.setup()

import inspect
from pathlib import Path


def print_header(title):
	print("\n" + "=" * 80)
	print(f"  {title}")
	print("=" * 80)


def show_function_source(func, name=None):
	"""显示函数源代码"""
	if name is None:
		name = func.__name__
	
	print(f"\n📄 {name} 源代码:")
	print(f"   位置: {inspect.getfile(func)}:{inspect.getsourcelines(func)[1]}")
	print("-" * 80)
	try:
		source = inspect.getsource(func)
		# 只显示前50行，避免太长
		lines = source.split('\n')[:50]
		for i, line in enumerate(lines, 1):
			print(f"{i:3d} | {line}")
		if len(source.split('\n')) > 50:
			print(f"... (还有 {len(source.split('\n')) - 50} 行)")
	except Exception as e:
		print(f"   无法获取源代码: {e}")


def trace_call_chain():
	"""追踪调用链"""
	print_header("调用链追踪")
	
	print("""
┌─────────────────────────────────────────────────────────────┐
│  AITitleFieldPanel / AIDescriptionFieldPanel 调用链          │
└─────────────────────────────────────────────────────────────┘

1. 用户点击 AI 按钮 (前端)
   ↓
2. 发送 AJAX 请求到 /admin/ai/basic_prompt/
   ↓
3. BasicPromptView.post()
   文件: wagtail_ai/views/basic_prompt.py
   ↓
4. BasicPromptAgent.execute()
   文件: wagtail_ai/agents/basic_prompt.py
   ↓
5. get_llm_service(alias='default')  ← 这里需要 PROVIDERS
   文件: wagtail_ai/agents/base.py
   ↓
6. get_provider('default')
   文件: wagtail_ai/agents/base.py
   读取: settings.WAGTAIL_AI['PROVIDERS']['default']
   ↓
7. LLMService.create(**provider_config)
   文件: django_ai_core/llm/base.py
   ↓
8. AnyLLM.create(provider='deepseek', ...)
   文件: any_llm/any_llm.py
   ↓
9. 创建 DeepSeekProvider 实例
   需要: api_key, api_base, model


┌─────────────────────────────────────────────────────────────┐
│  RichTextBlock(features=['ai']) 调用链                       │
└─────────────────────────────────────────────────────────────┘

1. 用户在 Draftail 编辑器中选中文字，点击 AI 按钮
   ↓
2. 发送请求到后端 AI 接口
   ↓
3. get_ai_backend('default')  ← 这里需要 BACKENDS
   文件: wagtail_ai/ai/base.py
   读取: settings.WAGTAIL_AI['BACKENDS']['default']
   ↓
4. 实例化 OpenAICompatibleBackend
   文件: blog/ai_backends.py (你的自定义后端)
   ↓
5. OpenAICompatibleBackend.chat_completions()
   直接调用 DeepSeek API
    """)


def show_key_files():
	"""显示关键文件"""
	print_header("关键源代码文件")
	
	try:
		import wagtail_ai.agents.base
		import wagtail_ai.agents.basic_prompt
		import wagtail_ai.ai.base
		import wagtail_ai.panels
		
		files = {
			'get_provider & get_llm_service': wagtail_ai.agents.base.__file__,
			'BasicPromptAgent': wagtail_ai.agents.basic_prompt.__file__,
			'get_ai_backend': wagtail_ai.ai.base.__file__,
			'AITitleFieldPanel': wagtail_ai.panels.__file__,
		}
		
		print("\n📁 文件位置:")
		for desc, filepath in files.items():
			print(f"\n  {desc}:")
			print(f"    {filepath}")
			
			# 显示文件开头部分
			try:
				with open(filepath, 'r', encoding='utf-8') as f:
					lines = f.readlines()[:30]
					print("    " + "-" * 60)
					for i, line in enumerate(lines, 1):
						print(f"    {i:3d} | {line.rstrip()}")
					print("    " + "-" * 60)
			except Exception as e:
				print(f"    无法读取文件: {e}")
	
	except Exception as e:
		print(f"\n❌ 无法获取文件信息: {e}")


def show_critical_code():
	"""显示关键代码段"""
	print_header("关键代码分析")
	
	print("\n🔍 1. get_provider() 函数")
	print("   这个函数负责从 WAGTAIL_AI['PROVIDERS'] 读取配置")
	
	try:
		from wagtail_ai.agents.base import get_provider
		show_function_source(get_provider)
	except Exception as e:
		print(f"   无法显示: {e}")
	
	print("\n🔍 2. get_llm_service() 函数")
	print("   这个函数使用 get_provider() 的结果创建 LLM 服务")
	
	try:
		from wagtail_ai.agents.base import get_llm_service
		show_function_source(get_llm_service)
	except Exception as e:
		print(f"   无法显示: {e}")
	
	print("\n🔍 3. get_ai_backend() 函数")
	print("   这个函数从 WAGTAIL_AI['BACKENDS'] 读取配置")
	
	try:
		from wagtail_ai.ai.base import get_ai_backend
		show_function_source(get_ai_backend)
	except Exception as e:
		print(f"   无法显示: {e}")


def analyze_error():
	"""分析错误原因"""
	print_header("错误原因分析")
	
	print("""
❌ 错误信息:
   any_llm.exceptions.MissingApiKeyError:
   No openai API key provided. Please provide it in the config
   or set the OPENAI_API_KEY environment variable.

🔍 错误原因:
   1. AITitleFieldPanel 调用 get_llm_service()
   2. get_llm_service() 调用 get_provider('default')
   3. get_provider() 在 WAGTAIL_AI['PROVIDERS'] 中找不到 'default'
   4. 系统 fallback 到 'openai' provider (硬编码的默认值)
   5. any_llm 尝试创建 OpenAI provider
   6. 但是没有 OPENAI_API_KEY 环境变量 → 报错

📊 调用栈验证:
   File "wagtail_ai/agents/base.py", line 81, in get_llm_service
     return LLMService.create(**get_provider(alias))
                              ^^^^^^^^^^^^^^^^^^^
   这里调用了 get_provider()

   File "any_llm/any_llm.py", line 99, in _verify_and_set_api_key
     raise MissingApiKeyError(self.PROVIDER_NAME, self.ENV_API_KEY_NAME)
   any_llm 期望的是 'openai' provider，但没有对应的 API key

✅ 解决方案:
   在 WAGTAIL_AI 配置中添加 PROVIDERS 部分:

   WAGTAIL_AI = {
       "PROVIDERS": {
           "default": {
               "provider": "deepseek",  # ← 关键：指定 provider
               "model": "deepseek-chat",
               "api_key": os.getenv("DEEPSEEK_API_KEY"),
               "api_base": os.getenv("DEEPSEEK_BASE_URL"),
           }
       },
       "BACKENDS": {
           # ... 保持不变
       },
   }

💡 为什么 RichTextBlock 能用？
   因为 RichTextBlock(features=['ai']) 使用的是:
   - get_ai_backend() → 读取 BACKENDS 配置
   - 你已经配置了 BACKENDS，所以能正常工作

   而 AITitleFieldPanel 使用的是:
   - get_llm_service() → 读取 PROVIDERS 配置
   - 你没有配置 PROVIDERS，所以失败
    """)


def main():
	"""主函数"""
	print("\n" + "🔍" * 40)
	print("  Wagtail-AI 源代码追踪工具")
	print("🔍" * 40)
	
	# 1. 调用链追踪
	trace_call_chain()
	
	# 2. 显示关键文件
	show_key_files()
	
	# 3. 显示关键代码
	show_critical_code()
	
	# 4. 错误分析
	analyze_error()
	
	print_header("总结")
	print("""
📝 问题定位完成！

核心问题：
  配置中缺少 PROVIDERS 部分，导致 AITitleFieldPanel 失败

解决步骤：
  1. 运行调试脚本确认问题：
     python debug_wagtail_ai.py

  2. 应用修复配置：
     复制 fixed_settings.py 中的配置到 base.py

  3. 重启服务器测试：
     python manage.py runserver 0.0.0.0:8000

  4. 如需深入调试，使用交互式工具：
     python debug_interactive.py

     然后在交互式环境中运行：
     >>> test_provider()  # 测试 PROVIDERS 配置
     >>> test_backend()   # 测试 BACKENDS 配置
    """)


if __name__ == "__main__":
	main()