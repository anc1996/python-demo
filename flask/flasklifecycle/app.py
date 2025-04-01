from flask import Flask, request, jsonify, g, session, current_app


def create_app():
	"""应用工厂函数"""
	app = Flask(__name__)
	app.secret_key = "secret_key_demo"  # 用于加密会话数据
	
	# ================= 上下文管理 =================
	
	@app.before_request
	def before_request_logging():
		"""在每次请求处理之前调用"""
		print(f"[Before Request] 请求方法: {request.method}, 请求路径: {request.path}")
		g.start = "Request Context Initialized"
	
	@app.after_request
	def after_request_logging(response):
		"""在每次请求处理之后调用"""
		print(f"[After Request] 响应状态: {response.status}")
		response.headers["X-Demo-Header"] = "Flask Lifecycle Demo"
		return response
	
	@app.teardown_request
	def teardown_request_logging(exception=None):
		"""请求处理结束后调用，用于清理"""
		print(f"[Teardown Request] 清理请求上下文, 异常: {exception}")
	
	@app.teardown_appcontext
	def teardown_appcontext_logging(exception=None):
		"""应用上下文结束时调用"""
		print(f"[Teardown AppContext] 清理应用上下文, 异常: {exception}")
	
	# ================= 路由和视图函数 =================
	
	@app.route("/")
	def index():
		"""主页视图"""
		print("[View Function] 主页被调用")
		session["user"] = "Alice"  # 演示会话数据的存储
		return jsonify({"message": "Welcome to Flask Lifecycle Demo!"})
	
	@app.route("/error")
	def trigger_error():
		"""触发一个示例错误"""
		print("[View Function] 错误视图被调用")
		raise ValueError("This is a demo exception!")
	
	@app.errorhandler(500)
	def handle_internal_server_error(error):
		"""错误处理器"""
		print("[Error Handler] 捕获 500 错误")
		return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
	
	@app.route("/data")
	def data_view():
		"""数据视图函数"""
		print("[View Function] 数据视图被调用")
		user = session.get("user", "Guest")
		return jsonify({"user": user, "data": [1, 2, 3]})
	
	return app


def init_app(app):
	"""应用初始化函数"""
	print("[Initializing] 应用初始化设置")
	# 这里可以添加其他初始化代码
	# 例如：数据库初始化、插件注册等


# ================= 主程序 =================

if __name__ == "__main__":
	app = create_app()  # 创建应用实例
	init_app(app)  # 初始化应用
	print("[Starting] Flask 应用启动")
	app.run(host="0.0.0.0", port=5001, debug=True)