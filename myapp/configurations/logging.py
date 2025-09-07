import os
import logging

# Logging Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = PROJECT_ROOT[:-4]

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "app.log")


class RelativePathFilter(logging.Filter):
    def filter(self, record):
        try:
            record.relativepath = os.path.relpath(record.pathname, PROJECT_ROOT)
        except Exception:
            record.relativepath = record.pathname
        return True


logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "relative_path": {
            "()": RelativePathFilter,
        }
    },
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "{log_color}{levelname:5}{reset} "
                "{blue}[{asctime}]{reset} "
                # "{bold_yellow}[{name}]{reset} "
                "{bold_yellow}[{relativepath}:{reset}{green}{lineno}{reset}{yellow}]{reset} "
                "{yellow}---{reset} {white}{message}{reset}"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "colored_django": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "{log_color}{levelname:5}{reset} "
                "{blue}[{asctime}]{reset} "
                "{bold_yellow}[{name}]{reset} "
                "{yellow}---{reset} {white}{message}{reset}"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "plain": {
            "format": '{levelname:8} [{asctime}] [{relativepath}:{lineno}] - "{message}"',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "plain_django": {
            "format": "{levelname:8} [{asctime}] [{name}] --- {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console_app": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "filters": ["relative_path"],
            "level": "DEBUG",
        },
        "console_django": {
            "class": "logging.StreamHandler",
            "formatter": "colored_django",
            "level": "INFO",
        },
        "file_app": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 2,
            "formatter": "plain",
            "filters": ["relative_path"],
            "encoding": "utf-8",
            "level": "DEBUG",
        },
        "file_django": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 2,
            "formatter": "plain_django",
            "encoding": "utf-8",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console_app", "file_app"],
        "level": "INFO",
    },
    "loggers": {
        "myapp": {
            "handlers": ["console_app", "file_app"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console_django", "file_django"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console_django", "file_django"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logger = logging.getLogger("myapp")
