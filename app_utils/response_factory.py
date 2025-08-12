from app_model import ResponseModel
from app_class import AppResponse
from typing import Any


def success_response(data: Any = None, message: str = "success", code: int = 200):
    res = ResponseModel(status_code=code, message=message, data=data)
    return AppResponse(success=True, res=res)


def error_response(data: Any = None, message: str = "An error occured", code: int = 400):
    res = ResponseModel(status_code=code, message=message, data=data)
    return AppResponse(success=False, res=res)
