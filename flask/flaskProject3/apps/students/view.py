#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.students.model import Student, StudentInfo, StudentAddress, Grade, Course
from extends import db

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/student_1', methods=['GET'])
def student_1():
    """添加数据"""
    ## 添加主表信息的时候通过关联属性db.relationship同步添加附件表信息
    # student = Student(
    #     name="xiaolan02",
    #     age=16,
    #     sex=False,
    #     money=10000,
    #     email="xiaolan02@qq.com",
    #     info = StudentInfo(address="北京市昌平区百沙路204号", qq_num="100861000")
    # )
    # db.session.add(student)
    # db.session.commit()

    ## 添加附加表数据，通过关联属性中db.relationshop的backref同步添加主表数据
    # info = StudentInfo(
    #     address="北京市昌平区百沙路114号",
    #     qq_num="101161220",
    #     student = Student(
    #         name="xiaoxin02",
    #         age=14,
    #         sex=True,
    #         money=10200,
    #         email="MONEY@qq.com",
    #     )
    # )
    #
    # db.session.add(info)
    # db.session.commit()

    """查询数据"""
    # 正向关联----> 从主模型查询外键模型
    student = Student.query.get(1)
    print(student.info) # <StudentInfo 1>
    print(student.info.address) # 北京市昌平区百沙路204号

    # 反向关联----> 从外键模型查询主模型
    student_info = StudentInfo.query.filter(StudentInfo.qq_num=="100861000").first()
    print(student_info.student) ##    xiaolan02<Student>
    print(student_info.student.name) ##  xiaolan02
    print(student_info.user_id) ## 2     仅仅获取了外键真实数据

    """修改数据"""
    # 通过主表使用关联属性可以修改附加表的数据
    # student = Student.query.get(2)
    # student.info.address = "广州市天河区天河东路103号"
    # db.session.commit()
    #
    # # 也可以通过附加表模型直接修改主表的数据
    # student_info = StudentInfo.query.filter(StudentInfo.qq_num == "100861000").first()
    # print(student_info.student)
    # student_info.student.age = 22
    # db.session.commit()

    return "ok"

@student_bp.route('/student_2', methods=['GET'])
def student_2():
    """添加数据"""
    ## 添加主表信息的时候通过关联属性db.relationship同步添加附件表信息
    # student = Student.query.get(2)
    # # student.address_list.append(StudentAddress(province="广东省", city="广州市", area="东华区", address="江东大路1号"))
    # db.session.add(StudentAddress(province="广东省", city="广州市", area="东华区", address="江东大路1号", student_id=2))
    # db.session.commit()
    
    ## 添加附加表数据，通过关联属性中db.relationshop的backref同步添加主表数据
    # studentaddress=StudentAddress(province="广东省", city="广州市", area="海珠区", address="海珠区江南大道")
    # studentaddress.student = Student.query.get(1)
    # db.session.add(studentaddress)
    # db.session.commit()
    
    """查询数据"""
    student = Student.query.get(2)
    address_list=student.address_list.all()
    print('地址',address_list)
    address=student.address_list[0].address
    print(address)
    return "ok"
    
@student_bp.route('/student_3', methods=['GET'])
def student_3():
    
    """添加数据"""
    # grade=Grade(
    #     student=Student.query.filter(Student.name=="xiaoxin02").first(),
    #     course=Course.query.filter(Course.name=="数学").first(),
    #     score=90
    # )
    # db.session.add(grade)
    # db.session.commit()
    
    
    """查询数据"""
    student=Student.query.filter(Student.name=="xiaoxin02").first()
    for grade in student.grade_list:
        print(f"课程：{grade.course.name}，成绩：{grade.score}")
    
    
    return 'OK'
