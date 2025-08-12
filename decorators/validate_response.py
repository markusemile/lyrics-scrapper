import json
from typing import Callable, Any
from app_model.response_model import ResponseModel
from functools import wraps
from requests import Response
from logging import Logger
from app_utils import check_response
from app_utils.color import error


def validate_response(expected_data: bool = True, expected_type: Any = dict):

    def return_error(msg: str, logger: Logger):
        if logger:
            logger.error(msg)
            return {"error": msg}
        raise TypeError(msg)

    def to_response_model(response: Response) -> ResponseModel:
        res = ResponseModel(status_code=response.status_code)

        try:
            content = json.loads(response.content)
        except json.JSONDecodeError:
            res.message = f"{response.reason}: Response content is not valid JSON"
            return res

        if response.status_code == 200:
            res.data = content.get("response")

        if response.status_code != 200:
            msg = content.get("meta", {}).get("message", "unknow error")
            res.message = f"{response.reason}: {msg}"

        return res

    def decorator(func: Callable[..., Response],):
        @wraps(func)
        def wrapper(*args, **kwargs):

            res = func(*args, **kwargs)
            instance = args[0] if args and hasattr(args[0], '__class__') else None
            logger = getattr(instance, 'logger', None)

            casted_res: ResponseModel = to_response_model(response=res)

            if not isinstance(casted_res, expected_type):
                casted_res.message = f"function {func.__name__} don't return a ResponseModel"
                # raise TypeError(f"function {func.__name__} don't return a ResponseModel")

            if not check_response(res=casted_res, expected_data=expected_data, expected_type=dict):
                error(f"{casted_res.message}")
                input("[enter to continue...]")
                # raise ValueError(f"Invalid response in {func.__name__}: {casted_res}")

            return casted_res
        return wrapper
    return decorator
