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

def login_without_cookies(client):
    response = client.post(f"{BASE_URL}/locations/login_without_cookies")
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result
    return result['access_token']

def make_request_with_jwt_query_string(client, jwt, caplog):
    response = client.post(f"{BASE_URL}/locations/only_query_string?jwt={jwt}")
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response content: {response.content}")
    assert response.status_code == 200
    result = response.json()
    return result


def test_jwt_workflow_with_query_string(client, caplog):
    # 登录并获取 JWT
    jwt = login_without_cookies(client)
    assert jwt is not None

    # 使用 JWT 发出请求
    result = make_request_with_jwt_query_string(client, jwt, caplog)
    assert result['foo'] == 'quux'



