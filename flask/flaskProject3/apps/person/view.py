#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, render_template
from flask.views import MethodView,View

from apps.person.model import Person

person_bp=Blueprint('person',__name__,url_prefix='/person')

# 基本类试图
@person_bp.route('/persons_function', methods=['GET'])
def list_persons():
    persons = Person.query_all()
    result = [{"id": p.id, "name": p.name, "age": p.age, "email": p.email} for p in persons]
    return jsonify(result)


# 基本可重用视图
# 视图的生命周期和 self
# 默认情况下，每次处理请求时都会创建一个新的视图类的实例。这意味着，在 请求期间向 self 写入数据是安全的，因为下一个请求不会看到它，不像 其他形式的全局状态。
# 将 View.init_every_request 设置为 False ，将会只创建一个类的 实例，并将其用于每个请求。在这种情况下，写数据到 self 是不安全的。 如果你需要在请求期间存储数据，那么请使用 g 代替。
class personlifecycle(View):
	
	# 默认情况下，生成的视图将为每个请求创建一个视图类的新实例，并调用其
	# ：meth：'dispatch_request' 方法。如果视图类将
	# ：attr：'init_every_request' 到 ''False'' ，则每个请求都将使用相同的实例。
	init_every_request = False
	
	def dispatch_request(self):
		persons = Person.query_all()
		return render_template('person/person_list.html', objects=persons)
	
# View.dispatch_request() 方法等同于视图函数。
	# 调用 View.as_view() 方法将创建一个视图函数，该函数可以在应用上使用 add_url_rule() 方法来注册。
# as_view 的第一个参数是用于 url_for() 的指向视图的名称。
person_bp.add_url_rule('/person_lifecycle', view_func=personlifecycle.as_view('person_lifecycle'))

class PersonLifecycleAPI(MethodView):
	
	
    def __init__(self):
        self.shared_data = {}

    def get(self, id):
        """通过 self 访问共享数据"""
        person = Person.get_or_404(id)
        self.shared_data["last_accessed"] = person.name
        result = {"id": person.id, "name": person.name, "age": person.age, "email": person.email}
        return jsonify(result)

    def post(self, id):
        """更新共享数据"""
        person = Person.get_or_404(id)
        data = request.json
        updated_person = Person.update(id, data)
        self.shared_data["last_updated"] = updated_person.name
        result = {"id": updated_person.id, "name": updated_person.name, "age": updated_person.age, "email": updated_person.email}
        return jsonify(result)

# 注册路由
person_bp.add_url_rule('/person-lifecycleapi/<int:id>', view_func=PersonLifecycleAPI.as_view('person_lifecycleapi'))



# URL 规则
# 任何由URL捕获的变量都会作为关键字参数传递给 dispatch_request 方法， 就像普通的视图函数一样。
class personDetailView(View):
	
    def __init__(self, model):
        self.model = model
        self.template = f"person/{model.__tablename__.lower()}_detail.html"

    def dispatch_request(self, id):
        item = self.model.get_or_404(id)
        return render_template(self.template, item=item)

person_bp.add_url_rule(
    "/persons-detail/<int:id>",
	# as_view() 方法的第二个参数是模型类，它将在 dispatch_request() 方法中使用。
    view_func=personDetailView.as_view("persons_detail", Person)
)

class PersonView(View):
	# 一个常见的模式是用 methods=["GET", "POST"] 注册一个视图， 然后检查 request.method == "POST" 来决定做什么。
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            # 处理 POST 请求，创建新的 Person
            data = request.json
            new_person = Person.create(data)
            return jsonify({"id": new_person.id, "name": new_person.name, "age": new_person.age, "email": new_person.email})
        else:
            # 处理 GET 请求，返回所有 Person 列表
            persons = Person.query_all()
            result = [{"id": p.id, "name": p.name, "age": p.age, "email": p.email} for p in persons]
            return jsonify(result)

# 注册路由
person_bp.add_url_rule('/person-view', view_func=PersonView.as_view('person_view'))

class PersonAPI(MethodView):
    """
    MethodView 扩展了基本的 View ，以根据请求方法调度 类的不同方法。每个 HTTP 方法都会映射到类中具有相同（小写）名称的方法。
    MethodView 基于该类定义的方法自动设置 View.methods 。 它甚至知道如何处理子类覆盖或定义其他方法。
    """
    
    """处理 Person 的 CRUD 操作."""

    def get(self, id=None):
        if id is None:
            # 获取所有 Person 数据
            persons = Person.query_all()
            result = [{"id": p.id, "name": p.name, "age": p.age, "email": p.email} for p in persons]
            return jsonify(result)
        else:
            # 获取单个 Person 数据
            person = Person.get_or_404(id)
            result = {"id": person.id, "name": person.name, "age": person.age, "email": person.email}
            return jsonify(result)

    def post(self):
        # 创建新的 Person 数据
        data = request.json
        new_person = Person.create(data)
        result = {"id": new_person.id, "name": new_person.name, "age": new_person.age, "email": new_person.email}
        return jsonify(result), 201

    def patch(self, id):
        # 更新单个 Person 数据
        data = request.json
        updated_person = Person.update(id, data)
        result = {"id": updated_person.id, "name": updated_person.name, "age": updated_person.age, "email": updated_person.email}
        return jsonify(result)

    def delete(self, id):
        # 删除单个 Person 数据
        Person.delete(id)
        return '', 204
    
# 注册 API 路由
person_view = PersonAPI.as_view('person_api')
person_bp.add_url_rule('/person_api', view_func=person_view, methods=['GET', 'POST'])
person_bp.add_url_rule('/person_api/<int:id>', view_func=person_view, methods=['GET', 'PATCH', 'DELETE'])