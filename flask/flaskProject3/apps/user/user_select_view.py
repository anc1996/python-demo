#!/user/bin/env python3
# -*- coding: utf-8 -*-
from lib2to3.fixes.fix_input import context

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.testing.suite.test_reflection import users

from apps.user.model import User
from sqlalchemy import or_,and_,not_,desc


"""
1.查询：
	查询所有： 模型类.query.all()    ~  select * from user;
	如果有条件的查询：
	         模型类.query.filter_by(字段名 = 值)   ～  select * from user where 字段=值；
	         模型类.query.filter_by(字段名 = 值).first()   ～  select * from user where 字段=值 limit..；
	
	select * from user where age>17 and gender='男'；
	select * from user where username like 'zhang%';
	select * from user where rdatetime> xxx and rdatetime < xxx;
	
	         模型类.query.filter()  里面是布尔的条件   模型类.query.filter(模型名.字段名 == 值)
	         模型类.query.filter_by()  里面是一个等值   模型类.query.filter_by(字段名 = 值)


***** 模型类.query.filter() ******
	1. 模型类.query.filter().all()   -----> 列表
	2. 模型类.query.filter().first()  ----->对象
	3.User.query.filter(User.username.endswith('z')).all()   select * from user where username like '%z';
	  User.query.filter(User.username.startswith('z')).all()  # select * from user where username like 'z%';
	  User.query.filter(User.username.contains('z')).all()  # select * from user where username like '%z%';
	  User.query.filter(User.username.like('z%')).all()

  多条件：
  from sqlalchemy import or_, and_,not_
  并且： and_    获取： or_   非： not_
	  User.query.filter(or_(User.username.like('z%'), User.username.contains('i'))).all()
	   类似： select * from user where username like 'z%' or username like '%i%';
	
	  User.query.filter(and_(User.username.contains('i'), User.rdatetime.__gt__('2020-05-25 10:30:00'))).all()
	   # select * from user where username like '%i%' and rdatetime < 'xxxx'

  补充：__gt__,__lt__,__ge__(gt equal),__le__ （le equal）  ----》通常应用在范围（整型，日期）
       也可以直接使用 >  <  >=  <=  !=

	  User.query.filter(not_(User.username.contains('i'))).all()
	
	  18 19 20 17 21 22 ....
	  select * from user where age in [17,18,20,22];


排序：order_by

    user_list = User.query.filter(User.username.contains('z')).order_by(-User.rdatetime).all()  # 先筛选再排序
    user_list = User.query.order_by(-User.id).all()  对所有的进行排序
    注意：order_by(参数)：
    1。 直接是字符串： '字段名'  但是不能倒序
    2。 填字段名： 模型.字段    order_by(-模型.字段)  倒序

限制： limit
    # limit的使用 + offset
    # user_list = User.query.limit(2).all()   默认获取前两条
    user_list = User.query.offset(2).limit(2).all()   跳过2条记录再获取两条记录


 总结：
 1. User.query.all()  所有
 2. User.query.get(pk)  一个
 3. User.query.filter()   *   ？？？？？？？
     如果要检索的字段是字符串（varchar，db.String）:
       User.username.startswith('')
       User.username.endswith('')
       User.username.contains('')
       User.username.like('')
       User.username.in_(['','',''])
       User.username == 'zzz'
    如果要检索的字段是整型或者日期类型：
       User.age.__lt__(18)
       User.rdatetime.__gt__('.....')
       User.age.__le__(18)
       User.age.__ge__(18)
       User.age.between(15,30)

     多个条件一起检索： and_, or_
     非的条件： not_

     排序：order_by()
     获取指定数量： limit() offset()
 4. User.query.filter_by()


 删除:
 两种删除：
 1。逻辑删除（定义数据库中的表的时候，添加一个字段isdelete，通过此字段控制是否删除）
 id = request.args.get(id)
 user = User.query.get(id)
 user.isdelete = True
 db.session.commit()

 2。物理删除(彻底从数据库中删掉)
 id = request.args.get(id)
 user = User.query.get(id)
 db.session.delete(user)
 db.session.commit()


 更新:
 id = request.args.get(id)
 user = User.query.get(id)
 # 修改对象的属性
 user.username= xxxx
 user.phone =xxxx
 # 提交更改
 db.session.commit()


 两张表
"""

# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
user_select_bp = Blueprint('user_select', __name__, url_prefix='/user_select')

def user_tempelate(user):
	return {
		'username':user.username,
		'phone':user.phone,
		'email':user.email,
		'register_time':user.register_time
	}

@user_select_bp.route('/get')
def user_select():
	# 查询所有用户
	user = User.query.get(1) # 查询id为1的用户
	context=user_tempelate(user)
	return context

@user_select_bp.route('/getall')
def user_select_all():
	# 查询所有用户
	users = User.query.filter_by(is_deleted=False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/getusername')
def user_select_username():
	# 查询所有用户
	username=request.args.get('username')
	# 方法一：
	user = User.query.filter_by(username=username,is_deleted=False).first()
	# 方法二：
	# user = User.query.filter(User.username == username,User.is_deleted == False).first()
	context=user_tempelate(user)
	return context

@user_select_bp.route('/user_startwith')
def user_select_startwith():
	email=request.args.get('email')
	# startswith :查询以指定字符串开头的数据
	users = User.query.filter(User.email.startswith(email),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_endwith')
def user_select_endwith():
	email=request.args.get('email')
	# endswith :查询以指定字符串结尾的数据
	users = User.query.filter(User.email.endswith(email),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_like')
def user_select_like():
	email=request.args.get('email')
	# like :查询包含指定字符串的数据
	users = User.query.filter(User.email.like('%'+email+'%'),User.is_deleted == False).all()
	# nolike
	# users = User.query.filter(~User.email.like('%'+email+'%'),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_notlike')
def user_select_notlike():
	"""
	查询指定邮箱的用户:/user_notlike?email=qq
	:return:
	"""
	email=request.args.get('email')
	# nolike :查询包含指定字符串的数据
	users = User.query.filter(User.email.notlike('%'+email+'%'),User.is_deleted == False).all()
	# users = User.query.filter(~User.email.like('%'+email+'%'),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list


@user_select_bp.route('/user_contains')
def user_select_contains():
	email=request.args.get('email')
	# contains :查询包含指定字符串的数据
	users = User.query.filter(User.email.contains(email),User.is_deleted == False).all()
	# no contains
	# users = User.query.filter(~User.email.contains(email),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list


@user_select_bp.route('/user_or')
def user_select_or():
	username1=request.args.get('username1')
	username2=request.args.get('username2')
	# 方法一：使用or_
	users = User.query.filter(or_(User.username.contains(username1),User.username.contains(username2)),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_and')
def user_select_and():
	username1=request.args.get('username1')
	username2=request.args.get('username2')
	# 方法一：
	# users = User.query.filter(User.username.contains(username1),User.username.contains(username2),User.is_deleted == False).all()
	# 方法二：and_
	users = User.query.filter(and_(User.username.contains(username1),User.username.contains(username2)),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list



@user_select_bp.route('/user_in')
def user_select_in():
	"""
	查询指定邮箱的用户:/user_in?usernames=123,234
	:return:
	"""
	usernames=request.args.get('usernames')
	username_list=usernames.split(',')
	# in_ :查询包含指定字符串的数据
	users = User.query.filter(User.username.in_(username_list),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_not')
def user_select_not():
	"""
	查询指定邮箱的用户:/user_not?username=123
	:return:
	"""
	username=request.args.get('username')
	# not_ :查询不包含指定字符串的数据
	users = User.query.filter(not_(User.username.contains(username)),User.is_deleted == False).all()
	# users = User.query.filter(~User.username.contains(username),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list


@user_select_bp.route('/user_gt')
def user_select_gt():
	"""
	查询指定邮箱的用户:/user_gt?register_time=2023-06-01
	:return:
	"""
	register_time=request.args.get('register_time')
	# gt :查询大于指定时间的数据
	users=User.query.filter(User.register_time.__gt__(register_time),User.is_deleted == False).all()
	# users = User.query.filter(User.register_time > register_time,User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_ge')
def user_select_ge():
	"""
	查询指定邮箱的用户:/user_ge?register_time=2023-06-01
	:return:
	"""
	register_time=request.args.get('register_time')
	# ge :查询大于等于指定时间的数据
	users=User.query.filter(User.register_time.__ge__(register_time),User.is_deleted == False).all()
	# users = User.query.filter(User.register_time >= register_time,User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_lt')
def user_select_lt():
	"""
	查询指定邮箱的用户:/user_lt?register_time=2023-06-01
	"""
	register_time=request.args.get('register_time')
	# lt :查询小于指定时间的数据
	users=User.query.filter(User.register_time.__lt__(register_time),User.is_deleted == False).all()
	# users = User.query.filter(User.register_time < register_time,User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_le')
def user_select_le():
	"""
	查询指定邮箱的用户:/user_le?register_time=2023-06-01
	"""
	register_time=request.args.get('register_time')
	# le :查询小于等于指定时间的数据
	users=User.query.filter(User.register_time.__le__(register_time),User.is_deleted == False).all()
	# users = User.query.filter(User.register_time <= register_time,User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_between')
def user_select_between():
	"""
	查询指定邮箱的用户:/user_between?start_time=2022-06-01&end_time=2023-06-01
	"""
	start_time=request.args.get('start_time')
	end_time=request.args.get('end_time')
	# between :查询指定时间范围的数据
	users = User.query.filter(User.register_time.between(start_time,end_time),User.is_deleted == False).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

# order_by用法
@user_select_bp.route('/user_order_by')
def user_order_by():
	"""
	查询指定邮箱的用户:
		升序：/user_order_by?order_by=username
	"""
	# 选择字段排序
	order_by=request.args.get('order_by')
	# order_by :从大到小排序
	users = User.query.filter(User.is_deleted == False).order_by(order_by).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

@user_select_bp.route('/user_order_by_desc')
def user_order_by_desc():
	"""
	查询指定邮箱的用户:
		降序：/user_order_by_desc?order_by=username
	"""
	# 选择字段排序
	order_by=request.args.get('order_by')
	# order_by :从大到小排序
	users = User.query.filter(User.is_deleted == False).order_by(desc(order_by)).all()
	# users=User.query.filter(User.is_deleted == False).order_by(-User.username).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

# limit用法+offset偏移
@user_select_bp.route('/user_limit')
def user_limit():
	"""
		用户：/user_limit?limit=2&offset=1
	"""
	limit = request.args.get('limit')
	offset = request.args.get('offset')
	# limit :限制查询数量，offset：偏移量,表示从第几条开始
	users = User.query.filter(User.is_deleted == False).limit(limit).offset(offset).all()
	context_list=[]
	for user in users:
		context_list.append(user_tempelate(user))
	return context_list

