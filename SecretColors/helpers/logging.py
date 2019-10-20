"""
SecretColors 2019
Author: Rohit Suratekar

Helper functions and classes
"""

import functools
import logging
import warnings


class Log:
    def __init__(self, show_log: bool = False,
                 options: dict = None,
                 add_to_console: bool = True,
                 add_to_file: bool = False,
                 filename: str = "script.log",
                 logging_format: str = "%(asctime)s %(filename)s : %(message)s"):
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


def deprecated(message: str = None):
    """
    Simple decorator to put deprecation warnings
    :param message: Message (if any)

    Modified from https://stackoverflow.com/questions/2536307/
    decorators-in-the-python-standard-lib-deprecated-specifically
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always',
                                  DeprecationWarning)  # turn off filter

            m = "'{}' is deprecated. ".format(function.__name__)
            if message is not None:
                m += str(message)

            warnings.warn(m, category=DeprecationWarning, stacklevel=2)

            warnings.simplefilter('default',
                                  DeprecationWarning)  # reset filter

            return function(*args, **kwargs)

        return wrapper

    return decorator


def _warn(message: str, show_warning: bool = True) -> None:
    """
    Simple function to generate warning
    :param message: Message you want to send
    :param show_warning: If False, warnings will be suppressed
    """
    if show_warning:
        m = message + "\nTo suppress warning use 'show_warning=False' in " \
                      "constructor of the palette"
        ##
        warnings.warn(m)
