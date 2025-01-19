from loguru import logger

# logger.add(
#     sys.stdout,
#     format="synchronizer {time} {level} {message}",
#     level="INFO",
# )

logger.add(
    "log.txt",
    format="synchronizer {time} {level} {message}",
    level="INFO",
)


__all__ = ["logger"]
