import sys

from loguru import logger

logger.remove()


logger.add(
    "logfile.log",
    format="synchronizer {time} {level} {message}",
    level="INFO",
    backtrace=False,
)


logger.add(
    sys.stdout,
    format="synchronizer <green>{time}</green> <level>{level}</level> <cyan>{message}</cyan>",
    level="INFO",
    colorize=True,
)


__all__ = ["logger"]
