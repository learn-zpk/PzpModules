# -*- coding: utf-8 -*-

from flask import Flask

from src.config import global_config

if __name__ == '__main__':
    from src.core.web import init_env

    app = Flask(__name__)
    init_env.init(app)


    @app.before_request
    def _before_request():
        # from flask import request
        # auth_filter.identify(request, accept_dict, deny_dict)
        # todo 验证功能暂不提供
        pass


    app.debug = global_config.get('debug') == 'Y'

    app.run(host=global_config.get('host'), port=global_config.get('port'), threaded=True)
