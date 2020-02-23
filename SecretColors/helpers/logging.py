#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Logging util class


import logging

LOGGING_FORMAT = "%(asctime)s %(filename)s : %(message)s"


class Log:
    def __init__(self, show_log: bool = False,
                 options: dict = None,
                 add_to_console: bool = True,
                 add_to_file: bool = False,
                 filename: str = "script.log",
                 logging_format: str = LOGGING_FORMAT):
        self.show_log = show_log
        self.formatter = logging.Formatter(logging_format)
        self.add_to_console = add_to_console
        self.add_to_file = add_to_file
        self.filename = filename
        self._log_object = None

    @property
    def log_object(self):
        if self._log_object is None:
            self._log_object = logging.getLogger("log")
            if self.add_to_console:
                console = logging.StreamHandler()
                console.setFormatter(self.formatter)
                self._log_object.addHandler(console)

            if self.add_to_file:
                log_file = logging.FileHandler(self.filename)
                log_file.setFormatter(self.formatter)
                self._log_object.addHandler(log_file)
        return self._log_object

    def info(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.INFO)
            self.log_object.info(message)

    def debug(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.DEBUG)
            self.log_object.info(message)

    def error(self, message, raise_exception=True):
        if self.show_log:
            self.log_object.setLevel(logging.ERROR)
            self.log_object.error(message)

        if raise_exception:
            raise Exception(message)

    def warn(self, message):
        if self.show_log:
            self.log_object.setLevel(logging.WARN)
            self.log_object.warning(message)
