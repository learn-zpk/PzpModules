from flask import Blueprint

from src.core.framework.api_result import ApiResult
from src.api.service import proxy_service as service

proxy_manage = Blueprint('proxy_manage', __name__)


@proxy_manage.route('/list', methods=['GET'])
def _list():
    return ApiResult.success(service.proxy_list())
