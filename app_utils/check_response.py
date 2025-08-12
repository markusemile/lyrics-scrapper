from app_model.response_model import ResponseModel
from typing import Any


def check_response(res: ResponseModel, expected_data=True, expected_type: Any = dict):
    if not res:
        return False
    if res.status_code != 200:
        return False
    if expected_data:
        if res.data is None or not isinstance(res.data, expected_type):
            return False
    return True


