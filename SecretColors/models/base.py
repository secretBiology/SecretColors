#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main classes classes related to color and shades will go in this file

import collections

from SecretColors.helpers.logging import Log
from SecretColors.models.objects import ColorString
from SecretColors.utils import color_in_between


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
                 left: str = "#ffffff", right: str = "#000000",
                 default: float = 50):
        self.name = name
        self._raw_values = values
        self._shades = shades
        if log is None:
            log = Log()
        self.log = log
        self._values = None
        self.left = left  # Left hand end
        self.right = right  # Right hand end
        self.default = default  # Default shade

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
            self.log.error("Shade value should be in between 0-100",
                           exception=ValueError)

        self.log.debug(f"Color {self.name} is generated with {len(values)} "
                       f"values")

    def __repr__(self):
        return f"Color({self.name})"

    def get_all_shades(self):
        return self._shades

    @property
    def values(self):
        if self._values is None:
            v = []
            for c, s in zip(self._raw_values, self._shades):
                v.append(_RawColor(c, s, self.log))
            # Add left color if 0 is not included
            if min(self._shades) > 0:
                v.append(_RawColor(self.left, 0, self.log))
                self.log.debug(f"Added left color to {self.name}")
            # Add right color if 100 is not included
            if max(self._shades) < 100:
                self.log.debug(f"Added right color to {self.name}")
                v.append(_RawColor(self.right, 100, self.log))
            v = sorted(v)
            self._values = v
        return self._values

    def get(self) -> ColorString:
        return self.shade(self.default)

    def shade(self, value: float) -> ColorString:
        self.log.debug(f"Extracting shade '{value}' from '{self.name}'")

        if value < 0 or value > 100:
            self.log.error("Shade should be between 0-100",
                           exception=ValueError)

        for i, s in enumerate(self.values):
            if s.shade == value:
                return ColorString(s.hex)
            if s.shade > value:
                left = self.values[i - 1]
                right = s
                idx = (value - left.shade) * 100 / (right.shade - left.shade)
                idx = round(idx)
                colors = color_in_between(left.hex, right.hex, 99)
                colors.insert(0, left.hex)
                colors.append(right.hex)
                return ColorString(colors[idx])

        self.log.error(f"Something went wrong with shade {value}. Please "
                       f"report it on GitHub", exception=ValueError)
