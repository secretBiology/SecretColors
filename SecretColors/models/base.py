#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main classes will go in this file

import collections
import math

from SecretColors.helpers.logging import Log
from SecretColors.models.objects import ColorString
from SecretColors.utils import color_in_between

test = ['#2c080a', '#570408', '#750e13', '#a51920', '#da1e28',
        '#fb4b53', '#ff767c', '#ffa4a9', '#fcd0d3', '#fff0f1']


class _RawColor:
    """
    Simple class to get input from raw data
    """

    def __init__(self, color_hex: str, shade: float, log: Log = None):
        self.hex = color_hex
        self.shade = shade
        if log is None:
            log = Log()
        self.log = log
        self.log.debug(f"RawColor generated with value {self.hex} and shade "
                       f"{self.shade}")

    def __gt__(self, other):
        if isinstance(other, _RawColor):
            return self.shade > other.shade
        return self.shade > other

    def __lt__(self, other):
        if isinstance(other, _RawColor):
            return self.shade < other.shade
        return self.shade < other

    def __eq__(self, other):
        if isinstance(other, _RawColor):
            return self.shade == other.shade
        return self.shade == other

    def __ge__(self, other):
        if isinstance(other, _RawColor):
            return self.shade >= other.shade
        return self.shade >= other

    def __le__(self, other):
        if isinstance(other, _RawColor):
            return self.shade <= other.shade
        return self.shade <= other

    def __repr__(self):
        return f"_RawColor({self.hex}, {self.shade})"


class Color:
    def __init__(self, name: str, values: list,
                 shades: list, log: Log = None,
                 left: str = "#ffffff", right: str = "#000000"):
        self.name = name
        self._raw_values = values
        self._shades = shades
        if log is None:
            log = Log()
        self.log = log
        self._values = None
        self.left = left  # Left hand end
        self.right = right  # Right hand end

        if not isinstance(shades, collections.abc.Iterable) or isinstance(
                values, str):
            self.log.error("Both values and shades should be iterator. Do "
                           "not pass value as a string.", exception=ValueError)

        if len(values) != len(shades):
            self.log.error("Color values and shades should have same number "
                           "of items", exception=ValueError)

        if len(values) == 0:
            self.log.error("There should be at least one value in the list",
                           exception=ValueError)

        if min(shades) < 0 or max(shades) > 100:
            self.log.error("Shade value should be between 0-100",
                           exception=ValueError)

        self.log.debug(f"Color {self.name} is generated with {len(values)} "
                       f"values")

    @property
    def values(self):
        if self._values is None:
            v = []
            for c, s in zip(self._raw_values, self._shades):
                v.append(_RawColor(c, s, self.log))
            # Add left color if 0 is not included
            if min(self._shades) > 0:
                v.append(_RawColor(self.left, 0, self.log))
            # Add right color if 100 is not included
            if max(self._shades) < 100:
                v.append(_RawColor(self.right, 100, self.log))
            v = sorted(v)
            self._values = v
        return self._values

    def shade(self, value: float) -> ColorString:
        if value < 0 or value > 100:
            self.log.error("Shade should be between 0-100",
                           exception=ValueError)
        dec, top = math.modf(value)
        top = int(top)
        dec = round(dec * 100)
        left_c = self.values[0]
        right_c = self.values[-1]
        for i, s in enumerate(self.values):
            if top == s and dec == 0:
                return ColorString(s.hex)
            elif top == s:
                left_c = s
                right_c = self.values[i + 1]
                break
            elif s > top:
                left_c = self.values[i - 1]
                right_c = s
                break

        # TODO: Implement properly
        bks = right_c.shade - left_c.shade
        print(bks, top - left_c.shade)
        cols = color_in_between(left_c.hex, right_c.hex, bks)
        cols.insert(0, left_c.hex)
        cols.append(right_c.hex)
        # First get colors for 'top'
        idx = top - left_c.shade
        c1 = cols[top - 1]
        if dec == 0:
            return ColorString(c1)
        # Now get smaller section of color and do divisions
        c2 = cols[top]
        col2 = color_in_between(c1, c2, 98)
        col2.insert(0, c1)
        col2.append(c2)
        return ColorString(col2[dec - 1])


def run():
    c = Color("red", test, list(range(0, 100, 10)))
    c2 = Color("test", ["#ffffff", "#000000"], [0, 100])
    c2.shade(50)
