import os

from utils.config import config
from utils.helper import CloudStoringHelper
from utils.logger import logger

helper = CloudStoringHelper(token=config.TOKEN, folder_name=config.CLOUD_FOLDER_NAME)


monitored_folder_path = os.path.join(config.LOCAL_FOLDER_NAME)

logger.info(
    "Программа синхронизации файлов начинает работу с директорией {directory}".format(
        directory=monitored_folder_path,
    )
)

# if not os.path.exists(monitored_folder_path):
#     os.mkdir(monitored_folder_path)
#
#
# while True:
#     for i_file in os.listdir():
#         pass
