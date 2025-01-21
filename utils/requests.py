from typing import Any, Callable, Optional

import requests


def get_headers(token: str) -> dict[str, str]:
    headers = {
        "Authorization": "OAuth {token}".format(token=token),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    return headers


def _handle_get(
    url: str,
    token: str,
    params: Optional[dict[str, Any]],
    data: Any,
) -> requests.Response:
    return requests.get(url, headers=get_headers(token), params=params, data=data)


def _handle_put(
    url: str,
    token: str,
    params: Optional[dict[str, Any]],
    data: Any,
) -> requests.Response:
    return requests.put(
        url,
        headers=get_headers(token),
        params=params,
        data=data,
    )


def _handle_post(
    url: str,
    token: str,
    params: Optional[dict[str, Any]],
    data: Any,
) -> requests.Response:
    return requests.post(
        url,
        headers=get_headers(token),
        params=params,
        data=data,
    )


def _handle_delete(
    url: str,
    token: str,
    params: Optional[dict[str, Any]],
    data: Any,
) -> requests.Response:
    return requests.delete(
        url,
        headers=get_headers(token),
        params=params,
        data=data,
    )


method_handlers: dict[str, Callable[..., requests.Response]] = {
    "GET": _handle_get,
    "PUT": _handle_put,
    "POST": _handle_post,
    "DELETE": _handle_delete,
}


def make_request(
    url: str,
    token: str,
    method: str,
    params: Optional[dict[str, Any]] = None,
    data=None,
) -> requests.Response:
    method = method.upper()

    if method not in method_handlers:
        raise ValueError("Указан неверный HTTP метод.")

    method_handler = method_handlers[method]

    return method_handler(url=url, token=token, params=params, data=data)
