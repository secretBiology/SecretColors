"""
SecretColors 2019\n
Author: Rohit Suratekar

Revision No : 3

for more and up-to date information,
visit: https://github.com/secretBiology/SecretColors


This module provides all basic functions and main classes.

"""

from SecretColors._colors import *
from SecretColors._helpers import _warn, deprecated
import random

def color(func):
    func.__doc__ = "This is cool"
    return func


class Palette:
    def __init__(self, name: str = PALETTE_IBM, show_warning: bool = True):
        self.name = name
        self._palette = self._get_raw_palette(name, show_warning)
        self.show_warning = show_warning
        self._colors_dict = self._make_color_dict()
        self._iter_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._iter_index += 1
        try:
            return self.colors[self._iter_index - 1]
        except IndexError:
            self._iter_index = 0
            raise StopIteration

    def __str__(self):
        return "SecretColors.palette.Palette ({})".format(self.name)

    @staticmethod
    def _get_raw_palette(name: str, show_warning: bool):
        """
        :param name: Name of the color palette
        :param show_warning: If True, warnings will be shown
        :return: respective palette class
        """
        if name == PALETTE_IBM:
            return IBMPalette(show_warning)
        elif name == PALETTE_MATERIAL:
            return MaterialPalette(show_warning)
        elif name == PALETTE_BREWER:
            return ColorBrewer(show_warning)
        elif name == PALETTE_CLARITY:
            return ClarityPalette(show_warning)
        else:
            _warn("Invalid color Palette {}".format(name))
            raise Exception(
                "Invalid Color Palette. Available Palettes are: {}".format(
                    ALL_PALETTES
                ))

    def _make_color_dict(self) -> dict:
        """Simple functions which generates named dictionary of all primary
        colors
        """
        c = {}
        for x in self._palette.get_all_colors():
            c[x.name] = x
        return c

    @property
    def colors(self) -> list:
        """Returns list of base colors in current palette."""
        return [x.hex for x in self._colors_dict.values()]

    @property
    def colors_dict(self):
        """Returns named dictionary of the base colors of current palette."""
        return {x: self._colors_dict[x].hex for x in self._colors_dict.keys()}

    @property
    @deprecated("This function will be removed from next stable version. Use "
                "'palette.colors' instead")
    def get_color_list(self) -> list:
        """This is deprecated function

        Use 'palette.colors' instead
        """
        return self.colors

    @property
    @deprecated("This function will be removed from next stable version. Use "
                "'palette.colors_dict' instead")
    def get_color_dict(self) -> dict:
        """This is deprecated function

        Use 'palette.colors_dict' instead
        """
        return self.colors_dict

    def cycle(self, shade: float = None):
        """
        Makes infinite iterator out of base colors of the current palette

        >>> c = palette.cycle()
        >>> next(c) # First Color
        >>> next(c) # Second Color ...

        :param shade: If provided, iterator will be drawn in given shade
        :return: Infinite Iterator with hex
        """
        while True:
            for x in self.colors:
                yield x

    def get(self, no_of_colors: int, shade: float = None) -> list:
        """
        Gets number of colors based on default sequence. If no of colors
        requested in higher than available base palette colors, colors will
        be repeated from the beginning

        :param no_of_colors: Number of colors to get back
        :param shade: If provided, colors will be drawn in that shade
        :return: List of base colors
        """
        c = self.cycle()
        k = []
        for i in range(no_of_colors):
            k.append(next(c))
        return k

    def test(self):
        print(self.colors_dict)


def run():
    p = Palette()
    p.test()
