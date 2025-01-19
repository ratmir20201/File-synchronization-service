from typing import Any


def create_good_response(**kwargs) -> dict[str, Any]:
    """Функция для создания положительного ответа."""
    return {"result": True, **kwargs}


def create_error_response(error_message: str) -> dict[str, Any]:
    """Функция для создания ответа с ошибкой."""
    return {"result": False, "error_message": error_message}
