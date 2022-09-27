from logging import Logger, getLogger
from logging.config import dictConfig
from os import makedirs, path


def DefaultConsoleLogger() -> Logger:
    config_dict = {
        "version": 1,
        "formatters": {
            "tally_console_formatter": {
                "format": "%(asctime)s %(levelname)-8s %(name)-14s %(message)s",
                "datefmt": "%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "tally_console_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "tally_console_formatter"
            }
        },
        "loggers": {
            "tally_console": {
                "qualname": "tally_console",
                "handlers": ["tally_console_handler"],
                "level": "DEBUG"
            }
        }
    }
    dictConfig(config_dict)
    return getLogger("tally_console")


def DefaultFileLogger(filename: str = "./logs/tallytime.log") -> Logger:
    if not path.exists(path.dirname(filename)):
        makedirs(path.dirname(filename))

    config_dict = {
        "version": 1,
        "formatters": {
            "tally_file_formatter": {
                "format": "%(asctime)s %(levelname)-8s %(name)-14s %(message)s",
                "datefmt": "%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "tally_file_handler": {
                "()": "logging.FileHandler",
                "filename": filename,
                "formatter": "tally_file_formatter"
            }
        },
        "loggers": {
            "tally_file": {
                "qualname": "tally_file",
                "handlers": ["tally_file_handler"],
                "level": "DEBUG"
            }
        }
    }
    dictConfig(config_dict)
    return getLogger("tally_file")
