# encoding:utf-8
from src.api.controller.proxy_manage_controller import proxy_manage


def register(app):
    # 标注平台
    app.register_blueprint(proxy_manage, url_prefix='/proxy')
