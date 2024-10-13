from collections import OrderedDict

from contents.models import ContentCategory
from goods.models import GoodsChannel

def get_categories():
    """获取商品分类"""
    # {
    #     "1": {
    #         "channels": [
    #             {"id": 1, "name": "手机", "url": "http://shouji.jd.com/"},
    #             {"id": 2, "name": "相机", "url": "http://www.itcast.cn/"}
    #         ],
    #         "sub_cats": [
    #             {
    #                 "id": 38,
    #                 "name": "手机通讯",
    #                 "sub_cats": [
    #                     {"id": 115, "name": "手机"},
    #                     {"id": 116, "name": "游戏手机"}
    #                 ]
    #             },
    #             {
    #                 "id": 39,
    #                 "name": "手机配件",
    #                 "sub_cats": [
    #                     {"id": 119, "name": "手机壳"},
    #                     {"id": 120, "name": "贴膜"}
    #                 ]
    #             }
    #         ]
    #     },
    #     "2": {
    #         "channels": [],
    #         "sub_cats": []
    #     }
    # }
    categories=OrderedDict()
    # 查询所有的商品频道，1比1对应37个一级类别
    # 按照group_id和sequence对GoodsChannel表中的数据进行排序。
    good_channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历所有频道
    for channel in good_channels:
        # 获取当前频道所在的组
        channel_group_id = channel.group_id

        # 构造数据基本框架，共11组的频道组
        if channel_group_id not in categories:
            categories[channel_group_id] = {'channels': [], 'sub_cats': []}

        category1 = channel.category  # 当前频道的一级类别

        # {"id": 1, "name": "手机", "url": "http://shouji.jd.com/"},
        categories[channel_group_id]['channels'].append(
            {"id": category1.id, "name": category1.name, "url": channel.url})
        # 查询二级
        for category2 in category1.subs.all():
            # 在面向对象过程中增加sub_cats属性，jinja2认识模型类对象
            # 给二级类别添加一个保存三级类别的列表
            category2.sub_cats = []
            # 查询三级类别
            for category3 in category2.subs.all():
                category2.sub_cats.append(category3)
            # 将二级类别添加到一级类别sub_cat钟
            categories[channel_group_id]['sub_cats'].append(category2)

    return categories

def get_content():
    # 第一步：查询所有广告类别
    contents = OrderedDict()
    contentCategory_list = ContentCategory.objects.all()
    for contentCategory in contentCategory_list:
        # 查询未下架的广告并排序
        content_list=contentCategory.content_set.filter(status=True).order_by('sequence')
        contents[contentCategory.key]=content_list

    return contents


def get_breadcrumb(category):
    """
     获取面包屑导航
    :param category:商品类别
    :return:面包屑导航字典
    """
    breadcrumb = dict(
        cat1='',
        cat2='',
        cat3='',
        cat1url='',
    )
    # 当前类别为一级类别
    if category.parent is None:
        # 当前类别为一级类别
        breadcrumb['cat1'] = category
        breadcrumb['cat1url']=category.goodschannel_set.all()[0].url
    elif category.subs.count() == 0:
        # 当前类别为三级
        breadcrumb['cat3'] = category
        cat2 = category.parent
        breadcrumb['cat2'] = cat2
        breadcrumb['cat1'] = cat2.parent
        breadcrumb['cat1url']=cat2.parent.goodschannel_set.all()[0].url
    else:
        # 当前类别为二级
        breadcrumb['cat2'] = category
        breadcrumb['cat1'] = category.parent
        breadcrumb['cat1url']=category.parent.goodschannel_set.all()[0].url
    return breadcrumb