import pickle,base64

from django_redis import get_redis_connection

from goods.models import SKU


def merge_cart_cookie_to_redis(request, user, response):
    """
    登录后合并cookie购物车数据到Redis
    :param request: 本次请求对象，获取cookie中的数据
    :param response: 本次响应对象，清除cookie中的数据
    :param user: 登录用户信息，获取user_id
    :return: response
    """
    # 获取cookie中的购物车数据
    cookie_cart_str = request.COOKIES.get('carts')
    if not cookie_cart_str: # 如果不存在不需要合并
        return response
    # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
    cookie_cart_dict = pickle.loads(base64.b64decode(cookie_cart_str.encode()))
    # 新增字典，保持sku_id:count、selected、unselected
    new_cart_dict={}
    # 新增一个列表，存放selected勾选的sku_id
    new_selected_true=[]
    # 新增一个列表，存放selected不勾选的sku_id
    new_selected_false = []
    # 遍历cookie_cart_dict的购物车数据
    for sku_id,sku_dict in cookie_cart_dict.items():
        if SKU.objects.filter(id=sku_id).exists():
            new_cart_dict[sku_id]=sku_dict['count']
            if sku_dict["selected"]:
                new_selected_true.append(sku_id)
            else:
                new_selected_false.append(sku_id)

    '''
    3.1 Redis数据库中的购物车数据保留。
    3.2 如果cookie中的购物车数据在Redis数据库中已存在，将cookie购物车数据覆盖Redis购物车数据。
    3.3 如果cookie中的购物车数据在Redis数据库中不存在，将cookie购物车数据新增到Redis。
    3.4 最终购物车的勾选状态以cookie购物车勾选状态为准。
    '''
    # 根据新的数据结构，合并的redis
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    pl.hmset('carts_%s' % user.id, new_cart_dict)
    if new_selected_true:
        pl.sadd('selected_%s' % user.id,*new_selected_true)
    if new_selected_false:
        pl.srem('selected_%s' % user.id,*new_selected_false)
    pl.execute()
    # 清除cookie
    response.delete_cookie('carts')
    return response