# -*- coding:utf-8 -*-


from verifications.libs.SMScode.CCPRestSDK import REST

'''
    1.接口声明文件：SDK \CCPRestSDK.py
    2.接口函数定义：def sendTemplateSMS(self, to,datas,tempId) 
    3.参数说明：
    to: 短信接收手机号码集合,用英文逗号分开,如 '13810001000,13810011001',最多一次发送200个。
    datas：内容数据，需定义成数组方式，如模板中有两个参数，定义方式为array['Marry','Alon']。 
    templateId: 模板Id,如使用测试模板，模板id为"1"，如使用自己创建的模板，则使用自己创建的短信模板id即可。
'''

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da881ad97540181ba09d9b90215'


# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '6202374657f446eab2da5fcbc09f0029'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf070881ad8ad40181ba1b34f5025f'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'app.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'


def sendTemplateSMS(to, datas, tempId):
    '''
    发送短信验证码测试用例
    :param to:
    :param datas:
    :param tempId:
    :return:
    '''
    # 云通讯官方提供的发送短信代码实例
    # 发送模板短信
    # @param to 手机号码
    # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
    # @param $tempId 模板Id
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    print(result)

# 单例设计模式，单例模式确保某个类有且仅有一个实例，而且自行实例化并向整个系统提供这个实例
'''
单例类是一种设计模式，它确保一个类只有一个实例，并提供一个全局访问点。
单例类的目的是确保在整个应用程序中只有一个实例的类。
单例类的用途包括：
    共享资源：如果一个类负责共享资源，例如数据库连接或线程池，那么使用单例类可以确保在整个应用程序中只有一个实例，
            从而避免资源冲突。
    状态管理：单例类可以作为全局状态管理器，用于存储应用程序中的全局状态，例如配置信息、用户信息等。
    工具类：某些类提供的方法和属性不依赖于实例，可以直接通过类名访问，这样的类可以设计为单例类。
    避免循环引用：在某些情况下，类之间可能存在循环引用，导致无法正常销毁对象。使用单例类可以避免这种情况，
                因为单例类的实例始终存在。
'''
class CCP(object):
    """发送短信验证码的单例类"""
    # 定义单例的初始化方法
    def __new__(cls, *args, **kwargs):
        # 。__new__方法用于创建对象并返回对象,__new__方法是静态方法，而__init__是实例方法。
        """
        :return: 单例对象
        """
        # 判断单例是否存在:_instance是一个类属性，用于存储单例对象的引用
        if not hasattr(cls,'_instatance'):
            #hasattr: This is done by calling getattr(obj, name) and catching AttributeError.
            # 如果单例不存在，初始化单例
            cls._instance=super(CCP,cls).__new__(cls,*args,**kwargs)
            # 初始化REST SDK
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        # 返回单例
        return cls._instance

    # 用单例调用对象方法
    def send_template_sms(self,to,datas,tempId):
        # 发送短信验证码的方法
        """
        :param to:手机号码
        :param datas:内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        :param tempId: 模板Id,测试模板id位1
        :return:成功：0；失败：-1
        """
        # self指向对象方法cls._instance，结果self=<__main__.CCP object at 0x7facc21f6df0>
        result=self._instance.rest.sendTemplateSMS(to,datas,tempId)
         # 短信验证码发送有延迟
        # {'statusCode': '000000', 'templateSMS': {'smsMessageSid': '87cab8cccace4fc6bc0d17e96f3eadb4', 'dateCreated': '20240428224744'}}
        if(result.get('statusCode')=='000000'):
            return 0
        else:
            print(result)
            return -1


if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1，电话号码仅支持1-4位，
    # sendTemplateSMS('15775023056', ['4234', 5], 1)

    # 单例类发送短信验证码，测试的短信模板编号为1，电话号码仅支持1-4位，datas:['变量1'，’变量2‘]
    CCP().send_template_sms('15775023056',['1234', 5], 1)