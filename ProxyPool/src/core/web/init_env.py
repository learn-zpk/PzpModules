from src.core.handler import cors_handler, exception_handler, json_hanlder
from src.core.web import blueprint_registry


def init(app):
    """
    跨域处理
    """
    cors_handler.init(app)
    """
    全局异常处理
    """
    exception_handler.init(app)
    """
    序列化处理
    """
    json_hanlder.init(app)
    """
    蓝图注册
    """
    blueprint_registry.register(app)



