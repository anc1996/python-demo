#!/user/bin/env python3
# -*- coding: utf-8 -*-
from idlelib.pyparse import trans

from flask import Blueprint, jsonify

from apps.railway.model import Passenger, Train
from extends import db

railway_bp = Blueprint('railway', __name__, url_prefix='/railway')

@railway_bp.route('/railway_1', methods=['GET'])
def roles_1():
	# passenger1=Passenger(name="张三",age=20,sex="男")
	# passenger2=Passenger(name="李四",age=22,sex="女")
	# tran1=Train(train_name="G1234",train_type="高铁")
	# tran2=Train(train_name="D5678",train_type="动车")
	#
	# passenger1.tickets.append(tran1)
	# passenger1.tickets.append(tran2)
	#
	# # 添加到数据库
	# db.session.add(passenger1)
	# db.session.add(passenger2)
	# db.session.add(tran1)
	# db.session.add(tran2)
	# db.session.commit()
	
	passenger=Passenger.query.filter_by(name="张三").first()
	print(f'{passenger.tickets[0].train_name}')
	
	train=Train.query.filter_by(train_name="G1234").first()
	print(f'{train.passengers[0].name}')
	
	return 'OK'