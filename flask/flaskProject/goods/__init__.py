#!/user/bin/env python3
# -*- coding: utf-8 -*-


from flask import Blueprint



# 创建蓝图对象
goods_bp = Blueprint('goods', __name__)

# 从当前包中导入模块
from . import views