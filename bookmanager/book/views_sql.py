#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models.functions import Abs

from book.models import BookInfo,PeopleInfo
from django.db.models import *
from django.core.paginator import Paginator


"""
类似于 ipython的东西可以用来操作数据库
python manage.py shell
"""

#############################新增数据#####################################
# 方式1
# 要在python manage.py shell环境里，手动调用save方法
book=BookInfo(name='Python入门',pub_date='2000-01-01',readcount=4223,commentcount=1552)
# 需要手动调用save方法,“保存”必须是SQL插入或更新(或等效的)非sql后端)。通常，它们不应该被设置。
book.save()


# 方式2  要在python manage.py shell环境里，
# 直接入库
# objects 模型的管理类:对模型的增删改查都找objects
# 会把新生成的对象返回给我们
BookInfo.objects.create(name='java',readcount=2123,commentcount=552,pub_date='2010-1-1')


#############################修改(更新)数据#####################################
# 方式1
# 1.先查询数据
# select * from bookinfo where id=1
book1=BookInfo.objects.get(id=1)   #book: <BookInfo: 射雕英雄传>
#2. 直接修改实例的属性
book1.readcount=322
#3.调用save方法
book1.save()


# 方式2  直接更新
# filter 过滤
BookInfo.objects.filter(id=2).update(
    readcount=150,
    commentcount=300
)  # 成功返回：1,失败返回：0


##############################删除数据#####################################
#方式1
# 1. 先查询出数据
book2=BookInfo.objects.get(id=7)
#2.调用删除方法
book2.delete()

#方式2
book=BookInfo.objects.filter(id=8).delete() # 返回一个元组(删除的个数,字典{‘表名’:删除的个数})

###############################基本查询#####################################

# get  得到某一个数据
# all  获取所有的
# count 个数

#select * from bookinfo where id=1
# 返回一个单一对象
book3=BookInfo.objects.get(id=1)
#查询id 不存在的数据会抛出异常
try:
    book=BookInfo.objects.get(id=100)   # raise self.model.DoesNotExist
except BookInfo.DoesNotExist:
    print('查询的数据不存在')

# 返回所有结果,返回所有结果的列表
booklist=BookInfo.objects.all()

# count
# 先进行数据库查询，然后对查询结果进行计数
count=BookInfo.objects.all().count()
# 直接使用数据库的COUNT函数进行计数，因此后者可能更高效。
count=BookInfo.objects.count()

###############################filter,get,exclude#####################################
"""
    select * from bookinfo where 条件语句
    相当于 where查询
    filter(*args, **kwargs) : 筛选/过滤 返回 n个结果 (n = 0/1/n)，返回一个新的 QuerySet，其中包含与给定查找参数相匹配的对象。
    get                     : 返回1个结果
    exclude         : 排除掉符合条件剩下的结果  相当于 not，返回一个新的 QuerySet，其中包含与给定查找参数不匹配的对象。
    例如：
    Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline="Hello")
    用 SQL 术语来说，它的值是：SELECT ...  WHERE NOT (pub_date > '2005-1-3' AND headline = 'Hello')
    语法形式:
        以filter(字段名__运算符=值) 为例
"""
# get返回单一对象，查询编号为1的图书
book=BookInfo.objects.get(id=1)  #
#filter返回的是一个列表
books=BookInfo.objects.filter(id=1)
# exact:完全匹配id=1
books=BookInfo.objects.filter(id__exact=1)
print(book[0])
# exclude:排除掉符合条件剩下的结果  相当于 not
books=BookInfo.objects.exclude(id__exact=1)


# 查询书名包含'j'的图书
# name_contains包含,相对sql语句中的LIKE '%j%',
books=BookInfo.objects.filter(name__contains='J') # 区分大小写
books=BookInfo.objects.filter(name__icontains='J') #忽略大小写
# name__endswith以’a‘结尾的书名
books=BookInfo.objects.filter(name__endswith='A') # 区分大小写
books=BookInfo.objects.filter(name__iendswith='A')  #忽略大小写

# 查询书名为空的图书
books=BookInfo.objects.filter(name__isnull=True)
# 查询编号为1或3或5的图书
books=BookInfo.objects.filter(id__in=[1,3,5])

'''
    gt:greater than   gte:greater than or equal to
    lt:less than      lte:less than or equal to
    e:equal
'''
# 查询编号大于3的图书,
books=BookInfo.objects.filter(id__gt=3)
# 查询编号不等于3的图书
books=BookInfo.objects.exclude(id=3)# 返回列表
# 查询编号等于3的图书
books=BookInfo.objects.filter(id__exact=3)
# 不区分大小写的完全匹配java
books=BookInfo.objects.filter(name__iexact='Python')


#### 时间
# 查询1980年发表的图书
books=BookInfo.objects.filter(pub_date__year='1980')

# 查询1990年1月1日后发表的图书
books=BookInfo.objects.filter(pub_date__gt='1990-1-1')

# 对于日期和日期时间字段，精确的 ISO 8601 周号年份匹配。允许链接其他字段的查询。取整数年。
# 查询1990年发表的图书
books=BookInfo.objects.filter(pub_date__iso_year=1980)

# 查询12月发表的图书
books=BookInfo.objects.filter(pub_date__month=12)

# 查询1890年1月1日到2010年12月12日后发表的图书
books=BookInfo.objects.filter(pub_date__range=('1890-1-1','2010-12-12'))

# 查询2000年后发表的图书
books=BookInfo.objects.filter(pub_date__year__gt=2000)

# 查询01号发表的图书
books=BookInfo.objects.filter(pub_date__day=1)

# 查询星期号32发表的图书
books=BookInfo.objects.filter(pub_date__week=32)

# 查询第2季度发表的图书，取 1 到 4 之间的整数值，代表一年中的季度。
books=BookInfo.objects.filter(pub_date__quarter=2)

# regex：区分大小写的正则表达式匹配。查询含j**a的书名
books=BookInfo.objects.filter(name__regex='j.*a')
# iregex：不区分大小写的正则表达式匹配。查询含j**a的书名
books=BookInfo.objects.filter(name__iregex='J.*A')


############################   F(了解)         #####################################
# 使用F对象，被定义在django.db.models中,语法如下：F(属性名)
"""
首先导入包：from django.db.models import F
jango 使用 F() 对象来生成一个 SQL 表达式，在数据库层面描述所需的操作。
F() 对象表示模型字段的值、模型字段的转换值或注释列的值。它可以用于生成复杂的 SQL 表达式。
F对象的语法形式:filter(字段名__运算符=F('字段名'))
"""

# 查询id=1的图书的阅读量,对阅读量进行+1操作
book=BookInfo.objects.get(id=1)
book.commentcount=F('commentcount')+1
book.save()
# or
books=BookInfo.objects.filter(id__exact=2)
books.update(commentcount=F('commentcount')+1)

# 在过滤器中使用
# 查询阅读量大于等于评论量的图书。
books=BookInfo.objects.filter(readcount__gte=F('commentcount'))

#查询阅读量大于等于评论量2倍的图书
books=BookInfo.objects.filter(readcount__gte=F('commentcount')*2)

# 与注解一起使用
# 查询每本书的阅读量之间评论量大于100的
# annotate()函数会将这些值添加到返回的每个BookInfo对象中，你可以像访问普通属性一样访问这些注解值
books=BookInfo.objects.annotate(chazhi=Abs(F('readcount')-F('commentcount'))).filter(chazhi__gt=100 )
books[0].chazhi

# 对书本阅读量降排序
# nulls_last=True，那么在排序结果中，所有的空值（NULL）将会被放在最后，无论是升序还是降序排序。
books=BookInfo.objects.order_by(F('readcount').desc(nulls_last=True))

###############################Q对象(了解)#####################################

# 如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符，要导入：from django.db.models import Q
# 语法如下：Q(属性名__运算符=值)
"""
    一个 Q() 对象表示一个可以在与数据库相关的操作中使用的 SQL 条件。它类似于 F() 对象，它表示模型字段或注释的值。
    它们使得定义和重复使用条件成为可能，并可以使用操作符如 | （OR）、& （AND）和 ^ （XOR）来组合它们
    Q(字段名__运算符=值)
    或  Q()|Q() ..
    并且 Q()&Q() ..
    not  ~Q()
"""

# 需要查询id大于2 并且阅读量小于20的书籍
#
# 方式1:filter().filter()
books = BookInfo.objects.filter(id__gt=2).filter(readcount__lt=20)
# 方式2:filter(条件,条件)
books = BookInfo.objects.filter(id__gt=2, readcount__lt=20)
# 方式3
books=BookInfo.objects.filter(Q(id__gt=2) & Q(readcount__lt=20))

# 需要查询id大于2 或者 阅读量大于20的书籍
books = BookInfo.objects.filter(Q(id__gt=2) | Q(readcount__gt=20))
# 查询id大于2 或者 阅读量大于20的书籍,并且书名包含'三'
books=BookInfo.objects.filter((Q(id__gt=2)|Q(readcount__gt=20))&Q(name__contains='三'))
# 查询阅读量大于20的图书
books = BookInfo.objects.filter(Q(readcount__gt=20))
# 查询书籍id不为3
books = BookInfo.objects.filter(~Q(id=3))


###############################聚合函数(了解)#####################################
# 首先导入:from django.db.models import Avg,Sum
# 使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg平均，Count数量，Max最大，Min最小，Sum求和，
# 语法形式是: aggragte(Xxx('字段')) 返回一个字典,如果存在args，则表达式将作为参数传递Aggregate对象的默认别名。
# 当前数据的阅读总量
book_dist = BookInfo.objects.aggregate(Sum('readcount'))     # 返回字典：{'readcount__sum': 214}
# 当前数据的阅读平均量
book_dist = BookInfo.objects.aggregate(Avg('readcount'))
# 当前数据的数量
book_dist = BookInfo.objects.aggregate(Count('id'))
# 当前数据的最大数量
book_dist = BookInfo.objects.aggregate(Max('readcount'))
# 当前数据的最小数量
book_dist = BookInfo.objects.aggregate(Min('readcount'))


###############################排序#####################################
# 使用order_by对结果进行排序,返回列表
# 默认升序
books = BookInfo.objects.all().order_by('readcount')
# 降序
books = BookInfo.objects.all().order_by('-readcount')
# 查询阅读量大于30且小于300的图书,按阅读量降序
books=BookInfo.objects.filter(Q(readcount__gt=30)&Q(readcount__lt=300)).order_by('-readcount')
books=BookInfo.objects.filter(readcount__range=(30,300)).order_by('-readcount')

###############################关联查询#####################################
"""
书籍和人物的关系是   1:n
    书籍 中没有任何关于人物的字段
    人物 中有关于书籍的字段 book 外键
    
语法形式
    通过书籍查询人物信息(已知主表数据,关联查询从表数据)
    主表模型(实例对象).关联模型类名小写_set.all()
    通过人物查询书籍信息( 已知 从表数据,关联查询主表数据)
    从表模型(实例对象).外键
"""
# 方法一：查询书籍为1的人物信息,通过书籍查询人物信息(已知主表数据,关联查询从表数据)
people = PeopleInfo.objects.filter(book=1)
# 方法二：查询书籍为1的人物信息, 主表模型(实例对象).关联模型类名小写_set.all()
book = BookInfo.objects.get(id=1)
people = book.peopleinfo_set.all()

# 查询书籍为'天龙八部'的所有人物信息
# 步骤一；查询书籍为'天龙八部'
book = BookInfo.objects.filter(name='天龙八部')  # 返回的是列表，不是对象
# 步骤二：通过书籍查询人物信息
people = book[0].peopleinfo_set.all()
# 验证人物是否来自“天龙八部”
people_book_id = people[0].book_id



'''通过人物查询书籍信息（已知从表数据，关联查询主表数据)
'''
# 查询人物“曹操”来自哪个书籍
person=PeopleInfo.objects.get(name='曹操')
# 通过人物查询书籍书名属性
book_name = person.book.name
# 通过人物查询书籍阅读量属性
book_count = person.book.readcount


############################# 关联过滤查询     ###############################

"""
     我们需要的是书籍信息,已知条件是人物信息
    我们需要的是主表数据, 已知条件是从表信息

    filter(外键类名小写__字段__运算符=值)

"""
# 查询图书，要求图书人物为"郭靖"
books = BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
books = BookInfo.objects.filter(peopleinfo__name='郭靖')
# 查询图书，要求图书中人物的描述包含"八"
people = BookInfo.objects.filter(peopleinfo__description__contains='八')
'''
    filter(外键类名小写__字段__运算符=值)
    注意：如果没有"__运算符"部分，表示等于。
'''
# 查询书名为“天龙八部”的所有人物
people = PeopleInfo.objects.filter(book__name='天龙八部')
people = PeopleInfo.objects.filter(book__name__exact='天龙八部')

# 查询图书阅读量大于200的所有人物
people = PeopleInfo.objects.filter(book__readcount__lt=100)

# 查询图书阅读量大于评论书籍的所有人物
people=PeopleInfo.objects.filter(book__readcount__lt=F('book__commentcount'))

# 查询id大于2 或者 阅读量大于20书籍的中是否含有‘黄’人物
people=PeopleInfo.objects.filter((Q(book__id__gt=2)|Q(book__readcount__gt=20))&Q(name__contains='黄'))
people=PeopleInfo.objects.filter(Q(book__id__gt=2)|Q(book__readcount__gt=20)).filter(name__contains='黄')



###############################查询集#####################################
'''
Django的ORM中存在查询集的概念。
查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。
当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：
    all()：返回所有数据。
    filter()：返回满足条件的数据。
    exclude()：返回满足条件之外的数据。
    order_by()：对结果进行排序。
特性：1、惰性执行  :创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用
     2、缓存:  查询集会缓存结果，以避免重复查询数据库。
'''
# 对阅读量大于30的书籍，默认升序
books = BookInfo.objects.filter(readcount__gt=30).order_by('pub_date')
# 默认降序
books = BookInfo.objects.filter(readcount__gt=30).order_by('-pub_date')


# 缓存方法:
# 情况一：如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。
bookid_list=[book.id for book in BookInfo.objects.all()]
# 情况二：只是创建了一个查询集books,经过存储后，可以重用查询集，第二次使用缓存中的数据。
books = BookInfo.objects.all()
bookid_list = [book.id for book in books]


# 限制查询集
books = BookInfo.objects.all()[0:2]
books = BookInfo.objects.all()[:2]
#######################分页##############################
# from django.core.paginator import Paginator

books = BookInfo.objects.all()
# object_list        结果集 /列表
#  per_page         每页多少条记录
# object_list, per_page
# class Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)
    # 1. object_list:要分页的数据
    # 2. per_page:每页显示多少条数据
    # 3. orphans:最后一页最少有多少条数据
    # 4. allow_empty_first_page:是否允许空的第一页
# 当使用 len() 或直接迭代时，分页器的作用就像一个 Page 的序列。
p = Paginator(list(books), 4)
# 共多少条
p_count = p.count
# 获取第几页的数据
books_page = p.page(1)
# 获取第一页的数据
books_1_list = books_page.object_list  # 返回的是列表
# 下一页
books_bool=books_page.has_next()
# 上一页
books_bool=books_page.has_previous()
# 获取总页数。
total_page = p.num_pages
# 索引获取条目8在哪页
page_num = p.get_page(8)
#