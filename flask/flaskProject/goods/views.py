#!/user/bin/env python3
# -*- coding: utf-8 -*-


from . import goods_bp


@goods_bp.route('/get_goods')
def get_goods():
    return 'get goods'