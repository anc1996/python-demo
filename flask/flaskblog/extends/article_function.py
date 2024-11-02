#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import g
from apps.article.model import ArticleType




def get_article_type_hierarchy():
	# 第一级分类
	first_level_categories = ArticleType.query.filter(ArticleType.parent_id == None).all()
	# 第二级分类
	second_level_categories = []
	for first_level in first_level_categories:
		second_level = ArticleType.query.filter(ArticleType.parent_id == first_level.id).all()
		if second_level:
			second_level_categories.append({first_level:second_level})
	
	# 第三级分类
	third_level_categories = []
	for second_level in second_level_categories:
		for key, value in second_level.items():
			for second in value:
				third_level = ArticleType.query.filter(ArticleType.parent_id == second.id).all()
				if third_level:
					third_level_categories.append({second:third_level})

	article_type_hierarchy = {
		'first_level_categories': first_level_categories,
		'second_level_categories': second_level_categories,
		'third_level_categories': third_level_categories
	}
	return article_type_hierarchy


def setup_global_hooks(app):
    @app.before_request
    def before_request():
        # 渲染任务栏内容
	    g.article_type_hierarchy = get_article_type_hierarchy()
	    g.second_level_categories = g.article_type_hierarchy.get('second_level_categories')
	    g.third_level_categories = g.article_type_hierarchy.get('third_level_categories')
