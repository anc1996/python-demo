# 一个空文件，告诉 Python 这个目录应该被认为是一个 Python 包。


# 必需要在工程的包中导入pymysql，并且要调用install_as_MySQLdb方法
import pymysql
# 调用此函数后，任何导入MySQLdb的应用程序会不知不觉地实际使用pymysql。
pymysql.install_as_MySQLdb()


"""
	
	# 推荐在项目根目录的 __init__.py 文件中调用，这是项目初始化的第一步，确保配置的统一性。
	
	1、Django 启动时读取 DATABASES['ENGINE'] 配置，选择使用 django.db.backends.mysql。
	2、django.db.backends.mysql 尝试导入 MySQLdb。
	3、调用 pymysql.install_as_MySQLdb() 后，pymysql 模块被动态映射为 MySQLdb。
	4、Django 成功加载 pymysql，并使用它与 MySQL 数据库通信。
	
	    sys.modules["MySQLdb"] = sys.modules["pymysql"]
"""