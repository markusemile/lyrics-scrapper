import json
from typing import Callable, Any, Union, get_args
from functools import wraps
from logging import Logger


def validate_return(exit_on_fail=False, context: str = ""):
    def return_error(msg: str, logger: Logger):
        if logger:
            logger.error(msg)
            return {"error": msg}
        if exit_on_fail:
            raise TypeError(msg)
        input(f"WARNING: {msg}, [ENTER] to continue")

    def try_cast(res: Any, expect_type: type) -> Any:
        """
        convert string result into expected type if possible
        :param res: str = response
        :param expect_type: Any
        :return: Any
        """
        if not isinstance(res, str):
            return res

        cleaned = res.strip()

        try:
            if expect_type == int and cleaned.isdigit():
                return int(cleaned)

            if expect_type == float:
                return float(cleaned)

            if expect_type == bool:
                if cleaned.lower() in {"true", "1", "yes", "y", "ok", "oui"}:
                    return True
                if cleaned.lower() in {"false", "0", "no", "n", "non"}:
                    return False

            if expect_type == list or expect_type == dict:
                parsed = json.loads(cleaned)
                if isinstance(parsed, expect_type):
                    return parsed

            if expect_type is None:
                return None

        except TypeError:
            pass
        return res

    def is_none_allowed(expected_type) -> bool:
        args = get_args(expected_type)
        if args:
            return type(None) in args
        return expected_type is type(None)

    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0] if args and hasattr(args[0], '__class__') else None
            logger = getattr(instance, 'logger', None)
            expected_type: Any = kwargs.pop("expected_type", None)

            res = func(*args, **kwargs)

            casted_res = try_cast(res=res, expect_type=expected_type)

            if hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union:
                allowed_types = get_args(expected_type)
            else:
                allowed_types = (expected_type,)

            if res is None and not is_none_allowed(expected_type):
                msg = f"from {context} function {func.__name__} don't return a value"
                return return_error(msg, logger)

            if not isinstance(casted_res, allowed_types):
                if expected_type == int and isinstance(res, str):
                    cleaned = res.strip()
                    if cleaned.isdigit():
                        return int(cleaned)
                msg = (f"[{context}] → function '{func.__name__}' returned type '{type(res).__name__}' "
                       f"instead of expected '{expected_type.__name__}'")
                return return_error(msg=msg, logger=logger)
            return casted_res

        return wrapper

    return decorator
