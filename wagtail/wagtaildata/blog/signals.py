#!/user/bin/env python3
# -*- coding: utf-8 -*-

# blog/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BlogPage
from .mongodb_utils import page_content_collection
from wagtail.search.backends import get_search_backend

@receiver(post_save, sender=BlogPage)
def page_saved(sender, instance, **kwargs):
    """页面保存后更新搜索索引"""
    try:
        search_backend = get_search_backend()
        search_backend.add(instance)
        print(f"页面 {instance.title} 已添加到搜索索引")
    except Exception as e:
        print(f"更新搜索索引失败: {e}")

@receiver(post_delete, sender=BlogPage)
def page_deleted(sender, instance, **kwargs):
    """页面删除后删除对应的MongoDB内容"""
    if hasattr(instance, 'mongo_content_id') and instance.mongo_content_id:
        try:
            page_content_collection.delete_one({'_id': instance.mongo_content_id})
            print(f"已从MongoDB删除内容: {instance.mongo_content_id}")
        except Exception as e:
            print(f"从MongoDB删除内容失败: {e}")