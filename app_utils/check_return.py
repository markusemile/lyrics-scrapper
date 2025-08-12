from app_model import ResponseModel
from typing import Any


def check_return(res: Any, expected_type: Any = dict):
    if not res:
        return "EMPTY"
    if res is None or not isinstance(res, expected_type):
        return False
    return True
