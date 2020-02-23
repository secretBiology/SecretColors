#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Decorator functions will go here

import functools
import warnings


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
