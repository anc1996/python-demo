#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import requests
import logging

BASE_URL = "http://127.0.0.1:5001"

# Simulated client
@pytest.fixture
def client():
    return requests.Session()

def login_with_cookies(client):
    response = client.post(f"{BASE_URL}/locations/login_with_cookies")
    assert response.status_code == 200
    assert 'access_token_cookie' in response.cookies
    # 从响应 Cookie 中提取 CSRF 令牌
    csrf_token = response.cookies.get('csrf_access_token')
    client.headers.update({'X-CSRF-TOKEN': csrf_token})
    return response.cookies

def logout_with_cookies(client):
    response = client.post(f"{BASE_URL}/locations/logout_with_cookies")
    assert response.status_code == 200
    assert 'access_token_cookie' not in response.cookies

def make_request_with_jwt_cookies(client, caplog):
    response = client.post(f"{BASE_URL}/locations/only_cookies", cookies=client.cookies)
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response content: {response.content}")
    assert response.status_code == 200
    result = response.json()
    return result

def test_jwt_workflow_with_cookies(client, caplog):
    # 登录并获取 JWT Cookie
    cookies = login_with_cookies(client)
    assert cookies is not None

    # 使用 JWT Cookie 发出请求
    result = make_request_with_jwt_cookies(client, caplog)
    assert result['foo'] == 'qux'

    # 注销并删除 JWT Cookie
    logout_with_cookies(client)
    assert 'access_token_cookie' not in client.cookies
