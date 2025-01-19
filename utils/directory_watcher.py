import os
from typing import List

from watchdog.events import FileSystemEventHandler

from utils.helper import helper
from utils.logger import logger


class DirectoryChangeHandler(FileSystemEventHandler):
    """Обработчик событий в директории."""

    def __init__(self, ignored_extensions: List[str] = None):
        self.ignored_extensions = ignored_extensions

    def _is_ignored(self, path: str):
        """Проверяет, является ли файл игнорируемым."""
        return any(path.endswith(ext) for ext in self.ignored_extensions)

    def on_modified(self, event):
        """Метод изменяющий файл в облаке если он был изменен локально."""
        if not self._is_ignored(path=event.src_path):
            helper.reload(path=event.src_path)
            logger.info(f"Файл изменён: {event.src_path}")

    def on_created(self, event):
        """Метод создающий файл в облаке если он был создан локально."""
        if not self._is_ignored(path=event.src_path):
            helper.load(path=event.src_path)
            logger.info(f"Файл создан: {event.src_path}")

    def on_deleted(self, event):
        """Метод удаляющий файл в облаке если он был удален локально."""
        if not self._is_ignored(path=event.src_path):
            filename = os.path.basename(event.src_path)
            helper.delete(filename=filename)
            logger.info(f"Файл удалён: {event.src_path}")


event_handler = DirectoryChangeHandler(ignored_extensions=["~", ".tmp", ".bak"])
