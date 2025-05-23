from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    """自定义文件存储系统"""
    '''
    在你的存储类中，除了其他自定义的方法外，还必须实现 _open() 以及 _save() 等其他适合你的存储类的方法

    另外，如果你的类提供了本地文件存储，它必须重写 path() 方法。您的存储类必须是 deconstructible，以便在迁移中的字段上使用它时可以序列化。
    只要你的字段有自己的参数 serializable，你可以使用django.utils.deconstruct.deconstructible 类装饰器（这是 Django 在 FileSystemStorage 上使用的）。
    '''

    def __init__(self, fdfs_base_url=None):
        # Django 必须能以无参数实例化你的存储系统。
        # 方法一
        # if not fdfs_base_url:
        #     self.fdfs_base_url=settings.fdfs_base_url
        # 方法二：
        self.fdfs_base_url=fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self,name, mode='rb'):
        """
        调用者 Storage.open() ，这是存储类用于打开文件的实际机制。
        这必须返回一个 File 对象，但在大多数情况下，您需要在此处返回一些子类，这些子类实现特定于后端存储系统的逻辑。
        当文件不存在时，应引发 FileNotFoundError 异常。
        :name:文件路径
        :param mode:文件打开方式
        :return:因为当前不是去打开某个文件，所有这个方法不用。
        """
        pass

    def save(self, name, content, max_length=None):
        
        """将新内容保存到按名称指定的文件中。内容应该是适当的 File 对象或任何类似 Python 文件的对象，可以从一开始就阅读。 """
        # 获取文件的正确名称，因为它实际上将被保存。
        
        # 1、创建客户端对象:
        client=Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 2、调用上传函数, 进行上传:
        result=client.upload_by_buffer(content.read())
        # 判断是否上传成功:
        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')

        # 上传成功: 返回 file_id:
        file_id = result.get('Remote file_id')
        if '\\' in file_id:
            file_id = file_id.replace('\\', '//')
        # 这个位置返回以后, django 自动会给我们保存到表字段里.
        return file_id


#     def _save(self,name, content):
#         """
#         将来管理后台系统中，需要实现文件上传。
#     调用者 Storage.save() . name 意志已经经过 get_valid_name() 了 和 get_available_name() ，
#      content 意志本身就是一个 File 对象。
#
# 在调用Storage.save()方法时，文件名已经经过get_valid_name()和get_available_name()方法处理，确保文件名符合要求且不会覆盖其他文件。
#         :param name:文件路径
#         :param content:文件二进制内容
#         :return:None，应返回保存的文件的实际名称（通常是 name 传入的文件，但如果存储需要更改文件名，则返回新名称）。
#         """
#
#         pass

    def url(self,name):
        """
        返回可以访问 name 引用的文件内容的URL。对于不支持通过 URL 访问的存储系统，这将引发 NotImplementedError。
        :param name:文件相对路径
        :return: 返回文件的全路径，http://***.**.**.**:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        """
        return self.fdfs_base_url+name

    # 我们再添加一个新的方法
    # 该方法会在我们上传之前,判断文件名称是否冲突
    def exists(self, name):
        # 根据上面的图片我们可知,
        # fdfs 中的文件名是由 fdfs 生成的, 所以不可能冲突
        # 我们返回 False: 永不冲突
        return False