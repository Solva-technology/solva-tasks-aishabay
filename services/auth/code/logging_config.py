import logging
import os
import queue
from logging.handlers import (
    QueueHandler,
    QueueListener,
    TimedRotatingFileHandler,
)

from services.auth.code.core.constants import APP_LOG_BACKUP_COUNT, ERRORS_LOG_BACKUP_COUNT


def setup_logging(
    log_level: str = "DEBUG",
    log_dir: str = "services/auth/logs",
) -> QueueListener:
    """
    Setup non-blocking logging for FastAPI using QueueHandler + QueueListener.

    Args:
        log_level (str): Minimum log level
            (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir (str): Directory where logs will be stored.

    Returns:
        QueueListener: logging listener (must be started and stopped properly).
    """

    os.makedirs(log_dir, exist_ok=True)

    console_formatter = logging.Formatter(
        "%(levelname)s in %(name)s: %(message)s",
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)

    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        when="midnight",
        backupCount=APP_LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    error_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, "errors.log"),
        when="W0",  # every Sunday
        backupCount=ERRORS_LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.propagate = False

    python_multipart_logger = logging.getLogger("python_multipart")
    python_multipart_logger.propagate = False

    handlers = [console_handler, file_handler, error_handler]

    log_queue: queue.Queue = queue.Queue(-1)  # infinite queue

    queue_handler = QueueHandler(log_queue)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))
    root_logger.addHandler(queue_handler)

    listener = QueueListener(log_queue, *handlers, respect_handler_level=True)

    return listener
