import json

from celery_tasks.send_sms_code.ronglian_sms_sdk import SmsSDK

from shop.settings import dev_settings as settings

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
accountSid = settings.accountSid

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
accountToken = settings.accountToken

# 请使用管理控制台首页的APPID或自己创建应用的APPID
appId = settings.appId

def send_message():

    '''
        1.接口声明文件：SDK \CCPRestSDK.py
        2.接口函数定义：def sendTemplateSMS(self, to,datas,tempId)
        3.参数说明：
        to: 短信接收手机号码集合,用英文逗号分开,如 '13810001000,13810011001',最多一次发送200个。
        datas：内容数据，需定义成数组方式，如模板中有两个参数，定义方式为array['Marry','Alon']。
        templateId: 模板Id,如使用测试模板，模板id为"1"，如使用自己创建的模板，则使用自己创建的短信模板id即可。
    '''
    sdk = SmsSDK(accountSid, accountToken, appId)
    tid = '1'
    mobile = '15775023056'
    datas = ('4444', '5')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)



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
            # hasattr: 这是通过调用 getattr（obj， name） 并捕获 AttributeError 来完成的。
            # 如果单例不存在，初始化单例
            cls._instance=super(CCP,cls).__new__(cls,*args,**kwargs)
            # 初始化REST SDK
            cls._instance.sdk = SmsSDK(accountSid, accountToken, appId)
        # 返回单例
        return cls._instance

    # 用单例调用对象方法
    def send_template_sms(self,mobile,datas,tid):
        # 发送短信验证码的方法
        """
        """
        # self指向对象方法cls._instance，结果self=<__main__.CCP object at 0x7facc21f6df0>
        resp_str = self._instance.sdk.sendMessage(tid, mobile, datas) # 返回字符串
        resp_dict=json.loads(resp_str) # 短信验证码发送有延迟
        '''
        {
            'statusCode': '000000',
            'templateSMS': {'smsMessageSid': '87cab8cccace4fc6bc0d17e96f3eadb4', 'dateCreated': '20240428224744'}
        }
        '''
        
        if(resp_dict.get('statusCode')=='000000'):
            return 0
        else:
            print(resp_str)
            return -1

if __name__ == '__main__':
    # 测试发短信test专用
    # send_message()

    # 单例类发送短信验证码，测试的短信模板编号为1，电话号码仅支持1-4位，datas:['变量1'，’变量2‘]
    CCP().send_template_sms('15775023056',['1134', 5],'1')