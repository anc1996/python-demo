#!/user/bin/env python3
# -*- coding: utf-8 -*-
from redis.sentinel import Sentinel

# Sentinel 配置
REDIS_SENTINELS = [
    ('192.168.20.2', 26379),
]

# Sentinel 实例
sentinel = Sentinel(REDIS_SENTINELS)

# 获取 master 实例，指定密码
cli = sentinel.master_for('mymaster', password='123456')

# 写入数据
cli.set('itcast', 'python')

# 读取数据
value = cli.get('itcast')
print(value)  # 输出: b'python'
