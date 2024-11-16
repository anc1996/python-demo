#!/user/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from extends.minio_bucket import flask_bucket


def upload_file(file, user_id, allowed_extensions,save_path,tpye):
	"""
	上传文件
	:param file: 文件对象
	:param user_id: 用户id
	:param allowed_extensions: 支持什么类型
	:param save_path: 保存路径
	:param tpye: 存储类型
	:return:
	"""
	# 获取文件后缀
	suffix = file.filename.split('.')[-1]
	if suffix not in allowed_extensions:
		return None, '文件类型不支持'
	
	# 生成唯一的文件名，并与 user_id 关联
	unique_filename = f"{tpye}_{user_id}_{uuid.uuid4().hex}.{suffix}"
	# 配置路径
	# minio_file_path = f"images/user/photo/{unique_filename}"
	minio_file_path = f"{save_path}/{unique_filename}"
	# 上传文件
	flag = flask_bucket.flask_upload_file(bucket_file=minio_file_path, data=file)
	if not flag:
		return None, '文件上传失败'
	return minio_file_path, None