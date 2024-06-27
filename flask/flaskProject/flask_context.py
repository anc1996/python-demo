#!/user/bin/env python3
# -*- coding: utf-8 -*-

from flask import current_app, Blueprint

context_bp=Blueprint('passport',__name__)

@context_bp.route('/context_current_app')
def context_app():
    print(current_app.redis_cli)
    return current_app.redis_cli

