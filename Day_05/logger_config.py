import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger():
    # Main application logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)

    # Rotating file handler (10MB per file, 5 backups)
    handler = RotatingFileHandler(
        f"{LOG_DIR}/app.log",
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    # Format of each log message
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def setup_access_logger():
    access_logger = logging.getLogger("access_logger")
    access_logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        f"{LOG_DIR}/access.log",
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    access_logger.addHandler(handler)
    return access_logger

