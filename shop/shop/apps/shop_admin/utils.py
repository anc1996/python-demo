

# 重写以返回自定义响应
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
    }