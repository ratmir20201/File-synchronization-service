import functools
from typing import Callable

from utils.responses import create_error_response


def error_handler(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            return create_error_response(
                error_message="Произошла ошибка в методе {func_name}: {error}".format(
                    func_name=func.__name__,
                    error=str(exc),
                )
            )

    return wrapper
