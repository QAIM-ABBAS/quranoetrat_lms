import logging
from logging.config import dictConfig

from app.core.config import settings

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging() -> None:
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": LOG_FORMAT,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": log_level,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": log_level,
            },
            "loggers": {
                "uvicorn.error": {"level": log_level},
                "uvicorn.access": {"level": "INFO"},
                "sqlalchemy.engine": {
                    "level": "INFO" if settings.DEBUG else "WARNING",
                },
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)