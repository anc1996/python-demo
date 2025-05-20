#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import BlogPage
from utils.mongo import MongoManager

@receiver(pre_delete, sender=BlogPage)
def delete_blog_content_from_mongodb(sender, instance, **kwargs):
    """当BlogPage被删除时，同步删除MongoDB中的内容"""
    if instance.mongo_content_id:
        try:
            mongo_manager = MongoManager()
            result = mongo_manager.delete_blog_content(instance.mongo_content_id)
            print(f"删除MongoDB内容 ID:{instance.mongo_content_id} - {'成功' if result else '失败'}")
        except Exception as e:
            import traceback
            print(f"删除MongoDB内容时出错: {e}")
            print(traceback.format_exc())