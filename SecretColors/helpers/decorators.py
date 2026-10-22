#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Decorator functions will go here

import functools
import inspect
import warnings
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


REMOVAL = "It will be removed in the next major release."


def deprecated_aliases(**aliases: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Accept old keyword spellings without hiding the canonical signature."""
    def decorate(func: Callable[P, R]) -> Callable[P, R]:
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            supplied = signature.bind_partial(*args, **{
                k: v for k, v in kwargs.items() if k not in aliases}).arguments
            for old, new in aliases.items():
                if old in kwargs:
                    if new in supplied or new in kwargs:
                        raise TypeError(f"Use either '{old}' or '{new}', not both")
                    warnings.warn(f"'{old}' is deprecated; use '{new}' instead "
                                  f"in {func.__qualname__}(..., {new}=...). {REMOVAL}",
                                  DeprecationWarning, stacklevel=2)
                    kwargs[new] = kwargs.pop(old)
            return func(*args, **kwargs)
        return wrapper
    return decorate


def deprecated(message: str = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Simple decorator to put deprecation warnings
    :param message: Message (if any)

    Modified from https://stackoverflow.com/questions/2536307/
    decorators-in-the-python-standard-lib-deprecated-specifically
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            m = "'{}' is deprecated. ".format(function.__name__)
            if message is not None:
                m += str(message)
            m += " " + REMOVAL

            warnings.warn(m, category=DeprecationWarning, stacklevel=2)
            return function(*args, **kwargs)

        return wrapper

    return decorator


def _sample_color(shade: float = None,
                  n: int = 1,
                  gradient=True,
                  alpha: float = None,
                  start: float = None,
                  end: float = None):
    """
    The main function for 'SECRET' color

    >>> p.SECRET() # Prints default SECRET color from the palette

    :param shade: Color Shade (between 0-100). Default will be based on the
        Palette used. If that is not available 50 will be used.
    :param n: Number of colors (default: 1)
    :param gradient: If True, if number of colors are greater than 1,
        then will be arranged in ascending order of their shade value
    :param alpha: Transparency (between 0-1). Only works in selected
        color_modes : hexa, ahex, rgba
    :param start: If number of colors are more than 1, you can use
        this to define the starting shade of the color. This does not work when
        number of colors is 1
    :param end: If number of colors are more than 1, you can use
        this to define the ending shade of the color. This does not work when
        number of colors is 1
    :param space: Interpolation space: 'rgb' (default), 'lab' or 'lch'.
        RGB preserves the historical shade quantization.
    :return: ColorString (special string class)
    """
    pass


def color_docs(func: Callable[P, R]) -> Callable[P, R]:
    doc = _sample_color.__doc__
    doc = doc.replace("SECRET", func.__name__)
    func.__doc__ = doc

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        return func(*args, **kwargs)

    return wrap


def _sample_cmap(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
    """
    This is special method available for :class:`SecretColors.cmaps.SECRETMAP`
    class. This function provides easy access to `SNAME` colormap. You can
    also use :func:`~SecretColors.cmaps.SECRETMAP().get`
    method to achieve the same result.

    ..  code-block:: python
        :emphasize-lines: 3

        from SecretColors.cmaps import SECRETMAP
        cm = SECRETMAP()
        plt.imshow(data, cmap=cm.METHOD_NAME()) # Or cm.get('SNAME')
        plt.show()

    :param n: No of colors
    :param discrete: If True, ColorMap will be qualitative
    :param reverse: If True, ColorMap will be reversed
    :return: Matplotlib `LinearSegmentedColormap` or `ListedColormap` based
        on the options provided. You can use this directly in the matplotlib
    """
    pass


def cmap_docs(name, value) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func):
        doc = _sample_cmap.__doc__
        doc = doc.replace("SECRETMAP", name)
        doc = doc.replace("SNAME", value)
        doc = doc.replace("METHOD_NAME", func.__name__)
        func.__doc__ = doc

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return decorator
