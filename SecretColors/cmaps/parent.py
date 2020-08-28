#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

from SecretColors.models.palette import Palette
from SecretColors.helpers.logging import Log
import numpy as np


class ColorParent:
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
    def data(self):
        raise NotImplementedError

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

    def _get_colors(self, key: str, no_of_colors: int, backup: str,
                    staring_shade, ending_shade):

        if no_of_colors < 2:
            self.log.error("Minimum of 2 colors are required for generating "
                           "Colormap", exception=ValueError)
        colors = None
        # First check if for given combinations of parameters, colors are
        # available
        if self.data is not None:
            if key in self.data:
                if str(no_of_colors) in self.data[key]:
                    colors = self.data[key][str(no_of_colors)]
                    self.log.info("Colormap for given combination found")

        if colors is None:
            self.log.info("Colormap for given combination not found.")
            self.log.info("Searching standard colors")
            # Just make request for the color so that additional colors will
            # be added to palette
            self.palette.get(backup)

        if (staring_shade is not None or
                ending_shade is not None or
                colors is None):
            self.log.warn("Overriding the available standard Colormaps "
                          "because starting_shade or ending_shade is provided")

            if staring_shade is None:
                staring_shade = min(self.palette.colors[
                                        backup].get_all_shades())
            if ending_shade is None:
                ending_shade = max(
                    self.palette.colors[backup].get_all_shades())

            return self.palette.get(backup, no_of_colors=no_of_colors,
                                    starting_shade=staring_shade,
                                    ending_shade=ending_shade)

        return colors

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

    def greens(self, starting_shade: float = None, ending_shade: float = None,
               no_of_colors: int = 10,
               is_qualitative: bool = False, is_reversed=False):
        """
        :param starting_shade: Minimum shade
        :param ending_shade: Maximum shade
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :param is_reversed: Reverses the order of color in Colormap
        :return: Matplotlib cmap wrapper
        """

        colors = self._get_colors('green', 10, 'green',
                                  starting_shade,
                                  ending_shade)
        return self._derive_map(colors, is_qualitative, is_reversed)

    def reds(self, starting_shade: float = None, ending_shade: float = None,
             no_of_colors: int = 10,
             is_qualitative: bool = False, is_reversed=False):
        """
        :param starting_shade: Minimum shade
        :param ending_shade: Maximum shade
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :param is_reversed: Reverses the order of color in Colormap
        :return: Matplotlib cmap wrapper
        """

        if starting_shade is None:
            starting_shade = min(self.palette.colors['red'].get_all_shades())
        if ending_shade is None:
            ending_shade = max(self.palette.colors['red'].get_all_shades())

        return self._derive_map(self.palette.red(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative, is_reversed)
