#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from io import BytesIO

from flask import session,render_template, request, jsonify, make_response, current_app, g,Blueprint
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from email_validator import validate_email, EmailNotValidError
from wtforms.validators import ValidationError

from apps.article.model import Article,ArticleType
from apps.user.model import User, UserInfo, UserAlbum
from apps.user.userForm import PhoneCodeLoginForm, UsernamePasswordLoginForm, RegisterForm, SendMsgForm, resetForm
from extends import db,cache
from extends.alisms.sms import Sample
from extends.file_function import upload_file
from extends.minio_bucket import flask_bucket
from extends.picture_verifycode.verify_code import generate_image
from extends.wangyisms.sms import wy_send_sms
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
	# 使用 email_validator 验证邮箱格式
	try:
		valid = validate_email(email)
		email = valid.email  # 规范化邮箱地址
	except EmailNotValidError as e:
		return jsonify({'exists': False, 'error_msg': str(e)})
	
	# 检查邮箱是否已存在
	user = User.query.filter_by(email=email).first()
	if user:
		return jsonify({'exists': False, 'error_msg': '邮箱已存在'})
	else:
		return jsonify({'exists': True})


from flask import flash, redirect, url_for

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            phone = form.phone.data
            email = form.email.data
            # 创建user对象
            user = User(username=username, password=password, email=email, phone=phone)
            # 将user对象添加到数据库
            db.session.add(user)
            db.session.commit()

            # 注册成功，跳转到个人资料页
            response = make_response(redirect(url_for('home.index')))
            # 设置cookie加密
            singed_user_id = current_app.serializer.dumps({'user_id': user.id})
            response.set_cookie('user_id', singed_user_id, max_age=60 * 60 * 24 * 7, httponly=True, secure=False)
            # 更新缓存
            cache.delete('view//')
            # session 用法
            session[user.id] = user.username
            return response
        else:
	        flash(form.errors, 'error')
	        return redirect(url_for('user.register'))
    return render_template('user/register.html', form=form)



@user_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    login_type = request.args.get('type')
    if login_type == 'username':
        form = UsernamePasswordLoginForm()
    elif login_type == 'phone':
        form = PhoneCodeLoginForm()
    else:
        return render_template('user/login.html', form=None, error_login_msg='请选择登录方式')

    if request.method == 'POST':
        if form.validate_on_submit():
	        # 根据登录方式获取用户
            user = User.query.filter_by(username=form.username.data).first() \
	                if login_type == 'username' \
	                else User.query.filter_by(phone=form.phone.data).first()
            # 创建响应对象并重定向到首页
            response = make_response(redirect(url_for('home.index')))
            singed_user_id = current_app.serializer.dumps({'user_id': user.id})
            response.set_cookie('user_id', singed_user_id, max_age=60 * 60 * 24 * 7, httponly=True, secure=False)
            session[user.id] = user.username
            # 更新缓存
            cache.delete('view//')
            return response
        else:
	        return render_template('user/login.html', form=form, error_login_msg=form.errors)

    return render_template('user/login.html', form=form)

@user_bp.route('/sendmsg', methods=['POST'], endpoint='sendmsg')
def sendmsg():
	form = SendMsgForm(request.form)
	if form.validate():
		phone = form.phone.data
		sms_provider = form.sms_provider.data
		
		# 发送验证码
		if sms_provider == 'netease':
			success, code = wy_send_sms(phone)
		elif sms_provider == 'ali':
			# 用阿里云发送验证码
			# 这里需要实现阿里云发送验证码的逻辑
			success, code = Sample.send_sms(phone)  # 示例代码，实际应替换为阿里云发送验证码的逻辑
		
		# 处理发送结果
		if success:
			# 状态200
			cache.set(phone, code, timeout=60)  # 60秒过期
			return jsonify({"sms_status": "短信发送成功", 'status': 200}), 200
		else:
			return jsonify({"sms_status": "短信发送失败", 'status': 500}), 500
	else:
		return jsonify({"sms_status": form.errors, 'status': 500}), 500


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
	# 创建响应对象并重定向到首页
	response = make_response(redirect(url_for('home.index')))
	
	# 检查cookie中是否存在user_id
	if 'user_id' in request.cookies:
		# 获取cookie中的用户ID
		singed_user_id = request.cookies.get('user_id')
		# 对用户ID进行解密
		user_id = current_app.serializer.loads(singed_user_id).get('user_id')
		# 删除session中的用户ID
		session.pop(user_id, default=None)
		# 删除cookie中的用户ID
		response.delete_cookie('user_id')
	
	# 删除首页缓存
	cache.delete('view//')
	return response


@user_bp.route('/profile', methods=['GET', 'POST'], endpoint='profile')
@login_required
def profile():
	# 获取当前登录用户
	user = g.user
	# 获取用户的详细信息
	user_info = UserInfo.query.filter_by(user_id=user.id).first()
	return render_template('user/profile.html', user=user, user_info=user_info)





@user_bp.route('/update_user_info', methods=['GET', 'POST'], endpoint='update_user_info')
@login_required
def update_user_info():
	
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
                                       user_info=userinfo, profile_error_msg=error_msg)
	  
	    # 允许上传的文件类型
        if icon:
            icon_name = icon.filename
            # 获取蓝图的名字
            # 返回上传文件的路径和错误信息
            minio_file_path, error_msg = upload_file(icon, user.id,
                                                     current_app.config['IMAGE_ALLOWED_EXTENSIONS'],'user/images','icon')
            if error_msg:
                return render_template('user/profile.html',
                                       user=user, profile_error_msg=error_msg)
            
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
                                   user=user, user_info=userinfo, profile_error_msg=f'更新失败: {str(e)}')
        # 重定向到个人资料页
        return redirect(url_for('user.profile'))

    # get请求，用于更新用户信息
    return redirect(url_for('user.profile'))




@user_bp.route('/publish_article', methods=['GET', 'POST'], endpoint='publish_article')
@login_required
def publish_article():
	# 获取当前登录用户
	user = g.user
	third_level_categories = g.third_level_categories
	
	if request.method == 'POST':
		title = request.form.get('article_title')
		content = request.form.get('article_content')
		type_id = request.form.get('type_id',type=int)
		if not all([title, content, type_id]):
			return render_template('user/add_article.html', error_article_msg='标题和内容、分类不能为空', user=user,
			                       third_level_categories=third_level_categories)
		
		# 将文章保存到数据库数据库
		article = Article(title=title, content=content, user_id=user.id, type_id=type_id)
		try:
			db.session.add(article)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			return render_template('user/add_article.html', error_article_msg='文章发布失败', user=user,
			                       third_level_categories=third_level_categories)
		return redirect(url_for('home.index'))
	
	return render_template('user/add_article.html', user=user,
	                       third_level_categories=third_level_categories)


@user_bp.route('/user_article_list', methods=['GET'], endpoint='user_article_list')
@login_required
def user_article_list():
	
	# 获取当前登录用户
	user = g.user
	
	# 获取页码
	page = request.args.get('page', 1, type=int)
	
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
	return render_template('user/user_article_list.html',user=user, pagination=pagination)

@user_bp.route('/user_change_article', methods=['GET', 'POST'], endpoint='user_change_article')
@login_required
def user_change_article():
	# 获取当前登录用户
	user=g.user
	# 获取当前登录用户的文章分类
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
			                       third_level_categories=third_level_categories,article=current_article)
		
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
			                       third_level_categories=third_level_categories,article=current_article)
		return redirect(url_for('user.user_article_list'))
	
	# 获取文章ID
	article_id = request.args.get('article_id', type=int)
	# 获取当前文章详情
	current_article = Article.query.filter(Article.id == article_id,Article.is_deleted==False).first()
	return render_template('user/change_article.html',
	                       user=user,third_level_categories=third_level_categories, article=current_article)
	

@user_bp.route('/delete_article', methods=['GET'], endpoint='delete_article')
@login_required
def delete_article():
	# 获取当前登录用户
	user=g.user
	
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
	if request.method == 'POST':
		# 获取上传图片
		album = request.files.get('album_file')  # FilesStorage对象，用于上传文件
		album_name = request.form.get('album_name')
		description = request.form.get('description')
		
		if not album:
			return render_template('user/add_album.html',user=user, album_error_msg='文件不存在')
		
		# 使用封装的函数上传文件
		minio_file_path, error_msg = upload_file(album, user.id, current_app.config['IMAGE_ALLOWED_EXTENSIONS'],'user/images','album')
		
		if error_msg:
			return render_template('user/add_album.html',user=user, album_error_msg=error_msg)
		
		user.albums.append(UserAlbum(name=album_name, path=minio_file_path, description=description))
		
		# 保存到数据库
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			# 删除刚才上传的图片
			flask_bucket.remove_file(minio_file_path)
			return render_template('user/add_album.html', user=user, profile_error_msg=f'更新失败: {str(e)}')
		
		# 重定向到个人资料页
		return redirect(url_for('user.user_album_list'))
	
	return render_template('user/add_album.html',
	                       user=user)

	
@user_bp.route('/user_album_list', methods=['GET'], endpoint='user_album_list')
@login_required
def user_album_list():
	# 获取当前登录用户
	user = g.user
	# 分页查询当前用户的相册
	pagination = UserAlbum.query.filter_by(user_id=user.id).order_by(UserAlbum.album_datetime.desc()).paginate(page=1, per_page=10)
	
	return render_template('user/user_album_list.html',user=user, pagination=pagination)


@user_bp.route('/user_change_album', methods=['GET', 'POST'], endpoint='user_change_album')
@login_required
def user_change_album():
	# 获取当前登录用户
	user = g.user
	
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
			minio_file_path, error_msg = upload_file(album, user.id, current_app.config['IMAGE_ALLOWED_EXTENSIONS'],'user/images','album')
			if error_msg:
				return render_template('user/change_album.html', user=user, album=user_album, album_error_msg=error_msg)
			user_album.path = minio_file_path
		try:
			db.session.add(user_album)
			db.session.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			if minio_file_path:
				# 假如album存在并上传了，才删除刚才上传的图片
				flask_bucket.remove_file(minio_file_path)
				
			return render_template('user/change_album.html', user=user, album=user_album, album_error_msg=f'更新失败: {str(e)}')
		return redirect(url_for('user.user_album_list'))
		
	album_id = request.args.get('album_id')
	# 获取当前相册详情
	current_album = UserAlbum.query.filter(UserAlbum.id == album_id, UserAlbum.user_id == user.id).first()
	return render_template('user/change_album.html',user=user, album=current_album)

@user_bp.route('/delete_album', methods=['GET'], endpoint='delete_album')
@login_required
def delete_album():
	# 获取当前登录用户
	user=g.user
	
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
	return render_template('user/about_me.html', user=user)


# 生成图片验证码
@user_bp.route('/image_code', methods=['GET'], endpoint='image_code')
def image_code():
	# 检查是否有之前的验证码session，如果有则删除
	if 'image_code' in session:
		session.pop('image_code', None)
	# 生成验证码
	image, code = generate_image(current_app.config['IMAGE_CODE_LENGTH'])
	# 将验证码图片转换为二进制
	buffer = BytesIO()  # BytesIO对象用于在内存中存储二进制数据
	image.save(buffer, 'JPEG')
	buffer_bytes = buffer.getvalue()
	
	# 将验证码保存到session中
	session['image_code'] = {
		'code': code,
		# 设置验证码的过期时间为5分钟
		'expiration': (datetime.now() + timedelta(minutes=5)).timestamp()
	}
	# 将验证码图片返回给客户端
	response = make_response(buffer_bytes)
	response.headers['Content-Type'] = 'image/jpeg'
	return response


@user_bp.route('/reset_password', methods=['GET', 'POST'], endpoint='reset_password')
@login_required
def reset_password():
    user = g.user
    restform = resetForm()

    if request.method == 'POST':
        if restform.validate_on_submit():
            old_password = restform.old_password.data
            new_password = restform.new_password.data
            try:
                # 检查旧的密码
                if not user.check_password(old_password):
                    raise ValidationError('旧密码不正确')
                # 更新密码
                user.password = new_password
                db.session.add(user)
                db.session.commit()
                # 重定向到首页
                return redirect(url_for('home.index'))
            except ValidationError as e:
                # 捕获 ValidationError 并返回错误信息
                reset_error_msg = str(e)
                return render_template('user/reset_password.html', reset_error_msg=reset_error_msg, restform=restform, user=user)

    return render_template('user/reset_password.html', restform=restform, user=user)
