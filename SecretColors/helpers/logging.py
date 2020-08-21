#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Logging util class

import inspect
import logging
import os
from typing import Type


class LogFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno > self.__level


class Log:
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
        self._log_object = None
        self.min_log_level = min_log_level

    @property
    def log_object(self):
        if self._log_object is None:
            self._log_object = logging.getLogger("log")
            if self.add_to_console:
                console = logging.StreamHandler()
                console.setFormatter(self.formatter)
                console.addFilter(LogFilter(self.min_log_level))
                self._log_object.addHandler(console)

            if self.add_to_file:
                log_file = logging.FileHandler(self.filename)
                log_file.setFormatter(self.formatter)
                log_file.addFilter(LogFilter(self.min_log_level))
                self._log_object.addHandler(log_file)
        return self._log_object

    def info(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.INFO)
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = os.path.basename(module.__file__)
            self.log_object.info(message, extra={"script": filename})

    def error(self, message, raise_exception=True,
              exception: Type[Exception] = None):
        if self.show_log:
            self.log_object.setLevel(logging.ERROR)
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = os.path.basename(module.__file__)
            self.log_object.error(message, extra={"script": filename})

        if raise_exception:
            if exception is None:
                raise Exception(message)
            else:
                raise exception(message)

    def warn(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.WARN)
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = os.path.basename(module.__file__)
            self.log_object.warning(message, extra={"script": filename})

    def debug(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.DEBUG)
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = os.path.basename(module.__file__)
            self.log_object.debug(message, extra={"script": filename})

    def deprecated(self, message):
        self.log_object.setLevel(logging.WARN)
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = os.path.basename(module.__file__)
        self.log_object.warning(message, extra={"script": filename})
