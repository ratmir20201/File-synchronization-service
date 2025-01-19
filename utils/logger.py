import sys

from loguru import logger

logger.add(
    sys.stderr,
    format="synchronizer {time} {level} {message}",
    level="INFO",
)

logger.add(
    "log.txt",
    format="synchronizer {time} {level} {message}",
    level="INFO",
)


__all__ = ["logger"]
