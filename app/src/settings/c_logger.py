import os
from loguru import logger
from app.src.settings.base import PROJECT_DIR


server_log_path = os.path.join(os.path.join(PROJECT_DIR, "logs"), "server.log")
logger.add(server_log_path, retention="10 days", level="INFO", format="{time} {level} {message}")

LOG_CONFIGURE = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "default_file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": server_log_path,
        },
        "default_console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
        "access_file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": server_log_path,
        },
        "access_console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default_file", "default_console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default_file", "default_console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access_file", "access_console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
