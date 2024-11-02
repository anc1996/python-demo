#!/user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, backref

from extends import db
class Student(db.Model):
    """学生信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "db_students_1"
    # 字段定义
    
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
    name:Mapped[str] = mapped_column(db.String(15), comment="姓名")
    age:Mapped[int] = mapped_column(db.SmallInteger, comment="年龄")
    sex:Mapped[bool] = mapped_column(db.Boolean, default=True, comment="性别")
    email:Mapped[str] = mapped_column(db.String(128), unique=True, comment="邮箱地址")
    money:Mapped[float] = mapped_column(db.Numeric(10,2), default=0.0, comment="钱包")
    
    # # 第一种方式：在主表中声明关联属性
    # # 关联属性不是数据库的字段不会在数据表中出现，仅仅是SQLAlchemy为了方便开发者使用关联查询提供的对象属性
    # # info 可以代表与当前数据对应的外键模型对象
    # # 在主模型中声明关联属性
    # info = db.relationship("StudentInfo", uselist=False,backref="student")
    ## 一对多关系
    ## 从Student        查询  StudentAddress:  Student.address_list = []
    ## 从StudentAddress 查询  Student:         StudentAddress.student = 学生模型对象
    """
	    - lazy = 'subquery'，查询当前数据模型时，采用子查询(subquery)，把外键模型的属性也瞬间查询出来了。
	    - lazy = True或lazy = 'select'，查询当前数据模型时，不会把外键模型的数据查询出来，只有操作到外键关联属性时，才进行连表查询数据[执行SQL]
	    - lazy = 'dynamic'，查询当前数据模型时，不会把外键模型的数据查询出来，只有操作到外键关联属性并操作外键模型具体属性时，才进行连表查询数据[执行SQL]
    """
    # address_list=db.relationship("StudentAddress", backref="student", lazy="dynamic",uselist=True)
    # 多对多关系
    # grade_list=db.relationship("Grade", backref="student", lazy="dynamic",uselist=True)
    #  secondary 参数用于定义多对多关系中的中间表（关联表）。多对多关系通常涉及两个模型类，它们之间通过一个中间表来关联。
    #  secondary 参数允许你指定这个中间表的名称或模型类。
    
    def __repr__(self):
        return f"{self.name}<Student>"
        
    @property
    def to_dict(self):
        """把对象转化成字典"""
        return {
	        "id": self.id,
	        "name": self.name,
	        "age": self.age,
	        "sex": self.sex,
	        "email": self.email,
	        "money": float("%.2f" % self.money),
        }

class StudentInfo(db.Model):
    """学生信息附加表"""
    __tablename__ = "db_student_info_1"
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True, comment="主键")
    address:Mapped[str] = mapped_column(db.String(500), nullable=True, comment="默认地址")
    qq_num:Mapped[str] = mapped_column(db.String(15), nullable=True, comment="QQ号")
    ## 外键设置[默认创建数据库物理外键]
    user_id:Mapped[int] = mapped_column(db.ForeignKey("db_students_1.id"), comment="学生id")
    
    # 第二种方式：在附加表中声明关联属性
    # 模型属性，不是数据库的字段，不会在数据表中出现，仅仅是SQLAlchemy为了方便开发者使用关联查询所提供的对象属性
    # info 可以代表与当前数据对应的外键模型对象
    student = db.relationship("Student", backref=backref("info",uselist=False))
    

class StudentAddress(db.Model):
    """学生收货地址"""
    __tablename__ = "db_student_address_1"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, comment="主键")
    user_id: Mapped[int] = mapped_column(db.ForeignKey("db_students_1.id"), comment="学生id")
    province: Mapped[str] = mapped_column(db.String(20), comment="省份")
    city: Mapped[str] = mapped_column(db.String(20), comment="城市")
    area: Mapped[str] = mapped_column(db.String(20), comment="区县")
    address: Mapped[str] = mapped_column(db.String(200), comment="详细地址")
    
    # 第二种方式：在附加表中声明关联属性
    student=db.relationship("Student", uselist=False,
                            backref=backref("address_list", lazy="dynamic",uselist=True))
    
	

## 所有的模型必须直接或间接继承于db.Model
class Course(db.Model):
	
	"""课程数据模型"""
	__tablename__ = "db_course_1"
	
	id:Mapped[int] = mapped_column(db.Integer, primary_key=True, comment="主键")
	name:Mapped[str] = mapped_column(db.String(64), unique=True, comment="课程")
	price:Mapped[float] = mapped_column(db.Numeric(7, 2), comment="价格")
	
	# 第一种方式：在主表中声明关联属性
	# 多对多关系映射
	# grade_list=db.relationship("Grade", backref="course", lazy="dynamic",uselist=True)
	
	
	
	## repr()方法类似于django的__str__，用于打印模型对象时显示的字符串信息
	
	def __repr__(self):
		return f'{self.name}<Course>'


class Teacher(db.Model):
	"""老师数据模型"""
	__tablename__ = "db_teacher"
	id: Mapped[int] = mapped_column(db.Integer, primary_key=True, comment="主键")
	name: Mapped[str] = mapped_column(db.String(64), unique=True, comment="姓名")
	option: Mapped[str] = mapped_column(db.Enum("讲师", "助教", "班主任"), default="讲师", comment="职位")
	
	def __repr__(self):
		return f"{self.name}< Teacher >"
	
# 多对多关系:成绩
class Grade(db.Model):
	__tablename__ = "db_grade"
	
	id: Mapped[int] = mapped_column(db.Integer, primary_key=True, comment="主键")
	student_id: Mapped[int] = mapped_column(db.ForeignKey("db_students_1.id"), comment="学生id")
	course_id: Mapped[int] = mapped_column(db.ForeignKey("db_course_1.id"), comment="课程id")
	score: Mapped[float] = mapped_column(db.Numeric(5, 2), comment="成绩")
	time:Mapped[datetime]=mapped_column(db.DateTime,default=datetime.now,comment="考试时间")
	
	# 第2种：在附加表中声明关联属性
	student = db.relationship("Student", backref=backref("grade_list", lazy="dynamic",uselist=True))
	course = db.relationship("Course", backref=backref("grade_list", lazy="dynamic",uselist=True))
	
	def __repr__(self):
		return f"<Grade {self.id}>"