#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func,select


from apps.article.model import Article,ArticleType
from apps.user.model import User
from extends import db
from extends.login_verify import get_user_id

# 创建蓝图对象,name参数是蓝图的名称，url_prefix参数是蓝图的URL前缀m,__name__是蓝图所在模块
article_bp = Blueprint('article', __name__, url_prefix='/article')


# 获取文章列表
@article_bp.route('/get_articles', methods=['GET'], endpoint='get_articles')
def get_articles():
	# 获取用户信息
	user,response=get_user_id()
	# 获取文章分类参数，页码
	type_id=request.args.get('type_id',type=int)
	page=request.args.get('page',1,type=int)
	# 获取文章分类名字
	article_typename = ArticleType.query.get(type_id).type_name
	articletype_dict={
		'type_id':type_id,
		 'typename':article_typename
	}
	
	# 获取二级分类
	second_level_categories = g.second_level_categories

	# 使用 in_ 方法查询所有属于这些 ArticleType 的文章
	pagination = (Article.query.filter(
					Article.type_id.in_(
						# 子查询，
						select(ArticleType.id).where(ArticleType.parent_id == type_id)
					),Article.is_deleted == False
				)
	            .join(User).join(ArticleType)
	            .with_entities(
						Article.id,
						Article.title,
						func.substr(Article.content, 1, 100).label('content'),
						Article.publish_time,
						Article.read_count,
						Article.collect_count,
						Article.comment_count,
						Article.like_count,
						Article.comment_status,
						Article.user_id,
						Article.type_id,
						User.username.label('author_name'),  # 获取作者名字
						ArticleType.type_name.label('article_type_name')  # 获取文章分类名字
				)
	            .order_by(Article.publish_time.desc())
	            .paginate(page=page, per_page=10))
	
	# pagination.items 获取当前页的数据
	# pagination.has_next 是否有下一页
	# pagination.has_prev 是否有上一页
	# pagination.next_num 下一页页码
	# pagination.prev_num 上一页页码
	# pagination.pages 总页数
	# pagination.page 当前页码
	# pagination.per_page 每页显示的数量
	# pagination.total 总记录数
	

	# 存在则显示user，不存在则显示None；
	return render_template('article/articles_list.html',
	                       pagination=pagination,second_level_categories=second_level_categories,
	                       user=user,articletype_dict=articletype_dict)


@article_bp.route('/article_detail', methods=['GET'], endpoint='article_detail')
def get_article_detail():
	# 获取用户信息
	user,response=get_user_id()
	# 获取二级分类
	second_level_categories = g.second_level_categories
	# 获取文章ID
	article_id=request.args.get('article_id',type=int)
	# 获取当前文章详情
	current_article=Article.query.filter(Article.id==article_id,Article.is_deleted == False).first()
	# 同时阅读数+1
	if current_article:
		current_article.read_count += 1
		try:
			# 提交
			db.session.add(current_article)
			db.session.commit()
		except SQLAlchemyError as e:
			# 回滚
			db.session.rollback()
			# 打印错误
			print(e)
		
		# 获取上一篇文章
		previous_article = Article.query.filter(Article.id < article_id,Article.is_deleted == False).with_entities(
							Article.id, Article.title
						).order_by(Article.id.desc()).limit(1).first()
		# 获取下一篇文章
		next_article = Article.query.filter(Article.id > article_id,Article.is_deleted == False).with_entities(
							Article.id, Article.title
						).order_by(Article.id.asc()).limit(1).first()
	
		# 获取三篇类型相同的文章
		related_articles = (Article.query.filter(
									Article.type_id == current_article.type_id,
									Article.id != article_id,
									Article.is_deleted == False)
								.with_entities(Article.id, Article.title)
		                        .order_by(Article.publish_time.desc()).limit(3).all())
		article_detail_data = {
			'current_article': current_article,
			'previous_article': previous_article,
			'next_article': next_article,
			'related_articles': related_articles
		}
		return render_template('article/article_detail.html',
		                       article_detail_data=article_detail_data, user=user,
		                       second_level_categories=second_level_categories)
	else:
		return '查询不到文章，404'
	
@article_bp.route('/article_like', methods=['GET'], endpoint='article_like')
def article_like():
	# 获取文章ID
	article_id = request.args.get('article_id')
	# 获取点赞标志
	like_flag = request.args.get('like_flag',type=int)
	# 判断是否是int型且在1和0之间
	if not article_id.isdigit() or int(like_flag) not in [0, 1]:
		return jsonify(love_error_msg='参数错误'), 400
	# 获取文章
	article = Article.query.get(article_id)
	if not article:
		return jsonify(love_error_msg='文章不存在'), 404
	if int(like_flag) == 0:
		article.like_count += 1
	else:
		article.like_count -= 1
	# 添加
	db.session.add(article)
	# 提交
	db.session.commit()
	return jsonify(like_count=article.like_count), 200
