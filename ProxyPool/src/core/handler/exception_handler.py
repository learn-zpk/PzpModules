# encoding:utf-8

# 统一异常处理
from flask import jsonify

from src.core.framework.operate_code import OperateCode
from src.core.framework.operate_exception import BusinessException, AuthException


def init(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        status_code = 500
        if isinstance(error, BusinessException):
            status_code = 200
        elif isinstance(error, AuthException):
            status_code = 400
        # 记录日志
        # flask_log_handler.log_flask_exception(error)

        return jsonify({
            'error': {
                'code': error.code if hasattr(error, 'code') else OperateCode.SYSTEM_ERROR.value,
                'message': str(error)
            }
        }), status_code
