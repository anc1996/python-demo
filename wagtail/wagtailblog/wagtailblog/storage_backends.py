#!/user/bin/env python3
# -*- coding: utf-8 -*-
# wagtailblog/storage_backends.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MinioMediaStorage(S3Boto3Storage):
    """Minio 存储后端用于媒体文件"""
    location = 'media'
    file_overwrite = False

class MinioDocumentStorage(S3Boto3Storage):
    """Minio 存储后端用于文档文件"""
    location = 'documents'
    file_overwrite = False

class MinioImageStorage(S3Boto3Storage):
    """Minio 存储后端用于图片文件"""
    location = 'images'
    file_overwrite = False

class MinioOriginalImageStorage(S3Boto3Storage):
    """Minio 存储后端用于原始图片文件"""
    location = 'original_images'
    file_overwrite = False

class MinioVideoStorage(S3Boto3Storage):
    """Minio 存储后端用于视频文件"""
    location = 'videos'
    file_overwrite = False