"""Log."""
from colorama import Fore, Back, Style

import enum
import datetime


class LogLevel(enum.Enum):
    DEBUG = 0,
    INFO = 1,
    SUCCESS = 2,
    WARN = 3,
    ERROR = 4,
    INPUT = 5,


class Log:
    """Log."""

    def __init__(self, bot_name: str):
        """Init."""
        self.bot_name = bot_name

    def write_line(self, log_level: LogLevel, data: str, *args, **kwargs):
        """Write line."""
        time = datetime.datetime.now().strftime('%H:%M:%S')
        level = self._get_log_level(log_level).upper()
        color = self._get_color(log_level)
        print(f"{color}[{self.bot_name} {time}] {level}: {data}", *args, **kwargs)

    def ask_input(self, data):
        """Ask for user input."""
        self.write_line(LogLevel.INPUT, data)

    def debug(self, data):
        """Log debug"""
        self.write_line(LogLevel.DEBUG, data)

    def info(self, data):
        """Log info."""
        self.write_line(LogLevel.INFO, data)

    def success(self, data):
        """Log success."""
        self.write_line(LogLevel.SUCCESS, data)

    def warn(self, data):
        """Log warning."""
        self.write_line(LogLevel.WARN, data)

    def error(self, data):
        """Log error."""
        self.write_line(LogLevel.ERROR, data)

    def _get_log_level(self, log_level: LogLevel):
        """Get log level str."""
        if log_level == LogLevel.DEBUG:
            return 'DEBUG'
        elif log_level == LogLevel.INFO:
            return 'INFO'
        elif log_level == LogLevel.SUCCESS:
            return 'SUCESS'
        elif log_level == LogLevel.WARN:
            return 'WARN'
        elif log_level == LogLevel.ERROR:
            return 'ERROR'
        elif log_level == LogLevel.INPUT:
            return 'INPUT'

    def _get_color(self, log_level: LogLevel):
        """Get color."""
        if log_level == LogLevel.DEBUG:
            return Fore.WHITE
        elif log_level == LogLevel.INFO:
            return Fore.WHITE
        elif log_level == LogLevel.SUCCESS:
            return Fore.GREEN
        elif log_level == LogLevel.WARN:
            return Fore.YELLOW
        elif log_level == LogLevel.ERROR:
            return Fore.RED
        elif log_level == LogLevel.INPUT:
            return Fore.BLUE
