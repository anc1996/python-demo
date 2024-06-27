#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import current_app, Blueprint

context_bp1=Blueprint('context_flask1',__name__)

@context_bp1.route('/context_current_app1')
def context_app():
    print(current_app.redis_cli)
    return current_app.redis_cli

