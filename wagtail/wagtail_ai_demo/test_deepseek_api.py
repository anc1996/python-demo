#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DeepSeek API 连接和超时问题
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import time

# 加载环境变量
load_dotenv()


def test_deepseek_direct():
	"""直接测试 DeepSeek API"""
	print("\n" + "=" * 80)
	print("  直接测试 DeepSeek API")
	print("=" * 80)
	
	api_key = os.getenv('DEEPSEEK_API_KEY')
	base_url = os.getenv('DEEPSEEK_BASE_URL')
	model = os.getenv('DEEPSEEK_MODEL')
	
	print(f"\n配置:")
	print(f"  API Key: {api_key[:10]}...{api_key[-5:]}")
	print(f"  Base URL: {base_url}")
	print(f"  Model: {model}")
	
	try:
		client = OpenAI(
			api_key=api_key,
			base_url=base_url,
			timeout=60.0,  # 设置 60 秒超时
		)
		
		print("\n发送请求...")
		start_time = time.time()
		
		response = client.chat.completions.create(
			model=model,
			messages=[
				{"role": "user", "content": "你好，请用一句话介绍自己"}
			],
			max_tokens=100
		)
		
		end_time = time.time()
		
		print(f"✅ 成功！耗时 {end_time - start_time:.2f} 秒")
		print(f"📨 回复: {response.choices[0].message.content}")
		return True
	
	except Exception as e:
		print(f"❌ 失败: {type(e).__name__}: {e}")
		import traceback
		traceback.print_exc()
		return False


def test_network():
	"""测试网络连接"""
	print("\n" + "=" * 80)
	print("  测试网络连接")
	print("=" * 80)
	
	import socket
	
	base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
	# 提取域名
	domain = base_url.replace('https://', '').replace('http://', '').split('/')[0]
	
	print(f"\n测试连接到 {domain}...")
	
	try:
		# DNS 解析
		ip = socket.gethostbyname(domain)
		print(f"✅ DNS 解析成功: {domain} -> {ip}")
		
		# 测试端口连接
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(10)
		result = sock.connect_ex((domain, 443))
		sock.close()
		
		if result == 0:
			print(f"✅ 端口 443 可以连接")
			return True
		else:
			print(f"❌ 端口 443 无法连接")
			return False
	
	except Exception as e:
		print(f"❌ 网络测试失败: {e}")
		return False


def check_proxy():
	"""检查代理设置"""
	print("\n" + "=" * 80)
	print("  检查代理设置")
	print("=" * 80)
	
	proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']
	
	found_proxy = False
	for var in proxy_vars:
		value = os.getenv(var)
		if value:
			print(f"  ⚠️  发现代理: {var}={value}")
			found_proxy = True
	
	if not found_proxy:
		print("  ✅ 未设置代理")
	
	return not found_proxy


def test_with_longer_timeout():
	"""使用更长的超时时间测试"""
	print("\n" + "=" * 80)
	print("  使用更长超时时间测试 (120 秒)")
	print("=" * 80)
	
	api_key = os.getenv('DEEPSEEK_API_KEY')
	base_url = os.getenv('DEEPSEEK_BASE_URL')
	model = os.getenv('DEEPSEEK_MODEL')
	
	try:
		client = OpenAI(
			api_key=api_key,
			base_url=base_url,
			timeout=120.0,  # 增加到 120 秒
		)
		
		print("\n发送简单请求...")
		start_time = time.time()
		
		response = client.chat.completions.create(
			model=model,
			messages=[
				{"role": "user", "content": "hi"}
			],
			max_tokens=10
		)
		
		end_time = time.time()
		
		print(f"✅ 成功！耗时 {end_time - start_time:.2f} 秒")
		print(f"📨 回复: {response.choices[0].message.content}")
		return True
	
	except Exception as e:
		print(f"❌ 仍然失败: {type(e).__name__}: {e}")
		return False


def suggest_fixes():
	"""提供修复建议"""
	print("\n" + "=" * 80)
	print("  修复建议")
	print("=" * 80)
	
	print("""
根据测试结果，可能的解决方案：

1. 🔧 在 PROVIDERS 配置中增加超时时间:

   WAGTAIL_AI = {
       "PROVIDERS": {
           "default": {
               "provider": "deepseek",
               "model": os.getenv("DEEPSEEK_MODEL"),
               "api_key": os.getenv("DEEPSEEK_API_KEY"),
               "api_base": os.getenv("DEEPSEEK_BASE_URL"),
               "timeout": 120,  # ← 添加这一行，单位是秒
           }
       },
       # ...
   }

2. 🌐 检查网络连接:
   - 确保服务器可以访问 api.deepseek.com
   - 检查防火墙设置
   - 如果在国内，可能需要配置代理

3. 🔑 验证 API Key:
   - 确保 API Key 有效且未过期
   - 在 DeepSeek 控制台检查 API Key 的使用额度

4. 🚀 使用更快的模型:
   - 如果可能，尝试使用 deepseek-chat (更快)
   - 避免在高峰时段使用

5. 🐛 临时解决方案:
   - 先使用 RichTextBlock 的 AI 功能（通过 BACKENDS）
   - 等网络条件改善后再使用 AITitleFieldPanel
    """)


def main():
	"""主函数"""
	print("\n" + "🔍" * 40)
	print("  DeepSeek API 连接测试")
	print("🔍" * 40)
	
	# 1. 检查代理
	no_proxy = check_proxy()
	
	# 2. 测试网络
	network_ok = test_network()
	
	# 3. 直接测试 API
	api_ok = False
	if network_ok:
		api_ok = test_deepseek_direct()
	
	# 4. 如果失败，尝试更长超时
	if not api_ok and network_ok:
		test_with_longer_timeout()
	
	# 5. 提供修复建议
	suggest_fixes()
	
	print("\n" + "=" * 80)
	print("  总结")
	print("=" * 80)
	print(f"""
测试结果:
  - 网络连接: {'✅' if network_ok else '❌'}
  - 无代理干扰: {'✅' if no_proxy else '⚠️'}
  - API 调用: {'✅' if api_ok else '❌'}

建议: {'配置正确，请增加超时时间' if network_ok and not api_ok else '请检查网络连接'}
    """)


if __name__ == "__main__":
	main()