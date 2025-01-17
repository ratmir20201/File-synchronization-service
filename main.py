import os

from utils.config import config
from utils.helper import CloudStoringHelper

helper = CloudStoringHelper(token=config.TOKEN, folder_name=config.CLOUD_FOLDER_NAME)


# Прописать путь до файла 1.txt может это уберет ошибку 404
local_folder = os.path.join("")
result_2 = helper.load("/monitored_folder/1.txt")

print(result_2)
print(result_2.text)
