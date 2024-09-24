from datetime import datetime

from flask import Flask
from sqlalchemy.orm import load_only, contains_eager
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# 创建数据库对象
db=SQLAlchemy()
class Config(object):
    # 配置数据库的连接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.20.2:3306/toutiao'
    # 配置数据库的跟踪信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置数据库的调试信息
    SQLALCHEMY_ECHO = True # 打印时，显示查询的sql语句
    # FLASK的调试模式
    DEBUG = True

# 通过app.config.from_object()方法加载配置对象
app.config.from_object(Config)

db.init_app(app)


class User(db.Model):
    """
    用户基本信息
    """
    # 定义表名
    __tablename__='user_basic'

    # 定义状态常量
    class STATUS:
        ENABLE = 1
        DISABLE = 0

    # 定义字段
    id=db.Column('user_id',db.Integer,primary_key=True,doc='用户ID')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')

    mobile=db.Column(db.String,unique=True,doc='手机号')
    password=db.Column(db.String,doc='密码')
    name = db.Column('user_name',db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean,default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean,default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer,  default=0, doc='发布文章数量')
    fans_count = db.Column(db.Integer, default=0,  doc='粉丝数量')
    like_count = db.Column(db.Integer, default=0, doc='点赞数量')
    read_count = db.Column(db.Integer, default=0, doc='阅读数量')


    # profile是一个变量名，它代表了与UserProfile表之间的关系。不对应数据库中的字段，只是一个变量名，为了方便查询
    # 如果不做格外的配置，此方式的查询属于惰性查询，直到获取user.profile的时候才会真正的查询数据库.
    profile=db.relationship('UserProfile',uselist=False)
    # primaryjoin='User.id==Relation.user_id' 代表了关联关系的条件，即user表的id字段与relation表的user_id字段关联
    # uselist=True 代表了关联关系是一对多的关系
    followings=db.relationship('Relation',primaryjoin='User.id==foreign(Relation.user_id)',uselist=True)
    # primaryjoin='User.id==Relation.target_user_id' 代表了关联关系的条件，即user表的id字段与relation表的target_user_id字段关联
    #
    followers=db.relationship('Relation',primaryjoin='User.id==Relation.target_user_id',foreign_keys='Relation.target_user_id',uselist=True)
class UserProfile(db.Model):
    """
    用户详细信息
    """
    # 定义表名
    __tablename__='user_profile'

    class GENDER:
        # 0:男 1:女
        MALE = 0
        FEMALE = 1

    # 定义字段
    # ForeignKey 要传递的是表名.字段名
    id=db.Column('user_id',db.Integer,db.ForeignKey('user_basic.user_id'), primary_key=True,doc='用户ID')
    gender=db.Column(db.Integer,default=0,doc='性别')
    birthday = db.Column(db.Date,doc='生日')
    real_name=db.Column(db.String,doc='真实姓名')
    id_number=db.Column(db.String,doc='身份证号')
    id_card_front=db.Column(db.String,doc='身份证正面')
    id_card_back=db.Column(db.String,doc='身份证反面')
    id_card_handheld=db.Column(db.String,doc='手持身份证')
    ctime=db.Column('create_time',db.DateTime,default=datetime.now,doc='创建时间')
    # onupdate=datetime.now 更新时间
    utime=db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area=db.Column(db.String,doc='地区')
    company=db.Column(db.String,doc='公司')
    career=db.Column(db.String,doc='职业')
    education=db.Column(db.String,doc='学历')


class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        # 0:删除 1:关注 2:拉黑
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'),doc='用户ID')
    target_user_id = db.Column(db.Integer,db.ForeignKey('user_basic.user_id'), doc='目标用户ID')
    relation = db.Column(db.Integer, doc='用户间关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


    user=db.relationship('User',primaryjoin='Relation.target_user_id==foreign(User.id)',uselist=False)


@app.route('/')
def hello_world():  # put application's code here
    ret=User.query.all()
    print(ret)
    return "OK,user:{}".format(ret)

@app.route('/inner')
def inner():
    # SELECT *
    # FROM user_relation INNER JOIN user_basic ON user_relation.target_user_id = user_basic.user_id
        # WHERE user_relation.user_id = %s
    USER=Relation.query.join(Relation.user).options(load_only(Relation.user_id, Relation.target_user_id),
                                               contains_eager(Relation.user).load_only(User.name)).filter(
        Relation.user_id == 1).all()
    return "OK,user:{}".format(USER)



if __name__ == '__main__':
    app.run()

