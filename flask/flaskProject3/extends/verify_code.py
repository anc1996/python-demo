import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter


def get_random_color():
	"""
    生成一个随机的RGB颜色
    :return: 一个包含三个随机整数的元组，表示RGB颜色
    """
	return random.randint(120, 200), random.randint(120, 200), random.randint(120, 200)


def generate_image(length):
	"""
    生成一个包含随机验证码的图像
    :param length: 验证码的长度
    :return: 生成的图像对象和验证码字符串
    """
	s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	size = (130, 50)  # 图像的尺寸
	
	# 创建画布，背景颜色为白色
	im = Image.new('RGB', size, (250, 250, 250))
	font_path=os.path.join(os.path.dirname(__file__),'font/方正正中黑简体.ttf')
	# 创建字体对象，使用指定的字体文件和大小
	font = ImageFont.truetype(font_path, size=35)
	
	# 创建ImageDraw对象，用于在图像上绘制
	draw = ImageDraw.Draw(im)
	
	# 绘制验证码
	code = ''
	for i in range(length):
		c = random.choice(s)  # 从字符集中随机选择一个字符
		code += c  # 将字符添加到验证码字符串中
		# 在图像上绘制字符，位置随机偏移
		rand_len = random.randint(-5, 5)
		draw.text((130 * 0.2 * (i+1) + rand_len, 50 * 0.2 + rand_len),
		          text=c,
		          fill=get_random_color(),  # 字符颜色为随机颜色
		          font=font)
	
	# 绘制干扰线
	for i in range(8):
		x1 = random.randint(0, 130)  # 随机生成起点x坐标
		y1 = random.randint(0, 50 / 2)  # 随机生成起点y坐标
		
		x2 = random.randint(0, 130)  # 随机生成终点x坐标
		y2 = random.randint(50 / 2, 50)  # 随机生成终点y坐标
		
		draw.line(((x1, y1), (x2, y2)), fill=get_random_color())  # 绘制随机颜色的线条
	
	# 对图像进行边缘增强处理，增加图像的清晰度
	im = im.filter(ImageFilter.EDGE_ENHANCE)
	
	return im, code  # 返回生成的图像和验证码字符串


if __name__ == '__main__':
	generate_image(4)  # 生成一个长度为4的验证码图像
