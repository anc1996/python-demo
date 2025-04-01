import base64,json,logging,pickle

from django.http import HttpResponseForbidden, JsonResponse
from django.views import View
from django.shortcuts import render
from django_redis import get_redis_connection

from goods.models import SKU
from shop.utils.response_code import RETCODE, err_msg

# Create your views here.
logger=logging.getLogger('carts')
class CartsView(View):
    """购物车管理"""
    def post(self,request):
        """将商品保存购物车"""
        # 接收和校验参数
        json_dict=json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count=json_dict.get('count')
        selected = json_dict.get('selected', True) # 可选

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': err_msg[RETCODE.NECESSARYPARAMERR]})
        
        # 判断count是否为数字
        try:
            count=int(count)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '参数count不是数字'})

        # 校验勾选是否是bool
        if selected and not isinstance(selected,bool): # 判断一个对象是否是一个已知的类型，
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '参数selected类型不对'})

        # 判断sku_id是否存在
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '商品不存在'})

        user=request.user
        # 判断用户是否登录
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 新增购物车数据，hincrby能判断sku_id是否存在，并自动累加
            # HINCRBY key field increment,为哈希表 key 中的域 field 的值加上增量 increment 。
            pl.hincrby('carts_%s'% user.id ,sku.id ,count )
            # 新增选中的状态，
            if selected:
                # SADD key member [member ...]
                # Redis Sadd 命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。
                pl.sadd('selected_%s' % user.id, sku.id)
            # 执行管道
            pl.execute()
            return JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})
        else:
            # 用户未登录，操作cookie购物车
            # 获取cookie中获取cart的数据，判断是否由购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 如果有购物车数据，将字符串由b64解密后转成byte,最后在通过pickle转成字典
                cart_dict =pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict={}
            # 判断当前要添加的商品在cart_dict中是否存在
            if sku.id in cart_dict:
                # 如果存在，累加count
                count+=cart_dict[sku.id]['count']
            cart_dict[sku.id] = { 'count': count,'selected': selected}
            # 将字典转成bytes,用base64加密转成base64的byte类型。
            cookie_cart_str_bytes=base64.b64encode(pickle.dumps(cart_dict))
            # 最后将bytes转字符串转成字符串
            cookie_cart_str=cookie_cart_str_bytes.decode()
            # 响应结果并将购物车数据写入到cookie
            response=JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})
            response.set_cookie('carts', cookie_cart_str)
            return response

    def get(self, request):
        """展示购物车"""
        user = request.user
        # 1.查询cookies的购物车
        cart_str = request.COOKIES.get('carts')
        # 1.用户登录的后，将cookies购物车加入到redis购物车
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            redis_conn = get_redis_connection('carts')
            
            '''将cookie购物车的数据保存到redis'''
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                pl = redis_conn.pipeline()
                for sku_id in cart_dict:
                    # 获取sku_id和count
                    count = cart_dict[sku_id]['count']
                    selected = bool(cart_dict[sku_id]['selected'])
                    # 将购物车数据同步到redis
                    # 新增购物车数据
                    pl.hincrby('carts_%s' % user.id, sku_id, int(count))
                    # 新增选中的状态
                    if selected:
                        pl.sadd('selected_%s' % user.id, sku_id)
                    else:
                        pl.srem('selected_%s' % user.id, sku_id)
                # 执行管道
                pl.execute()
                
            # 查询hash数据,HGETALL key,命令用于返回存储在 key 中的哈希表中所有的域和值。
            redis_cart_dict=redis_conn.hgetall('carts_%s'% user.id)
            # 查询set数据,SMEMBERS key命令返回存储在 key 中的集合的所有的成员。 不存在的集合被视为空集合。
            set_selected_list=redis_conn.smembers('selected_%s' % user.id)
            
            # 删除redis中selected不存在的sku_id
            pl = redis_conn.pipeline()
            for selected_skuid in set_selected_list:
                if selected_skuid not in redis_cart_dict.keys():
                    pl.srem('selected_%s'% user.id,selected_skuid)
            # 执行管道
            pl.execute()
            
            # 将redis中的数据构造成跟cookie中的格式一致，方便统一查询
            '''{
                "sku_id1": {
                    "count": "1",
                    "selected": "True"
                },
                ...
            }'''
            cart_dict = {}
            for sku_id,count in redis_cart_dict.items():
                # 判断SKU是否存在
                if SKU.objects.filter(id=sku_id).exists():
                    try:
                        cart_dict[int(sku_id)] = {'count': int(count), 'selected': sku_id in set_selected_list}
                    except ValueError:
                        # 如果转换失败，打印错误信息并跳过当前循环
                        print(f"Error converting to int: sku_id={sku_id}, count={count}")
                        continue
                else:
                    pl = redis_conn.pipeline()
                    # 如果sku_id不存在，删除sku_id
                    pl.hdel('carts_%s'% user.id,sku_id) # hdel用法：Delete ``keys`` from hash ``name``
                    # 如果sku_id不存在，删除sku_id
                    pl.srem('selected_%s'% user.id,sku_id) # srem用法：Remove ``values`` from set ``name``
                    pl.execute()
        else:
            # 用户未登录，查询cookie购物车
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict =pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict={}
                
        # 2.构造购物车渲染数据
        '''
        [{sku1数据1},{sku数据2}]
        '''
        sku_ids = cart_dict.keys()
        # in在一个给定的可迭代对象中；通常是一个列表、元组或查询集。这不是一个常见的用例，但字符串（可迭代）是可以接受的。
        # 等价于sql:SELECT ... WHERE id IN (1, 3, 4);
        skus = SKU.objects.filter(id__in=sku_ids)
        # 如果sku_id不在数据库删除redis的is
        cart_skus = []
        for sku in skus:
            cart_skus.append({
            'id':sku.id,'name': sku.name,
            'count': cart_dict.get(sku.id).get('count'),
            'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，字符串转'True'，方便json解析
            'default_image_url': sku.default_image.url,
            'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
            'amount':str(sku.price * cart_dict.get(sku.id).get('count')),
            })
        context={'cart_skus':cart_skus}
        
        # 3.渲染到模板
        response = render(request, 'cart.html', context=context)
        # 用户已登录，清除cookie中的购物车数据
        if user.is_authenticated and cart_str:
            response.delete_cookie('carts')
        return response

    def put(self, request):
        """修改购物车数据"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': err_msg[RETCODE.NECESSARYPARAMERR]})

        # 判断count是否为数字
        try:
            count = int(count)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '参数count不是数字'})
        # 校验勾选是否是bool
        if selected and not isinstance(selected, bool):  # 判断一个对象是否是一个已知的类型，
                return JsonResponse({'code': RETCODE.ALLOWERR, 'errmsg': '参数selected类型不对'})
            
        # 判断sku_id是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '商品不存在'})


        user = request.user
        # 判断用户是否登录
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 由于后端收到的数据是最终的结果，直接覆盖
            pl.hset('carts_%s' % user.id, sku_id, count)
            # 是否选中
            if selected:
                # SADD key member [member ...]
                # Redis Sadd 命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                # SREM key member [member ...]
                # SREM 用于在集合中删除指定的元素。如果指定的元素不是集合成员则被忽略。
                # 如果集合 key 不存在则被视为一个空的集合，该命令返回0。
                pl.srem('selected_% s' % user.id, sku_id)
            pl.execute()
        else:
            # 用户未登录，操作cookie购物车
            # 获取cookie中获取cart的数据，判断是否由购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict =pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict={} # 如果没有购物车数据，创建一个空字典
                
            # 对当前内容直接覆盖，
            cart_dict[sku_id] = {'count': count, 'selected': selected}
            # 将字典转成bytes,再将bytes转成base64的bytes,
            cookie_str_bytes = base64.b64encode(pickle.dumps(cart_dict))
            # 最后将bytes转字符串转成字符串
            cookie_cart_str = cookie_str_bytes.decode()

        # 3.渲染模板
        cart_sku = {
            'id': sku_id,
            'count': count,
            'selected': selected,
            'name': sku.name,
            'default_image_url': sku.default_image.url,
            'price': sku.price,
            'amount': sku.price * count,
        }
        response = JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功','cart_sku':cart_sku})
        # 如果用户未登录，响应结果并将购物车数据写入到cookie
        if not user.is_authenticated:
            response.set_cookie('carts', cookie_cart_str)
        return response

    def delete(self, request):
        """删除购物车"""
        # 1.接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 2.判断sku_id是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '商品不存在'})

        # 3.判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，删除redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 删除键，就等价于删除了整条记录
            # HDEL key field [field ...]
            # Redis HDEL 命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。
            # 如果 key 粗存在，会被当作空哈希表处理并返回 0 。
            pl.hdel('carts_%s' % user.id, sku_id)
            # SREM key member [member ...]
            # SREM 用于在集合中删除指定的元素。如果指定的元素不是集合成员则被忽略。
            # 如果集合 key 不存在则被视为一个空的集合，该命令返回0。
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
        else:
            # 用户未登录，删除cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict =pickle.loads(base64.b64decode(cart_str.encode()))
                cart_dict.pop(sku_id, None)
                # 将字典转成bytes,再将bytes转成base64的bytes,
                cookie_str_bytes = base64.b64encode(pickle.dumps(cart_dict))
                # 最后将bytes转字符串转成字符串
                cart_str = cookie_str_bytes.decode()

        # 4.创建响应对象
        response = JsonResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})
        if not user.is_authenticated and cart_str:
            response.set_cookie('carts', cart_str)
        return response

class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 1.接收和校验参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)
        # 校验参数
        if selected and not isinstance(selected, bool):
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '参数selected类型不对'})

        # 2.判断用户是否登录
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            # 获取字典中的key，
            redis_sku_ids = redis_conn.hgetall('carts_%s' % user.id)
            # 判断用户是否全选
            if selected:
                # 全选
                redis_conn.sadd('selected_%s' % user.id, *redis_sku_ids)
            else:
                # 取消全选
                redis_conn.srem('selected_%s' % user.id, *redis_sku_ids)
        else:
            # 用户未登录，删除cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                for sku_id in cart_dict:
                    cart_dict[sku_id]['selected']=selected
                # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串转成字符串
                cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()

        # 3.渲染模板
        response = JsonResponse({'code': RETCODE.OK, 'errmsg': '全选购物车成功'})
        # 写入cookie
        if not user.is_authenticated:
                response.set_cookie('carts', cookie_cart_str)
        return response


class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        
        # 1、判断用户是否登录
        '''
                {
            "code":"0",
            "errmsg":"OK",
            "cart_skus":[
                {
                    "id":1,
                    "name":"Apple MacBook Pro 13.3英寸笔记本 银色",
                    "count":1,
                    "default_image_url":"http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429"
                },
                ......
            ]
        }
        :param request:
        :return:
        '''
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection('carts')
            # 获取字典中说要sku的id
            redis_sku_ids = redis_conn.hgetall('carts_%s' % user.id)
            # 查询set数据,SMEMBERS key命令返回存储在 key 中的集合的所有的成员。 不存在的集合被视为空集合。
            set_selected_list = redis_conn.smembers('selected_%s' % user.id)
            cart_dict = {}
            for sku_id, count in redis_sku_ids.items():
                cart_dict[int(sku_id)] = {'count': int(count), 'selected': sku_id in set_selected_list}
        else:
            # 用户未登录，查询cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
        
        # 2、构造购物车渲染数据
        '''
        [{sku1数据1},{sku数据2}]
        '''
        sku_ids = cart_dict.keys()
        # in在一个给定的可迭代对象中；通常是一个列表、元组或查询集。这不是一个常见的用例，但字符串（可迭代）是可以接受的。
        # 等价于sql:SELECT ... WHERE id IN (1, 3, 4);
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id, 'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'default_image_url': sku.default_image.url,
            })
        # 响应json列表数据
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'cart_skus': cart_skus})

