from dataclasses import dataclass
from enum import Enum
from itertools import count


class WriteMode(Enum):
    ON_EACH = 1
    ON_EACH_NO_START = 2
    ON_EACH_NO_END = 3
    ON_END = 4


class TimeRenderMode(Enum):
    AS_SECONDS = 1
    AS_MILLIS = 2
    AS_UTC = 3
    AS_TIMEZONE = 4


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


_log_num = count(1)


@dataclass
class TallyLogSettings:
    """Class for keeping track of the configuration for a TallyLog"""
    name: str = "custom_{}".format(next(_log_num))  # TODO: USE THIS NAME
    write_mode: WriteMode = WriteMode.ON_EACH
    default_log_level: LogLevel = LogLevel.INFO
    default_expire_time: int = 3600  # in seconds
    time_render: TimeRenderMode = TimeRenderMode.AS_SECONDS
    # TODO: ADD TIMEZONE SUPPORT
