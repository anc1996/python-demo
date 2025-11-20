#!/user/bin/env python3
# -*- coding: utf-8 -*-
# blog/ai_backends.py

import os
from dataclasses import dataclass
from typing import Any, Self

import requests
from wagtail_ai.ai.base import BaseAIBackendConfigSettings
from wagtail_ai.ai.openai import OpenAIBackend, OpenAIBackendConfig, OpenAIResponse


# 1. 重命名配置类，使其更通用
class OpenAICompatibleBackendConfigSettingsDict(BaseAIBackendConfigSettings):
	BASE_URL: str


@dataclass(kw_only=True)
class OpenAICompatibleBackendConfig(OpenAIBackendConfig):
	base_url: str
	
	@classmethod
	def from_settings(
			cls, config: OpenAICompatibleBackendConfigSettingsDict, **kwargs: Any
	) -> Self:
		if "BASE_URL" not in config:
			raise RuntimeError("WAGTAIL_AI CONFIG 缺少 'BASE_URL'")
		
		kwargs.setdefault("base_url", config["BASE_URL"])
		
		return super().from_settings(config, **kwargs)  # type: ignore


# 2. 重命名后端类，使其更通用
class OpenAICompatibleBackend(OpenAIBackend):
	# 告诉它使用我们新的配置类
	config_cls = OpenAICompatibleBackendConfig
	
	# 3. 覆盖 chat_completions 方法
	def chat_completions(self, messages: list[dict[str, Any]]) -> OpenAIResponse:
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {self.get_openai_api_key()}",
		}
		payload = {
			"model": self.config.model_id,
			"messages": messages,
			"max_tokens": self.config.token_limit,
		}
		
		# ⬇️ 关键：使用配置中的 base_url，而不是硬编码的 OpenAI URL
		url = f"{self.config.base_url}/chat/completions"
		
		response = requests.post(
			url,
			headers=headers,
			json=payload,
			timeout=self.config.timeout_seconds,
		)
		
		response.raise_for_status()
		return OpenAIResponse(response)