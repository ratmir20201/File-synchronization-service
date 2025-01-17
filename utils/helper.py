import json
import os

from utils.requests import make_request


class CloudStoringHelper:
    def __init__(self, token: str, folder_name: str):
        self.token = token
        self.folder_name = folder_name
        self.folder_path = "disk:/{folder_name}".format(
            folder_name=folder_name,
        )

        self.folder_exist()

    def folder_exist(self):
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
        elif response.status_code == 409:
            print(
                "Директория {folder_name} уже существует.".format(
                    folder_name=self.folder_name,
                )
            )

    def load(self, path: str):
        """
        Функция для загрузки файла из локальной директории в облако.

        path(str) - путь до файла на локальном компьютере.
        """
        filename = os.path.basename(path)
        get_url_response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources/upload",
            token=self.token,
            method="get",
            params={
                "path": "{folder_path}/{filename}".format(
                    folder_path=self.folder_path,
                    filename=filename,
                ),
                "url": path,
                "overwrite": True,
            },
        )
        print(get_url_response, get_url_response.text)
        data = json.loads(get_url_response.text)

        with open(path, "rb") as file:
            upload_file_response = make_request(
                url=data["href"],
                token=self.token,
                method=data["method"],
                data=file,
            )

        return upload_file_response

    def reload(self, path: str):
        pass

    def delete(self, filename: str):
        pass

    def get_info(self):
        response = make_request(
            url="https://cloud-api.yandex.net/v1/disk/resources",
            token=self.token,
            params={"path": self.folder_path, "fields": "name,_embedded.items.path"},
            method="get",
        )

        return json.loads(response.text)
