import json
import os
from typing import Any

from utils.handlers import error_handler
from utils.requests import make_request
from utils.responses import create_error_response, create_good_response


class CloudStoringHelper:
    def __init__(self, token: str, folder_name: str):
        self.token = token
        self.folder_name = folder_name
        self.folder_path = "disk:/{folder_name}".format(
            folder_name=folder_name,
        )

        self.__folder_create()

    @error_handler
    def __folder_create(self):
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            method="put",
            params={"path": self.folder_path},
        )
        if response.status_code == 201:
            print(
                "Директория {folder_name} успешно создана.".format(
                    folder_name=self.folder_name,
                )
            )

    @error_handler
    def __get_url_for_load_request(self, path: str, overwrite: bool) -> dict[str, Any]:
        """Приватный метод для получения ссылки на загрузку или перезапись файла."""

        filename = os.path.basename(path)

        get_url_response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources/upload",
            token=self.token,
            method="get",
            params={
                "path": self.folder_path + "/" + filename,
                "url": path,
                "overwrite": overwrite,
            },
        )
        data = json.loads(get_url_response.text)

        return data

    @error_handler
    def __make_load_request(self, path: str, overwrite: bool = False) -> dict:
        """Приватный метод для исполнения загрузки или перезаписи файла на диске."""

        data = self.__get_url_for_load_request(path=path, overwrite=overwrite)

        with open(path, "rb") as file:
            upload_file_response = make_request(
                url=data["href"],
                token=self.token,
                method=data["method"],
                data=file,
            )

        if upload_file_response.status_code == 201:
            return create_good_response()
        return create_error_response(
            error_message="Файл не был создан ошибка {error_code}".format(
                error_code=upload_file_response.status_code
            ),
        )

    @error_handler
    def load(self, path: str):
        """
        Функция для загрузки файла из локальной директории в облако.

        path(str) - путь до файла на локальном компьютере.
        """
        response = self.__make_load_request(path=path, overwrite=False)
        return response

    @error_handler
    def reload(self, path: str):
        """
        Функция для перезаписи файла в директории на облаке.

        path(str) - путь до файла на локальном компьютере.
        """
        response = self.__make_load_request(path=path, overwrite=True)
        return response

    @error_handler
    def delete(self, filename: str):
        """Функция для удаления файла из директории в облаке через название файла."""
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            method="delete",
            params={"path": self.folder_path + "/" + filename},
        )

        if response.status_code == 204:
            return create_good_response()
        return create_error_response(
            "Не удалось удалить файл, ошибка {error_code}".format(
                error_code=response.status_code
            )
        )

    @error_handler
    def get_info(self):
        """Функция для получения всех файлов в директории на сервере."""
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            params={"path": self.folder_path, "fields": "name,_embedded.items.path"},
            method="get",
        )

        return create_good_response(files=json.loads(response.text))
