import sys

from utils.decorators import error_handler
from utils.logger import logger
from utils.requests import make_request
from YandexApi.status_codes import FOLDER_ALREADY_EXIST_CODE, HTTP_CREATED, HTTP_OK


class CloudStoringPresetting:
    """
    Класс для настройки облака.

    Перед взаимодействием с сервером, проверяется токен и
    создается папка в яндекс диске с названием из переменных окружения.
    """

    def __init__(self, token: str, folder_name: str):
        self.token = token
        if not self._token_validator():
            logger.error("Программа завершает свою работу из-за ошибки.")
            sys.exit()
        self.folder_name = folder_name
        self.folder_path = "disk:/{folder_name}".format(
            folder_name=folder_name,
        )

        self._folder_create()

    @error_handler
    def _token_validator(self) -> bool:
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk",
            token=self.token,
            method="get",
        )
        if response.status_code == HTTP_OK:
            return True
        logger.error(
            "Ваш токен недействителен: {error_code} — {error_message}".format(
                error_code=response.status_code,
                error_message=response.text,
            )
        )
        return False

    @error_handler
    def _folder_create(self) -> None:
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            method="put",
            params={"path": self.folder_path},
        )
        if response.status_code == HTTP_CREATED:
            logger.info(
                "Директория {folder_name} успешно создана на Яндекс диске.".format(
                    folder_name=self.folder_name,
                )
            )
        elif response.status_code != FOLDER_ALREADY_EXIST_CODE:
            logger.error(
                "Произошла ошибка: {error_code} - {error_message}.".format(
                    error_code=response.status_code,
                    error_message=response.text,
                )
            )

    @error_handler
    def _get_file_path(self, filename: str) -> str:
        return "{folder_path}/{filename}".format(
            folder_path=self.folder_path,
            filename=filename,
        )
