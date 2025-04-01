class MasterSlaveDBRouter(object):
    """数据库读写路由"""

    def db_for_read(self, model, **hints):
        """读所使用的服务器:"""
        # 建议用于读取“模型”类型对象的数据库。
        # 如果数据库操作可以提供有助于选择数据库的任何附加信息，它将在 hints 中提供。这里 below 提供了有效提示的详细信息。
        # 如果没有建议，则返回 None 。
        return "slave"

    def db_for_write(self, model, **hints):
        """写所使用的服务器:"""
        # 建议用于写入模型类型对象的数据库。
        # 如果数据库操作可以提供有助于选择数据库的任何附加信息，它将在 hints 中提供。这里 below 提供了有效提示的详细信息。
        # 如果没有建议，则返回 None 。
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        
        # 如果允许 obj1 和 obj2 之间的关系，返回 True 。
        # 如果阻止关系，返回 False ，或如果路由没意见，则返回 None。这纯粹是一种验证操作，由外键和多对多操作决定是否应该允许关系。
        # 如果没有路由有意见（比如所有路由返回 None），则只允许同一个数据库内的关系。
        db_set = {'default', 'slave'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True  # 允许在主库和从库之间的关系
        return None

    def allow_migrate(db, app_label, model_name=None, **hints):
        """
        决定是否允许迁移操作在别名为 db 的数据库上运行。
            如果操作运行，那么返回 True ，
            如果没有运行则返回False ，或路由没有意见则返回None 。
        """
        return db == 'default'