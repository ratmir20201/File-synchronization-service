from watchdog.events import FileSystemEventHandler

from utils.logger import logger


class DirectoryChangeHandler(FileSystemEventHandler):
    """Обработчик событий в директории."""

    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"Файл изменён: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"Файл создан: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"Файл удалён: {event.src_path}")


event_handler = DirectoryChangeHandler()
