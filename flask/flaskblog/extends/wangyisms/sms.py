#!/user/bin/env python3
# -*- coding: utf-8 -*-
# !/user/bin/env python3
# -*- coding: utf-8 -*-

import hashlib,time,requests,random
from flask import current_app



def send_code(mobile, authCode):
	url = 'https://api.netease.im/sms/sendcode.action'
	"""
        AppKey	网易云信分配的账号，请替换你在管理后台应用下申请的Appkey
        Nonce	随机数（最大长度128个字符）
        CurTime	当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String)
        CheckSum	SHA1(AppSecret + Nonce + CurTime)，三个参数拼接的字符串，进行SHA1哈希计算，转化成16进制字符(String，小写)
    """
	AppKey = current_app.config['WANGYI_APP_KEY']
	# 生成128个长度以内的随机字符串
	nonce = hashlib.new('sha512', str(time.time()).encode("utf-8")).hexdigest()
	# 获取当前时间戳
	curtime = str(int(time.time()))
	# 网易云信的 App Secret
	AppSecret = current_app.config['WANGYI_APP_SECRET']
	# 根据要求进行SHA1哈希计算
	check_sum = hashlib.sha1((AppSecret + nonce + curtime).encode("utf-8")).hexdigest()
	
	header = {
		"AppKey": AppKey,
		"Nonce": nonce,
		"CurTime": curtime,
		"CheckSum": check_sum,
	}
	
	data = {
		'mobile': mobile,  # 手机号
		# 'codeLen': '6',  # 验证码长度，默认为 4 位，取值范围为 4-10 （注：语音验证码的取值范围为 4-8位）。
		'needUp': 'false',  # 是否需要支持短信上行。true: 需要，false: 不需要。
		'authCode': authCode  # 客户自定义验证码，长度为 4 ～ 10 位，支持字母和数字。如果设置了该参数，则codeLen参数无效
	}
	
	# 发送POST请求
	response = requests.post(url, data=data, headers=header)
	return response

# 生成随机六位数
def generate_code(phone):
	# 提取手机号的最后6位数字
	last_six_digits = phone[-6:]
	# 获取当前时间戳的最后6位数字
	timestamp_last_six_digits = str(int(time.time()))[-6:]
	# 结合手机号和时间戳随机生成验证码
	code = ''.join(random.sample(last_six_digits + timestamp_last_six_digits, 6))
	return code
	
def send_sms(phone):
	"""
		resp.content
		 Response:b'{"code":200,"msg":"2201","obj":"223333"}'
		msg 字段表示此次发送的sendid；obj 字段表示此次发送的验证码。
		code:200、315、403、414、416、500
			403	无权限	您的应用没有开通短信服务，请至 网易云信控制台 应用管理 > 产品功能 > 短信 查看是否已开启短信服务（欠费关停后需重新开启短信服务）
			414	客户端提交了非法参数	请检查对应参数是否合法，具体请参考返回的 msg。
			416	操作过于频繁	发送频率超过设置的频控，或设置了短信禁发国家。请至 网易云信控制台 应用管理 > 产品功能 > 短信 > 安全设置 查看频控和禁发国家（上限 25 条/天）。
	"""
	# 根据手机号以及时间，来生成6位随机验证码数字
	code=generate_code(phone)
	# 发送验证码
	response = send_code(phone, code)
	if response.status_code == 200:
		result = response.json()
		if result['code'] == 200:
			return True,code
		else:
			print("ERROR: ret.code=%s,msg=%s" % (result['code'], result['msg']))
			return False,code
	return False,code

if __name__ == '__main__':
	send_code("15775023056", '123456')  # 要发送的手机号
