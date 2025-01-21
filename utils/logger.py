import sys

from loguru import logger as _logger

_logger.remove()


_logger.add(
    "logfile.log",
    format="synchronizer {time} {level} {message}",
    level="INFO",
    backtrace=False,
)


_logger.add(
    sys.stdout,
    format="synchronizer <green>{time}</green> <level>{level}</level> "
    "<cyan>{message}</cyan>",
    level="INFO",
    colorize=True,
)


logger = _logger
