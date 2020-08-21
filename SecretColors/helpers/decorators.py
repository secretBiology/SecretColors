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


def _sample_doc(shade: float = None,
                no_of_colors: int = 1,
                gradient=True,
                alpha: float = None,
                starting_shade: float = None,
                ending_shade: float = None):
    """
    The main function for 'SECRET' color

    >>> p.SECRET() # Prints default SECRET color from the palette

    :param shade: Color Shade (between 0-100). Default will be based on the
        Palette used. If that is not available 50 will be used.
    :param no_of_colors: Number of colors (default: 1)
    :param gradient: If True, if number of colors are greater than 1,
        then will be arranged in ascending order of their shade value
    :param alpha: Transparency (between 0-1). Only works in selected
        color_modes : hexa, ahex, rgba, hsla
    :param starting_shade: If number of colors are more than 1, you can use
        this to define the starting shade of the color. This does not work when
        number of colors is 1
    :param ending_shade: If number of colors are more than 1, you can use
        this to define the ending shade of the color. This does not work when
        number of colors is 1
    :return: ColorString (special string class)
    """
    pass


def document(func):
    doc = _sample_doc.__doc__
    doc = doc.replace("SECRET", func.__name__)
    func.__doc__ = doc
    return func
