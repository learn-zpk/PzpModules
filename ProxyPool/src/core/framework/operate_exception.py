# encoding=utf-8
from src.core.framework.operate_code import OperateCode


class BusinessException(Exception):
    def __init__(self, message, code=OperateCode.BUSINESS_ERROR.value):
        self.code = code
        self.message = message


class DatabaseException(Exception):
    def __init__(self, message, code=OperateCode.DATABASE_ERROR.value):
        self.code = code
        self.message = message


class AuthException(Exception):
    def __init__(self, message, code=OperateCode.AUTH_ERROR.value):
        self.code = code
        self.message = message
