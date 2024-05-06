from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData
from .constants_oauth import ACCESS_TOKEN_EXPIRES


def generate_access_token(openid):
    """

    :param openid: 序列号openid
    :return: access_token(openid密文),byte类型
    """
    # 创建序列号对象
    # Serializer('密钥，越复杂越安全','过期时间')
    s = Serializer(settings.SECRET_KEY, ACCESS_TOKEN_EXPIRES)
    # 准备待序列号的字典数据
    data={'openid':openid}
    # 调用dumps方法进行序列化加密，返回bytes类型
    ciphertext=s.dumps(data)
    # 返回转成string，序列化的数据,
    return ciphertext.decode()

def check_access_token(access_token_openid):
    """
    解密opneid
    :param access_token:密文
    :return:明文
    """
    # 创建序列号对象,必须与加密一模一样
    # Serializer('密钥，越复杂越安全','过期时间')
    s = Serializer(settings.SECRET_KEY, ACCESS_TOKEN_EXPIRES)
    try:
        data=s.loads(access_token_openid)
    except BadData:
        return None
    else:
        openid = data.get('openid')
        return openid

