import logging
import sys
from typing import Literal

LoggerName = Literal["extraction", "request", "error"]


def setup_logging(level: str = "INFO") -> None:
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    if root.handlers:
        return

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    for name in ("extraction", "request", "error"):
        logging.getLogger(name).setLevel(
            getattr(logging, level.upper(), logging.INFO)
        )


def get_logger(name: LoggerName) -> logging.Logger:
    return logging.getLogger(name)
