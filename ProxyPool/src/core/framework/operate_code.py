# coding=utf-8
from enum import unique, Enum


@unique
class OperateCode(Enum):
    OPERATE_SUCCESS = 0  # 成功
    AUTH_ERROR = 1  # 认证错误
    SYSTEM_ERROR = 2  # 系统错误
    BUSINESS_ERROR = 3  # 业务错误
    DATABASE_ERROR = 4  # 数据库操作错误
