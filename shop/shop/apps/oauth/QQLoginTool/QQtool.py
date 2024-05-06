from urllib.parse import urlencode, parse_qs
import json
import requests


class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        # 申请QQ登录成功后，分配给应用的appid。
        self.client_id = client_id
        # **appkey**：appid对应的密钥，访问用户资源时用来验证应用的合法性
        self.client_secret = client_secret
        # 成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        self.redirect_uri = redirect_uri
        # 用于保存登录成功后的跳转页面路径。client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。
        self.state = state

    def get_qq_url(self):
        # QQ登录url参数组建，第一步：获取Authorization Code
        data_dict = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }

        # 构建url
        qq_url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(data_dict)

        return qq_url

    # 获取access_token值
    def get_access_token(self, code):
        # 构建参数数据
        data_dict = {
            # 授权类型，在本步骤中，此值为“authorization_code”。
            'grant_type': 'authorization_code',
            # 申请QQ登录成功后，分配给网站的appid。
            'client_id': self.client_id,
            #  申请QQ登录成功后，分配给网站的appkey。
            'client_secret': self.client_secret,
            # 与上面一步中传入的redirect_uri保持一致。
            'redirect_uri': self.redirect_uri,
            # 上一步返回的authorization code。如果用户成功登录并授权，则会跳转到指定的回调地址，并在URL中带上Authorization Code。
            # 例如，回调地址为www.qq.com/my.php，则跳转到：http://www.qq.com/my.php?code=520DD95263C1CFEA087******注意此code会在10分钟内过期。
            'code': code
        }
        print('code钥匙：', code)
        # 构建url
        access_url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(data_dict)

        # 发送请求
        try:
            response = requests.get(access_url)

            # 提取数据
            # access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
            data = response.text

            # 转化为字典
            data = parse_qs(data)
        except:
            raise Exception('qq请求失败')

        # 提取access_token
        access_token = data.get('access_token', None)

        if not access_token:
            raise Exception('access_token获取失败')

        return access_token[0]

    # 获取open_id值

    def get_open_id(self, access_token):

        # 构建请求url
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        # 发送请求
        try:
            response = requests.get(url)

            # 提取数据
            # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
            # code=asdasd&msg=asjdhui  错误的时候返回的结果
            data = response.text
            data = data[10:-3]
        except:
            raise Exception('qq请求失败')
        # 转化为字典d
        try:
            data_dict = json.loads(data)
            # 获取openid
            openid = data_dict.get('openid')
        except:
            raise Exception('openid获取失败')

        return openid
