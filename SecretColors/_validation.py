"""Shared validation for public numeric arguments."""

import math
from numbers import Integral, Real


def count(value, name="n", *, minimum=1) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"'{name}' should be an integer")
    if value < minimum:
        raise ValueError(f"'{name}' should be at least {minimum}")
    return int(value)


def number(value, name, *, minimum=None, maximum=None) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"'{name}' should be a number")
    if not math.isfinite(value):
        raise ValueError(f"'{name}' should be finite")
    if minimum is not None and value < minimum:
        raise ValueError(f"'{name}' should be at least {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"'{name}' should be at most {maximum}")
    return float(value)
