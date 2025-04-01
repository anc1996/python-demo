from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""
    # 接收索引字段：使用文档定义索引字段，并且使用模板语法渲染
    # document=True:sku_text.txt ,
    # use_template=True:templates/search/indexes/goods/sku_text.txt
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        """返回建立索引的模型类"""
        return SKU
    # 返回内容context
    
    # query：搜索关键字
    # paginator：分页paginator的模型对象
    # page：当前页的page对象（遍历page中的对象，可以得到result对象）
    # result.objects: 当前遍历出来的SKU对象。
    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)