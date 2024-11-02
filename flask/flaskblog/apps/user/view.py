#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re
import uuid

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, session, make_response, current_app, g
from sqlalchemy import or_,func
from sqlalchemy.exc import SQLAlchemyError

from apps.article.model import Article,ArticleType
from apps.user.model import User, UserInfo, UserAlbum
from extends import db, cache
from extends.file_function import upload_file
from extends.minio_bucket import flask_bucket
from extends.wangyisms.sms import send_sms
from extends.login_verify import login_required


# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
user_bp = Blueprint('user', __name__, url_prefix='/user')

# after_request是在每次请求之后执行的函数
@user_bp.after_request
def after_request(response):
	print('after_request,蓝图局域用法')
	response.set_cookie('a', 'bbbb', max_age=19)
	return response


@user_bp.route('/check_username', methods=['GET'])
def check_username():
	username = request.args.get('username')
	user = User.query.filter_by(username=username).first()
	if user:
		return jsonify({'exists': False, 'error_msg': '用户名已存在'})
	else:
		return jsonify({'exists': True})


@user_bp.route('/check_phone', methods=['GET'])
def check_phone():
	phone = request.args.get('phone')
	if not re.match(r'^1[3-9]\d{9}$', phone):
		return jsonify({'exists': False, 'error_msg': '手机号格式不正确'})
	
	user = User.query.filter_by(phone=phone).first()
	if user:
		return jsonify({'exists': False, 'error_msg': '手机号已存在'})
	else:
		return jsonify({'exists': True})


@user_bp.route('/check_email', methods=['GET'])
def check_email():
	email = request.args.get('email')
	if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email):
		return jsonify({'exists': False, 'error_msg': '邮箱格式不正确'})
	
	user = User.query.filter_by(email=email).first()
	if user:
		return jsonify({'exists': False, 'error_msg': '邮箱已存在'})
	else:
		return jsonify({'exists': True})


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	if request.method == 'POST':
		# 获取post提交的数据
		username = request.form.get('username')
		password = request.form.get('password')
		repassword = request.form.get('repassword')
		phone = request.form.get('phone')
		email = request.form.get('email')
		# 判断用户名和密码是否为空
		if not all([username, password, repassword]):
			return render_template('user/register.html', submit_error_msg='用户名和密码不能为空',second_level_categories=second_level_categories)
		# 判断两次密码是否一致
		if password != repassword:
			return render_template('user/register.html', submit_error_msg='两次密码不一致',second_level_categories=second_level_categories)
		
		# 判断手机号是否为空且格式是否正确
		if not phone and re.match(r'^1[3-9]\d{9}$', phone):
			return render_template('user/register.html', submit_error_msg='手机号格式不正确',second_level_categories=second_level_categories)
		
		# 判断邮箱是否为空且格式是否正确
		if not email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
			return render_template('user/register.html', submit_error_msg='邮箱格式不正确',second_level_categories=second_level_categories)
		# 判断用户是否已经注册
		# if any(user.username == username for user in users):
		# 	return render_template('user/register.html', msg='用户已注册')
		# 第一步：创建user对象
		user = User(username=username, password=password, email=email, phone=phone)
		# 第二步：将user对象添加到数据库
		db.session.add(user)
		db.session.commit()
		# 注册成功，跳转到个人资料页
		response = make_response(redirect(url_for('home.index')))
		# 设置cookie加密
		singed_user_id = current_app.serializer.dumps({'user_id': user.id})
		# cookie实现机制;httponly表示只能通过http协议访问，不能通过js访问，secure表示只能通过https协议访问
		response.set_cookie('user_id', singed_user_id, max_age=60 * 60 * 24 * 7, httponly=True, secure=False)
		# session 用法
		session[user.id] = user.username
		return response
	return render_template('user/register.html',second_level_categories=second_level_categories)


@user_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
	# 获取二级分类
	second_level_categories = g.second_level_categories
	if request.method == 'POST':
		type = request.args.get('type')
		if type == 'username':
			# 获取post提交的数据
			username = request.form.get('username')
			password = request.form.get('password')
			# 判断用户名和密码是否为空
			if not all([username, password]):
				return render_template('user/login.html', error_login_msg='用户名和密码不能为空',second_level_categories=second_level_categories)
			# 查找用户且
			user = User.query.filter_by(username=username).first()
			# 判断用户是否存在且密码是否正确
			if not user or not user.check_password(password):
				return render_template('user/login.html', error_login_msg='用户名或密码错误',second_level_categories=second_level_categories)
			# 判断用户是否被删除
			if user.is_deleted:
				return render_template('user/login.html', error_login_msg='用户已被删除,需要激活',second_level_categories=second_level_categories)
		elif type == 'phone':
			# 获取post提交的数据
			phone = request.form.get('phone')
			code = request.form.get('code')
			# 判断手机号和验证码格式是否正确
			if not re.match(r'^1[3-9]\d{9}$', phone) and not re.match(r'^\d{6}$', code):
				return render_template('user/login.html', error_login_msg='手机号和验证码格式不正确',second_level_categories=second_level_categories)
			# 验证code与redis数据库是否一致
			valid_code=cache.get(phone)
			# valid_code = current_app.redis_client.get(phone).decode('utf-8')
			if code != valid_code:
				return render_template('user/login.html', error_login_msg='验证码错误',second_level_categories=second_level_categories)
			# 查找用户是否存在
			user = User.query.filter_by(phone=phone).first()
			if not user:
				return render_template('user/login.html', error_login_msg='用户不存在',second_level_categories=second_level_categories)
			# 删除redis数据库中的验证码,若没有不报错
			# current_app.redis_client.delete(phone)
			cache.delete(phone)
		# 登录成功，跳转到个人资料页
		response = make_response(redirect(url_for('home.index')))
		# 设置cookie加密
		singed_user_id = current_app.serializer.dumps({'user_id': user.id})
		# cookie实现机制;httponly表示只能通过http协议访问，不能通过js访问，secure表示只能通过https协议访问
		response.set_cookie('user_id', singed_user_id, max_age=60 * 60 * 24 * 7, httponly=True, secure=False)
		# session 用法
		session[user.id] = user.username
		return response
	
	# get请求，用于登录
	return render_template('user/login.html',second_level_categories=second_level_categories)


@user_bp.route('/sendmsg', methods=['GET', 'POST'], endpoint='sendmsg')
def sendmsg():
	# 用手机验证码登录
	sms_provider = request.form.get('sms_provider')
	phone = request.form.get('phone')
	
	# 验证手机号格式
	if not re.match(r'^1[3-9]\d{9}$', phone):
		return jsonify({'sms_status': '手机号格式不正确', 'status': 400}), 400
	
	# 验证用户是否存在
	user = User.query.filter_by(phone=phone).first()
	if not user:
		return jsonify({'sms_status': '用户不存在', 'status': 404}), 404
	
	# 验证短信服务商
	if sms_provider not in ['netease', 'ali']:
		return jsonify({'sms_status': '请选择短信服务商', 'status': 400}), 400
	
	# 发送验证码
	if sms_provider == 'netease':
		success, code = send_sms(phone)
	elif sms_provider == 'ali':
		# 用阿里云发送验证码
		# 这里需要实现阿里云发送验证码的逻辑
		success, code = True, '123456'  # 示例代码，实际应替换为阿里云发送验证码的逻辑
	
	# 处理发送结果
	if success:
		# 状态200
		cache.set(phone, code, timeout=60)  # 60秒过期
		# current_app.redis_client.set(phone, code, ex=100)  # 60秒过期
		return jsonify({"sms_status": "短信发送成功", 'status': 200}), 200
	else:
		return jsonify({"sms_status": "短信发送失败", 'status': 500}), 500


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
	
	# 创建响应对象并重定向到首页
	# make_response()函数用于创建响应对象
	response = make_response(redirect(url_for('home.index')))
	
	# 检查cookie中是否存在user_id
	if 'user_id' in request.cookies:
		# 获取cookie中的用户ID
		singed_user_id = request.cookies.get('user_id')
		# 对用户ID进行解密
		user_id = current_app.serializer.loads(singed_user_id).get('user_id')
		# 删除session中的用户ID
		session.pop(user_id, None)
		# 删除cookie中的用户ID
		response.delete_cookie('user_id')
	return response


@user_bp.route('/profile', methods=['GET', 'POST'], endpoint='profile')
@login_required
def profile():
	# 获取二级分类
	second_level_categories = g.second_level_categories
	# 获取当前登录用户
	user = g.user
	# 获取用户的详细信息
	user_info = UserInfo.query.filter_by(user_id=user.id).first()
	return render_template('user/profile.html', user=user, user_info=user_info,second_level_categories=second_level_categories)



@user_bp.route('/update_user_info', methods=['GET', 'POST'], endpoint='update_user_info')
@login_required
def update_user_info():
	# 获取二级分类
    second_level_categories = g.second_level_categories
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        realname = request.form.get('realname')
        sex = request.form.get('sex')
        age = request.form.get('age')
        icon = request.files.get('icon')  # FileStorage对象, 用于上传文件
        user_content=request.form.get('user_content')
		
		
        # 获取当前登录用户
        user = g.user
        # 获取当前登录用户的详细信息
        userinfo = UserInfo.query.filter_by(user_id=user.id).first()

        # 检查用户名、手机号、邮箱是否已存在
        def check_exists(field, value, error_msg):
            if value:
                # getattr() 函数用于返回一个对象属性值。
                if User.query.filter(getattr(User, field) == value, User.id != user.id).first():
                    return error_msg
            return None

        for field, value, error_msg in [
            ('username', username, '用户名已存在'),
            ('phone', phone, '手机号已存在'),
            ('email', email, '邮箱已存在')
        ]:
            error_msg = check_exists(field, value, error_msg)
            if error_msg:
                return render_template('user/profile.html', user=user,
                                       user_info=userinfo, profile_error_msg=error_msg, second_level_categories=second_level_categories)
	  
	    # 允许上传的文件类型
        if icon:
            icon_name = icon.filename
            # 获取文件后缀
            
            minio_file_path, error_msg = upload_file(icon, user.id, current_app.config['IMAGE_ALLOWED_EXTENSIONS'])
            if error_msg:
                return render_template('user/profile.html',
                                       user=user, profile_error_msg=error_msg,
                                       second_level_categories=second_level_categories)
            
            # 删除minio保存的照片。
            if user.icon:
	            flask_bucket.remove_file(user.icon)
		
        # 更新用户信息
        user.username = username if username else user.username
        user.phone = phone if phone else user.phone
        user.email = email if email else user.email
        user.icon = minio_file_path if icon else user.icon

        if userinfo:
            userinfo.realname = realname if realname else userinfo.realname
            userinfo.sex = sex if sex else userinfo.sex
            userinfo.age = age if age else userinfo.age
            userinfo.content=user_content if user_content else userinfo.content
        else:
            # 如果userinfo不存在，则创建一个。
            userinfo = UserInfo(user_id=user.id, realname=realname, sex=sex, age=age)
        try:
            # 保存到数据库
            db.session.add(user)
            db.session.add(userinfo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template('user/profile.html',
                                   user=user, user_info=userinfo, profile_error_msg=f'更新失败: {str(e)}', second_level_categories=second_level_categories)
        # 重定向到个人资料页
        return redirect(url_for('user.profile'))

    # get请求，用于更新用户信息
    return redirect(url_for('user.profile'))




@user_bp.route('/publish_article', methods=['GET', 'POST'], endpoint='publish_article')
@login_required
def publish_article():
	user = g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	third_level_categories = g.third_level_categories
	
	if request.method == 'POST':
		title = request.form.get('article_title')
		content = request.form.get('article_content')
		type_id = request.form.get('type_id',type=int)
		if not all([title, content, type_id]):
			return render_template('user/add_article.html', error_article_msg='标题和内容、分类不能为空', user=user,
			                       second_level_categories=second_level_categories,
			                       third_level_categories=third_level_categories)
		
		# 将文章保存到数据库数据库
		article = Article(title=title, content=content, user_id=user.id, type_id=type_id)
		try:
			db.session.add(article)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return render_template('user/add_article.html', error_article_msg='文章发布失败', user=user,
			                       second_level_categories=second_level_categories,
			                       third_level_categories=third_level_categories)
		return redirect(url_for('home.index'))
	
	return render_template('user/add_article.html', user=user,
	                       second_level_categories=second_level_categories,
	                       third_level_categories=third_level_categories)


@user_bp.route('/user_article_list', methods=['GET'], endpoint='user_article_list')
@login_required
def user_article_list():
	
	# 获取当前登录用户
	user = g.user
	
	# 获取页码
	page = request.args.get('page', 1, type=int)
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	# 分页查询当前用户的文章
	pagination = (Article.query.filter_by(user_id=user.id,is_deleted=False)
	              .join(ArticleType)
	              .with_entities(
						Article.id,
						Article.title,
						func.substr(Article.content, 1, 100).label('content'),
		                Article.read_count,
		                Article.collect_count,
		                Article.comment_count,
		                Article.like_count,
		                Article.comment_status,
		                Article.user_id,
		                Article.type_id,
						Article.publish_time,
						ArticleType.type_name.label('article_type_name')  # 获取文章分类名字
					)
	              .order_by(Article.publish_time.desc()).paginate(page=page, per_page=10))
	
	# 返回文章列表页
	return render_template('user/user_article_list.html',
	                       second_level_categories=second_level_categories,
	                       user=user, pagination=pagination)

@user_bp.route('/user_change_article', methods=['GET', 'POST'], endpoint='user_change_article')
@login_required
def user_change_article():
	# 获取当前登录用户
	user=g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	third_level_categories = g.third_level_categories
	
	if request.method == 'POST':
		# 获取表单数据
		
		article_id=request.form.get('article_id')
		title = request.form.get('article_title')
		content = request.form.get('article_content')
		type_id = request.form.get('type_id', type=int)
		
		current_article = Article.query.filter(Article.id == article_id,Article.is_deleted == False).first()
		
		if not all([title, content, type_id]):
			return render_template('user/change_article.html', error_article_msg='标题和内容、分类不能为空', user=user,
			                       second_level_categories=second_level_categories,
			                       third_level_categories=third_level_categories,
			                       article=current_article)
		
		# 更新文章
		current_article.title = title
		current_article.content = content
		current_article.type_id = type_id
		try:
			db.session.add(current_article)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return render_template('user/change_article.html', error_article_msg='文章更新失败', user=user,
			                       second_level_categories=second_level_categories,
			                       third_level_categories=third_level_categories,
			                       article=current_article)
		return redirect(url_for('user.user_article_list'))
	
	# 获取文章ID
	article_id = request.args.get('article_id', type=int)
	# 获取当前文章详情
	current_article = Article.query.filter(Article.id == article_id,Article.is_deleted==False).first()
	return render_template('user/change_article.html',
	                       user=user,second_level_categories=second_level_categories,
	                       third_level_categories=third_level_categories,
	                       article=current_article)
	

@user_bp.route('/delete_article', methods=['GET'], endpoint='delete_article')
@login_required
def delete_article():
	# 获取当前登录用户
	user=g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	# 获取参数
	article_id = request.args.get('article_id')
	
	article=Article.query.filter(Article.id==article_id,Article.user_id==user.id).first()
	if article:
		article.is_deleted=True
		db.session.add(article)
		db.session.commit()
	
	return redirect(url_for('user.user_article_list'))


@user_bp.route('/upload_album', methods=['GET', 'POST'], endpoint='upload_album')
@login_required
def upload_album():
	# 获取当前登录用户
	user = g.user
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	if request.method == 'POST':
		# 获取上传图片
		album = request.files.get('album_file')  # FilesStorage对象，用于上传文件
		album_name = request.form.get('album_name')
		description = request.form.get('description')
		
		if not album:
			return render_template('user/add_album.html',
			                       user=user, album_error_msg='文件不存在',
			                       second_level_categories=second_level_categories)
		
		# 使用封装的函数上传文件
		minio_file_path, error_msg = upload_file(album, user.id, current_app.config['IMAGE_ALLOWED_EXTENSIONS'])
		
		if error_msg:
			return render_template('user/add_album.html',
			                       user=user, album_error_msg=error_msg,
			                       second_level_categories=second_level_categories)
		
		user.albums.append(UserAlbum(name=album_name, path=minio_file_path, description=description))
		
		# 保存到数据库
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			# 删除刚才上传的图片
			flask_bucket.remove_file(minio_file_path)
			return render_template('user/add_album.html', user=user, profile_error_msg=f'更新失败: {str(e)}',
			                       second_level_categories=second_level_categories)
		
		# 重定向到个人资料页
		return redirect(url_for('user.user_album_list'))
	
	return render_template('user/add_album.html',
	                       user=user, second_level_categories=second_level_categories)

	
@user_bp.route('/user_album_list', methods=['GET'], endpoint='user_album_list')
@login_required
def user_album_list():
	# 获取当前登录用户
	user = g.user
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	# 分页查询当前用户的相册
	pagination = UserAlbum.query.filter_by(user_id=user.id).order_by(UserAlbum.album_datetime.desc()).paginate(page=1, per_page=10)
	
	return render_template('user/user_album_list.html',second_level_categories=second_level_categories,
	                       user=user, pagination=pagination)


@user_bp.route('/user_change_album', methods=['GET', 'POST'], endpoint='user_change_album')
@login_required
def user_change_album():
	# 获取当前登录用户
	user = g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	if request.method == 'POST':
		# 获取表单数据
		album_id=request.form.get('album_id')
		album_name = request.form.get('album_name')
		description = request.form.get('description')
		album = request.files.get('album_file')
	
		# 更新相册信息
		user_album = UserAlbum.query.filter(UserAlbum.id == album_id, UserAlbum.user_id == user.id).first()
		# 只更新表单中有的数据
		user_album.name = album_name if album_name else user_album.name
		user_album.description = description if description else user_album.description
		if album:
			# 删除原来的图片
			flask_bucket.remove_file(user_album.path)
			# 上传新的图片
			minio_file_path, error_msg = upload_file(album, user.id, current_app.config['IMAGE_ALLOWED_EXTENSIONS'])
			if error_msg:
				return render_template('user/change_album.html', user=user, album=user_album, album_error_msg=error_msg,
				                       second_level_categories=second_level_categories)
			user_album.path = minio_file_path
		try:
			db.session.add(user_album)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			if minio_file_path:
				# 假如album存在并上传了，才删除刚才上传的图片
				flask_bucket.remove_file(minio_file_path)
			return render_template('user/change_album.html', user=user, album=user_album, album_error_msg=f'更新失败: {str(e)}',
			                       second_level_categories=second_level_categories)
		return redirect(url_for('user.user_album_list'))
		
	album_id = request.args.get('album_id')
	# 获取当前相册详情
	current_album = UserAlbum.query.filter(UserAlbum.id == album_id, UserAlbum.user_id == user.id).first()
	return render_template('user/change_album.html',
	                       user=user, album=current_album,second_level_categories=second_level_categories)

@user_bp.route('/delete_album', methods=['GET'], endpoint='delete_album')
@login_required
def delete_album():
	# 获取当前登录用户
	user=g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	# 获取参数
	album_id = request.args.get('album_id')
	album=UserAlbum.query.filter(UserAlbum.id==album_id,UserAlbum.user_id==user.id).first()
	if album:
		flask_bucket.remove_file(album.path)
		db.session.delete(album)
		db.session.commit()
	return redirect(url_for('user.user_album_list'))

# 关于用户的介绍
@user_bp.route('/about_me', methods=['GET'], endpoint='about_me')
@login_required
def about_me():
	# 获取当前登录用户
	user = g.user
	
	# 获取二级分类
	second_level_categories = g.second_level_categories
	
	return render_template('user/about_me.html', user=user,second_level_categories=second_level_categories)