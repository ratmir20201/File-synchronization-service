import os
import time

from watchdog.observers import Observer

from utils.config import config
from utils.directory_watcher import event_handler
from utils.helper import CloudStoringHelper
from utils.logger import logger

helper = CloudStoringHelper(token=config.TOKEN, folder_name=config.CLOUD_FOLDER_NAME)


monitored_folder_path = os.path.join(config.LOCAL_FOLDER_NAME)

observer = Observer()
observer.schedule(event_handler, path=monitored_folder_path, recursive=False)


if __name__ == "__main__":
    logger.info(
        "Программа синхронизации файлов начинает работу с директорией {directory}".format(
            directory=monitored_folder_path,
        )
    )

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
