from datetime import datetime

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email, ValidationError, EqualTo
from apps.user.model import User
from extends import cache

class SendMsgForm(FlaskForm):
    """发送短信验证码表单"""
    phone = StringField('手机号', validators=[
        DataRequired(message='手机号不能为空'),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    sms_provider = SelectField('短信服务商', choices=[('netease', '网易短信'), ('ali', '阿里短信')], validators=[
        DataRequired(message='请选择短信服务商')
    ])
    
    class Meta:
        csrf = False
        
    def validate_phone(self, field):
        user = User.query.filter_by(phone=field.data).first()
        if not user:
            raise ValidationError('用户不存在')

    def validate_sms_provider(self, field):
        if field.data not in ['netease', 'ali']:
            raise ValidationError('请选择正确的短信服务商')

class UsernamePasswordLoginForm(FlaskForm):
    """用户名密码登录表单"""
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    submit = SubmitField('登录')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('用户名不存在')
        if user.is_deleted:
            raise ValidationError('用户已被删除,需要激活')
        if not user.check_password(self.password.data):
            raise ValidationError('密码错误')

class PhoneCodeLoginForm(FlaskForm):
    """手机验证码登录表单"""
    phone = StringField('手机号', validators=[
        DataRequired(message='手机号不能为空'),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    code = StringField('验证码', validators=[
        DataRequired(message='验证码不能为空'),
        Length(6, 6, message='验证码必须是6位数字')
    ])
    sms_provider = SelectField('短信服务商', choices=[('netease', '网易短信'), ('ali', '阿里短信')], validators=[DataRequired(message='请选择短信服务商')])
    submit = SubmitField('登录')

    def validate_phone(self, field):
        user = User.query.filter_by(phone=field.data).first()
        if not user:
            raise ValidationError('用户不存在')
        valid_code = cache.get(field.data)
        cache.delete(field.data)
        if self.code.data != valid_code:
            raise ValidationError('验证码错误')


class RegisterForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空')
    ])
    re_password = PasswordField('确认密码', validators=[
        DataRequired(message='确认密码不能为空')
    ])
    phone = StringField('手机号', validators=[
        DataRequired(message='手机号不能为空'),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='邮箱格式不正确')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('用户名已存在')

    def validate_phone(self, field):
        user = User.query.filter_by(phone=field.data).first()
        if user:
            raise ValidationError('手机号已存在')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('邮箱已存在')

    

class resetForm(FlaskForm):
    """重置密码"""
    # 原始密码
    old_password = PasswordField('原始密码',
                                 validators=[DataRequired(message='原始密码不能为空'),
                                             Length(6, 12, message='密码长度必须在6～12位之间')])
    # 新密码
    new_password = PasswordField('新密码',
                                 validators=[DataRequired(message='新密码不能为空'),
                                             Length(6, 12, message='密码长度必须在6～12位之间')])
    # 再次确认密码
    reset_password = PasswordField('重置密码',
                                   validators=[DataRequired(message='确认密码不能为空'),
                                               Length(6, 12, message='密码长度必须在6～12位之间'),
                                               EqualTo('new_password', message='两次密码不一致')])
    # 图形验证码
    recaptcha = StringField(label='图形验证码', validators=[DataRequired(message='验证码不能为空')])
    
    # 验证图形验证码
    def validate_recaptcha(self, field):
        input_code = field.data
        session_code_data = session.get('image_code')
        
        if not session_code_data:
            raise ValidationError('验证码已过期或未生成')
        
        session_code = session_code_data['code']
        
        
        if input_code.lower() != session_code.lower():
            session.pop('image_code', None)
            raise ValidationError('验证码错误')
        session.pop('image_code', None)
        
        
        
    # 验证旧密码与新密码不能相同
    def validate_new_password(self, field):
        if self.old_password.data == field.data:
            raise ValidationError('新密码不能与原始密码相同')