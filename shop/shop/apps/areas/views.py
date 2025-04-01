import logging

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from areas.constants import province_city_REDIS_EXPIRES
from areas.models import Area
from shop.utils.response_code import RETCODE

# 创建日志
logger=logging.getLogger('areas')


class AreasView(View):
    """省市区三级联动"""
    
    def get(self, request):
        """处理GET请求"""
        area_id = request.GET.get('area_id')
        
        if not area_id:
            # 查询省份数据
            return self._get_provinces()
        else:
            # 查询市或区的数据
            return self._get_sub_areas(area_id)
    
    def _get_provinces(self):
        """获取省份数据"""
        # 从缓存中读取省份数据
        province_list = cache.get('province_list')
        
        if not province_list:
            try:
                # 查询省级数据
                province_model_list = Area.objects.filter(parent__isnull=True)
                # 转换为字典列表
                province_list = [{'id': model.id, 'name': model.name} for model in province_model_list]
                # 缓存数据
                cache.set('province_list', province_list, province_city_REDIS_EXPIRES)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, "errmsg": '查询省份数据错误'})
        
        return JsonResponse({'code': RETCODE.OK, "errmsg": 'OK', "province_list": province_list})
    
    def _get_sub_areas(self, area_id):
        """获取市或区的数据"""
        # 从缓存中读取市或区数据
        sub_data = cache.get(f'sub_area_{area_id}')
        
        if not sub_data:
            try:
                # 查询市或区的父级模型
                parent_model = Area.objects.get(id=area_id)
                sub_model_list = parent_model.subs.all()
                
                # 转换为字典列表
                sub_list = [{'id': model.id, 'name': model.name} for model in sub_model_list]
                
                # 组织数据结构
                sub_data = {
                    "id": parent_model.id,
                    'name': parent_model.name,
                    'subs': sub_list
                }
                
                # 缓存数据
                cache.set(f'sub_area_{area_id}', sub_data, 3600)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, "errmsg": '查询市区数据错误'})
        
        return JsonResponse({'code': RETCODE.OK, "errmsg": 'OK', "sub_data": sub_data})