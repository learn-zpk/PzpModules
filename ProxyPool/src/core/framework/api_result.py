# encoding=utf-8

from flask import Response, json

from src.core.framework.operate_code import OperateCode


class ApiResult(object):

    @staticmethod
    def success(data="", code=OperateCode.OPERATE_SUCCESS.value):
        return Response(json.dumps({"data": data, "code": code}, ensure_ascii=False),
                        status=200,
                        mimetype='application/json')

    @staticmethod
    def failed(message, code=OperateCode.SYSTEM_ERROR.value):
        return Response(json.dumps({"code": code, "message": message}, ensure_ascii=False),
                        status=200,
                        mimetype='application/json')
