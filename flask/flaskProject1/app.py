import json

from flask import Flask, Response, make_response, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

# 读取配置信息,silent 参数设置为 True，如果没有找到配置文件，则不会报错
app.config.from_pyfile('settings.py', silent=True)

# 检查配置信息是否加载成功
print(f'app.config:{app.config}')


@app.route('/', endpoint='index')
# endpoint: 为视图函数指定一个名称，这样就可以通过 url_for('index') 反向解析到这个视图函数
def index(name=None):
	# 使用 render_template() 方法可以渲染模板，您只要提供模板 名称和需要作为参数传递给模板的变量就行了。
	# 这里的name参数是传递给模板的变量
	return render_template('index.html', name=name)


@app.route('/hello_world')
def hello_world():  # put application's code here
	# 将配置转换为字符串格式并返回
	config_info = '\n'.join(f'{key}: {value}' for key, value in app.config.items())
	return f'Hello, World!<br>配置信息:<br>{config_info}'


data = {'a': '北京', 'b': '上海', 'c': '广州', 'd': '深圳'}


# 通过把 URL 的一部分标记为 <variable_name> 就可以在 URL 中添加变量。
# 标记的部分会作为关键字参数传递给函数。通过使用 <converter:variable_name> ，
# 可以选择性的加上一个转换器，为变量指 定规则。
@app.route('/getcity/<city>')
def get_city(city):
	print(type(city))  # <class 'str'>
	return data.get(city, '未找到')


@app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	# escape() 函数可以对字符串进行转义处理
	return f'User {escape(username)}'


@app.route('/add/<int:num1>/<int:num2>')
def show_post(num1, num2):
	# show the post with the given id, the id is an integer
	if num1 >= 0 and num2 >= 0:
		result = num1 + num2
		return f'add {result}'
	return 'num1和num2必须是正整数'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	# show the subpath after /path/,
	# subpath is a string
	return f'Subpath {escape(subpath)}'


# float
@app.route('/float/<float:float_num>')
def show_float(float_num):
	"""
	/float/1.2
	:param float_num:
	:return:
	"""
	# show the float after /float/
	return f'Float {escape(float_num + 0.5)}'


# uuid
@app.route('/uuid/<uuid:uuid>')
def show_uuid(uuid):
	"""
	/uuid/123e4567-e89b-12d3-a456-426614174000,否则报错
	:param uuid:
	:return:
	"""
	# show the uuid after /uuid/
	return f'UUID {escape(uuid)}'


# 唯一的 URL / 重定向行为
@app.route('/projects/')
def projects():
	# projects 的 URL 是中规中矩的，尾部有一个斜杠，看起来就如同一个文件夹。
	# 访问一个没有斜杠结尾的 URL （ /projects ）时 Flask 会自动进 行重定向，帮您在尾部加上一个斜杠（ /projects/ ）。
	return 'The project page'


@app.route('/about')
def about():
	# about 的 URL 没有尾部斜杠，这样看起来更像一个文件。
	# 如果访问 这个 URL 时添加了尾部斜杠（ /about/ ）就会得到一个 404 “未找到” 错误。这样可以保持 URL 唯一，并有助于搜索引擎重复索引同一 页面。
	return 'The about page'


@app.route('/h1')
def html_res():
	# 返回一个 Response 对象，可以渲染 HTML 标签
	# default_mimetype: str | None = "text/html"
	return Response('<h1>你好</h1>')


@app.route('/dict_response')
def dict_res():
	# 返回一个字典，Flask 会自动转换为 JSON 格式
	# 返回的数据类型是 application/json
	# 200：状态码
	return data, 200


@app.route('/make_response')
def make_res():
	headers = {'request_headers': request.headers,  # 请求头
	           'request_path': request.path,  # 请求路径
	           'request_method': request.method,  # 请求方法
	           'request_url': request.url,  # 请求 URL
	           'request_base_url': request.base_url,  # 请求的基础 URL
	           'request_host': request.host,  # 请求的主机名
	           }
	
	response = make_response(render_template('response1.html', foo=request.headers))
	response.headers['X-Parachutes'] = 'parachutes are cool'
	response.headers['hello'] = 'world'
	
	response.set_cookie('name', 'make_response')
	
	return response


@app.route('/routes')
def show_routes():
	# 返回一个字典，Flask 会自动转换为 JSON 格式
	# 返回的数据类型是 application/json
	# 200：状态码
	routes = []
	for rule in app.url_map.iter_rules():
		routes.append(f"{rule.endpoint}: {rule.rule}")
	return '<br>'.join(routes)


@app.route('/make_response2', methods=['GET', 'POST'])
def make_response2():
	if request.method == 'POST':
		data = {
			# post请求在请求体里
			'request_form': request.form,  # 请求表单数据
			'request_username': request.form.get('username'),
			'request_password': request.form.get('password'),
			'request_repassword': request.form.get('repassword'),
			'request_full_path': request.full_path,  # 请求的完整路径
			'request_path': request.path,  # 请求路径
			'request_method': request.method,  # 请求方法
		}
		if data['request_password'] == data['request_repassword']:
			user = {'username': data['request_username'], 'password': data['request_password']}
			users.append(user)
	else:
		data = {
			# get请求在url里
			'request_args': request.args,  # 请求参数
			'post_username': request.args.get('username'),
			'post_password': request.args.get('password'),
			'post_repassword': request.args.get('repassword'),
			'request_full_path': request.full_path,  # 请求的完整路径
			'request_path': request.path,  # 请求路径
			'request_method': request.method,  # 请求方法
		}
		# 用户密码一致性验证
		if data['post_password'] == data['post_repassword']:
			user = {'username': data['post_username'], 'password': data['post_password']}
			users.append(user)
	return redirect(url_for('index'))  # url_for('index') 反向解析


users = []


@app.route('/show')
def show():
	# users[] ----> str''   json字符串
	j_str = json.dumps(users)
	return j_str


class Girl:
	def __init__(self, name, addr):
		self.name = name
		self.gender = '女'
		self.addr = addr
	
	def __str__(self):
		return self.name


@app.route('/show1')
def show1():
	name = '沈凯'  # str
	age = 18  # int
	friends = ['建义', '陈璟', '小岳岳', '郭麒麟']  # list
	dict1 = {'gift': '大手镯', 'gift1': '鲜花', 'gift2': '费列罗'}  # dict
	girlfriend = Girl('小芳', '北京')  # 对象
	return render_template('show1.html', name=name, age=age, friends=friends, dict1=dict1, girlfriend=girlfriend)


@app.route('/show2')
def show2():
	"""讲解jinja的for和if用法"""
	girls = ['如花', '凤姐', '宋宋', '孙艺珍', '建玲', '林允儿']
	users = [
		{'username': 'zhangsan1', 'password': '123123', 'addr': '北京', 'phone': '13900001010'},
		{'username': 'zhangsan2', 'password': '123111', 'addr': '上海', 'phone': '13900991010'},
		{'username': 'zhangsan3', 'password': '123222', 'addr': '武汉', 'phone': '13900009990'},
		{'username': 'zhangsan4', 'password': '123333', 'addr': '西安', 'phone': '13900008810'},
		{'username': 'zhangsan5', 'password': '123444', 'addr': '成都', 'phone': '13977771010'},
		{'username': 'zhangsan6', 'password': '123555', 'addr': '深圳', 'phone': '13900121010'},
	
	]
	return render_template('show2.html', girls=girls, users=users)


@app.route('/show3')
def show3():
	"""讲解jinja的过滤器"""
	girls = ['如花', '凤姐', '宋宋', '孙艺珍', '建玲', '林允儿']
	girls.append('zhangshan')
	users = [
		{'username': 'zhangsan1', 'password': '123123', 'addr': '北京', 'phone': '13900001010'},
		{'username': 'zhangsan2', 'password': '123111', 'addr': '上海', 'phone': '13900991010'},
		{'username': 'zhangsan3', 'password': '123222', 'addr': '武汉', 'phone': '13900009990'},
		{'username': 'zhangsan4', 'password': '123333', 'addr': '西安', 'phone': '13900008810'},
		{'username': 'zhangsan5', 'password': '123444', 'addr': '成都', 'phone': '13977771010'},
		{'username': 'zhangsan6', 'password': '123555', 'addr': '深圳', 'phone': '13900121010'},
	]
	msg = '<h1>520快乐！</h1>'
	n1 = 'hello'
	return render_template('show3.html',girls=girls,users=users,msg=msg,n1=n1)

@app.route('/define_filter')
def define_filter():
	msg="hello everyone hello world"
	li=[1,2,3,4,5]
	return render_template('define_filter.html',msg=msg,li=li)

def replace_hello(value):
	print(value)
	value=value.replace('hello','hi')
	print(value)
	return value.strip() # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

# 第一种方式
# add_template_filter(filter_name, name=None)
app.add_template_filter(replace_hello,'replace_hello')

# 第二种方式
@app.template_filter('reverse_list')
def reverse_list(li):
	if isinstance(li,list):
		return list(reversed(li))
	return li


@app.route('/base')
def load_base():
	"""加载基础模板"""
	return render_template('base.html')


@app.route('/extends')
def extends():
	"""继承"""
	return render_template('extends.html')

@app.route('/include')
def include_html():
	"""导入"""
	return render_template('welcome.html')

@app.route('/macro1')
def show_macro1():
	"""宏，macro：In Jinja2,。它们允许您定义可重用的模板代码段。"""
	return render_template('macro/macro1.html')

@app.route('/macro2')
def show_macro2():
	"""宏，macro：In Jinja2,。它们允许您定义可重用的模板代码段。"""
	return render_template('macro/macro2.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5001, debug=True)
