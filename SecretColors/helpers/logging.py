#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Logging util class

import logging
import os
import sys
from typing import Type

LOGGER_NAME = "SecretColors"


class LogFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno > self.__level


class Log:
    """
    Thin wrapper around the 'SecretColors' logger. Handlers are attached
    only once per process (and only when `show_log` is True), so creating
    many Log objects does not duplicate the output.
    """

    def __init__(self, show_log: bool = False,
                 options: dict = None,
                 add_to_console: bool = True,
                 add_to_file: bool = False,
                 min_log_level: int = -1,
                 filename: str = "SecretColor.log",
                 logging_format: str = "%(asctime)s %(script)s [%("
                                       "levelname)s] : %(message)s"):
        self.show_log = show_log
        self.formatter = logging.Formatter(logging_format)
        self.add_to_console = add_to_console
        self.add_to_file = add_to_file
        self.filename = filename
        self.min_log_level = min_log_level
        self._configured = False

    @property
    def log_object(self) -> logging.Logger:
        logger = logging.getLogger(LOGGER_NAME)
        if self.show_log and not self._configured:
            self._configured = True
            if logger.level == logging.NOTSET:
                logger.setLevel(logging.DEBUG)
            if self.add_to_console:
                self._attach(logger, "console", logging.StreamHandler)
            if self.add_to_file:
                path = os.path.abspath(self.filename)
                self._attach(logger, f"file:{path}",
                             lambda: logging.FileHandler(path))
        return logger

    def _attach(self, logger: logging.Logger, key: str, factory):
        if any(getattr(h, "_secret_colors_key", None) == key
               for h in logger.handlers):
            return
        handler = factory()
        handler._secret_colors_key = key
        handler.setFormatter(self.formatter)
        handler.addFilter(LogFilter(self.min_log_level))
        logger.addHandler(handler)

    @staticmethod
    def _caller() -> str:
        frame = sys._getframe(3)
        return os.path.basename(frame.f_code.co_filename)

    def _emit(self, level: int, message):
        self.log_object.log(level, message, extra={"script": self._caller()},
                            stacklevel=3)

    def info(self, message):
        if self.show_log:
            self._emit(logging.INFO, message)

    def error(self, message, raise_exception=True,
              exception: Type[Exception] = None):
        if self.show_log:
            self._emit(logging.ERROR, message)

        if raise_exception:
            if exception is None:
                raise Exception(message)
            else:
                raise exception(message)

    def warn(self, message):
        if self.show_log:
            self._emit(logging.WARNING, message)

    def debug(self, message):
        if self.show_log:
            self._emit(logging.DEBUG, message)

    def deprecated(self, message):
        self._emit(logging.WARNING, message)
