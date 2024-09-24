#!/user/bin/env python3
# -*- coding: utf-8 -*-


class User:
	
	def __init__(self,username,password,phone):
		self.username=username
		self.password=password
		self.phone=phone
		
	def __str__(self):
		return self.username
	