import os
import time

from watchdog.observers import Observer

from utils.config import config
from utils.directory_watcher import event_handler
from utils.logger import logger

monitored_folder_path = os.path.join(config.LOCAL_FOLDER_NAME)


if __name__ == "__main__":

    if not os.path.exists(monitored_folder_path):
        os.mkdir(monitored_folder_path)
        logger.info(
            "Директория {directory} успешно создана.".format(
                directory=monitored_folder_path,
            )
        )

    logger.info(
        "Программа синхронизации файлов начинает работу с директорией {directory}.".format(
            directory=monitored_folder_path,
        )
    )

    observer = Observer()
    observer.schedule(event_handler, path=monitored_folder_path, recursive=False)

    try:
        observer.start()
        while True:
            time.sleep(config.PERIODICITY)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
