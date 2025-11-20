#!/user/bin/env python3
# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""AI 连接测试脚本"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from wagtail_ai.ai.openai import *

# 加载环境变量
load_dotenv()


def test_deepseek():
	"""测试 DeepSeek"""
	print("\n" + "=" * 60)
	print("🧪 测试 DeepSeek API")
	print("=" * 60)
	
	api_key = os.getenv('DEEPSEEK_API_KEY')
	if not api_key:
		print("❌ 未找到 DEEPSEEK_API_KEY")
		return False
	
	print(f"✓ API Key: {api_key[:10]}...{api_key[-5:]}")
	
	try:
		client = OpenAI(
			api_key=api_key,
			base_url=os.getenv('DEEPSEEK_BASE_URL')
		)
		
		response = client.chat.completions.create(
			model=os.getenv('DEEPSEEK_MODEL'),
			messages=[
				{"role": "user", "content": "你好，请用一句话介绍自己"}
			],
			max_tokens=100
		)
		
		print(f"✅ 连接成功！")
		print(f"📨 回复: {response.choices[0].message.content}")
		return True
	
	except Exception as e:
		print(f"❌ 连接失败: {e}")
		return False


if __name__ == "__main__":
	success = test_deepseek()
	sys.exit(0 if success else 1)