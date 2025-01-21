import os
import time

from watchdog.observers import Observer

from utils.config import config
from utils.directory_watcher import event_handler
from utils.logger import logger

monitored_folder_path = os.path.join(config.local_folder_name)


def setup_directory() -> None:
    """Создание директории, если она отсутствует."""
    if not os.path.exists(monitored_folder_path):
        os.mkdir(monitored_folder_path)
        logger.info(
            "Директория {directory} успешно создана.".format(
                directory=monitored_folder_path,
            )
        )


def start_observer() -> None:
    """Запуск наблюдателя за файлами."""
    observer = Observer()
    observer.schedule(event_handler, path=monitored_folder_path, recursive=False)

    try:
        observer.start()
        time.sleep(config.periodicity)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    setup_directory()
    logger.info(
        "Программа синхронизации файлов начинает работу с директорией "
        "{directory}.".format(
            directory=monitored_folder_path,
        )
    )
    start_observer()
