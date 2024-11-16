import pytest
import requests

BASE_URL = "http://127.0.0.1:5001"

# 模拟客户端，pytest.fixture装饰器会将client作为参数传递给测试函数
@pytest.fixture
def client():
    return requests.Session()


# 获取 JWT Token 的登录功能
def login(client):
    # 发出请求以获取JWT令牌
    response = client.post(f"{BASE_URL}/locations/login_without_cookies")
    # 解析响应以获取JWT令牌
    result = response.json()
    print(f"Login Response: {result}")
    # 将JWT令牌添加到请求头
    client.headers.update({'Authorization': f"Bearer {result['access_token']}"})
    return result['access_token']

# 注销功能，用于删除 JWT 令牌
def logout(client):
    # 发出请求以注销
    client.headers.pop('Authorization', None)

# 使用 JWT 函数发出请求
def make_request_with_jwt(client):
    # 发出受保护的请求
    response = client.post(f"{BASE_URL}/locations/protected")
    result = response.json()
    print(f"Protected Response: {result}")  # Debugging print statement
    return result

# 示例测试用例
def test_jwt_workflow(client):
    # Login and obtain JWT token
    token = login(client)
    assert token is not None

    # 使用 JWT 令牌发出请求
    result = make_request_with_jwt(client)
    assert result['foo'] == 'bar'

    #注销并删除 JWT 令牌
    logout(client)
    assert 'Authorization' not in client.headers
    
