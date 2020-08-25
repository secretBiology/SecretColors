#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  ColorMap related functions/classes

from SecretColors.models.palette import Palette
from SecretColors.helpers.logging import Log
import numpy as np


class ColorMap:
    def __init__(self, matplotlib,
                 palette: Palette = None,
                 log: Log = None,
                 seed=None):
        self._mat = matplotlib
        if log is None:
            log = Log()
        self.log = log
        if palette is None:
            palette = Palette()
            self.log.info(f"ColorMap will use '{palette.name}' palette")
        self._palette = palette
        self._seed = seed
        if seed is not None:
            np.random.seed(seed)
            self.log.info(f"Random seed set for : {seed}")

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        np.random.seed(value)
        self.log.info(f"Random seed set for : {value}")

    @property
    def palette(self):
        return self._palette

    @palette.setter
    def palette(self, palette: Palette):
        self._palette = palette
        self.log.info(f"ColorMap is now using '{palette.name}' palette")

    def _get_linear_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: LinearSegmentedColormap
        """
        try:
            return self._mat.colors.LinearSegmentedColormap.from_list(
                "secret_color", color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def _get_listed_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: ListedColormap
        """
        try:
            return self._mat.colors.ListedColormap(color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def _derive_map(self, color_list: list,
                    is_qualitative=False,
                    is_reversed=False):
        """
        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :param is_reversed: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """

        if is_reversed:
            color_list = [x for x in reversed(color_list)]
        if is_qualitative:
            return self._get_listed_segment(color_list)
        else:
            return self._get_linear_segment(color_list)

    def from_list(self, color_list: list, is_qualitative: bool = False,
                  is_reversed=False):
        """
        You can create your own colormap with list of own colors

        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :param is_reversed: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """
        return self._derive_map(color_list, is_qualitative, is_reversed)


def run():
    print("here")
