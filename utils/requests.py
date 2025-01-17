import requests


def get_headers(token: str) -> dict[str, str]:
    headers = {
        "Authorization": "OAuth {token}".format(token=token),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    return headers


def make_request(
    url: str,
    token: str,
    method: str,
    params: dict = None,
    data=None,
) -> requests.Response | dict[str, str]:
    method = method.upper()

    if method == "GET":
        response = requests.get(
            url,
            headers=get_headers(token=token),
            params=params,
        )
    elif method == "PUT":
        response = requests.put(
            url,
            headers=get_headers(token=token),
            params=params,
            data=data,
        )
    elif method == "POST":
        response = requests.post(
            url,
            headers=get_headers(token=token),
            params=params,
        )
    elif method == "DELETE":
        response = requests.delete(
            url,
            headers=get_headers(token=token),
            params=params,
        )
    else:
        return {"error_message": "Указан неверный HTTP метод."}

    return response
