import json
import os
from typing import Any, Dict

from utils.config import config
from utils.decorators import error_handler
from utils.requests import make_request
from utils.responses import create_error_response, create_good_response
from YandexApi.settings import CloudStoringPresetting
from YandexApi.status_codes import HTTP_CREATED, HTTP_NO_CONTENT


class CloudStoringAPI(CloudStoringPresetting):
    """Класс для взаимодействия с API Яндекс диска."""

    @error_handler
    def load(self, path: str):
        """
        Функция для загрузки файла из локальной директории в облако.

        path(str) - путь до файла на локальном компьютере.
        """
        response = self._make_load_request(path=path, overwrite=False)
        return response

    @error_handler
    def reload(self, path: str):
        """
        Функция для перезаписи файла в директории на облаке.

        path(str) - путь до файла на локальном компьютере.
        """
        response = self._make_load_request(path=path, overwrite=True)
        return response

    @error_handler
    def delete(self, filename: str):
        """Функция для удаления файла из директории в облаке через название файла."""
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            method="delete",
            params={
                "path": self._get_file_path(filename=filename),
            },
        )

        if response.status_code == HTTP_NO_CONTENT:
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

    @error_handler
    def _get_url_for_load_request(self, path: str, overwrite: bool) -> Dict[str, Any]:
        """Приватный метод для получения ссылки на загрузку или перезапись файла."""

        filename = os.path.basename(path)

        get_url_response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources/upload",
            token=self.token,
            method="get",
            params={
                "path": self._get_file_path(filename=filename),
                "url": path,
                "overwrite": overwrite,
            },
        )
        data: Dict[str, Any] = json.loads(get_url_response.text)

        return data

    @error_handler
    def _make_load_request(self, path: str, overwrite: bool = False) -> Dict[str, Any]:
        """Приватный метод для исполнения загрузки или перезаписи файла на диске."""

        data = self._get_url_for_load_request(path=path, overwrite=overwrite)

        with open(path, "rb") as file:
            upload_file_response = make_request(
                url=data["href"],
                token=self.token,
                method=data["method"],
                data=file,
            )

        if upload_file_response.status_code == HTTP_CREATED:
            return create_good_response()
        return create_error_response(
            error_message="Файл не был создан ошибка {error_code}".format(
                error_code=upload_file_response.status_code
            ),
        )


helper = CloudStoringAPI(token=config.token, folder_name=config.cloud_folder_name)
