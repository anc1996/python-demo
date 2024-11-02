#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re

from flask import session
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class UserForm(FlaskForm):
	
	
	# 定义表单字段
	username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=12, message='用户名长度必须在6～12位之间')])
	password = PasswordField('密码',validators=[DataRequired(), Length(min=6, max=12, message='密码长度必须在6～12位之间')])
	repassword = PasswordField('确认密码',validators=[DataRequired(), Length(min=6,max=12, message='密码长度必须在6～12位之间'),
	                                                  EqualTo('password',message='两次密码不一致')])
	# 这里
	phone=StringField('手机号码',validators=[DataRequired(),Regexp(r'^1[3-9]\d{9}$',message='手机号格式错误')])
	icon=FileField('头像',validators=[FileRequired(message='请选择文件'),FileAllowed(['jpg','png','gif'],message='文件类型错误')])
	recaptcha=StringField(label='验证码')
	

	def validate_recaptcha(self,field):
		input_code=field.data
		session_code=session.get('image_code')
		# 同时删除session中的验证码
		session.pop('image_code')
		if input_code.lower()!=session_code.lower():
			raise ValueError('验证码错误')

		
	def validate_username(self,field):
		
		if field.data[0].isdigit():
			raise ValueError('用户名不能以数字开头')
		