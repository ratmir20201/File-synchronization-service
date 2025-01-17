import os.path

from utils.config import config
from utils.helper import CloudStoringHelper

helper = CloudStoringHelper(token=config.TOKEN, folder_name=config.CLOUD_FOLDER_NAME)


# Прописать путь до файла 1.txt может это уберет ошибку 404
path = os.path.join("monitored_folder", "test.png")
result_2 = helper.load(path=path)

print(result_2)
print(result_2.text)


result = helper.get_info()
print(result)
