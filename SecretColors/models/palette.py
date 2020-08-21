#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# Main palette class

from typing import Dict, List, Union

import numpy as np

from SecretColors.data.constants import *
from SecretColors.data.palettes import (IBMPalette, MaterialPalette,
                                        ClarityPalette, ColorBrewer,
                                        ParentPalette)
from SecretColors.helpers.decorators import deprecated, document
from SecretColors.helpers.logging import Log
from SecretColors.models.base import Color, ColorString
from SecretColors.utils import get_complementary, color_in_between


def _get_palette(name: str) -> ParentPalette:
    name = name.strip().lower()
    if name == PALETTE_MATERIAL:
        return MaterialPalette()
    elif name == PALETTE_CLARITY:
        return ClarityPalette()
    elif name == PALETTE_BREWER:
        return ColorBrewer()
    else:
        return IBMPalette()


def _validate_object(obj, cls, item_name):
    if not isinstance(obj, cls):
        raise TypeError(f"'{item_name}' should be {type(cls)}. You have "
                        f"provided {type(obj)}")


def _param_deprecation(log: Log, item: str, **kwargs):
    if item in kwargs:
        log.deprecated(f"'{item}' argument is deprecated and it will have no "
                       f"impact on the workflow.")


class Palette:
    def __init__(self, name: str = PALETTE_IBM,
                 color_mode: str = MODE_HEX, *,
                 show_warning: bool = False,
                 seed: float = None,
                 log: Log = None, **kwargs):

        _validate_object(name, str, "name")
        _validate_object(color_mode, str, "color_mode")

        self._palette_name = name.strip().lower()
        if log is None:
            log = Log(show_log=show_warning)
        else:
            _validate_object(log, Log, "log")

        self.log = log
        self.color_mode = color_mode.strip().lower()
        if self.color_mode not in ALL_COLOR_MODES:
            self.log.error(f"Unknown color_mode '{color_mode}'. Currently "
                           f"available modes: {ALL_COLOR_MODES}",
                           exception=ValueError)

        _param_deprecation(self.log, "allow_gray_shades", **kwargs)

        self.log.info(f"New '{name}' palette is initialized successfully.")
        self._palette = None
        self._colors = None
        self.seed = seed

    @property
    def _value(self) -> ParentPalette:
        if self._palette is None:
            self._palette = _get_palette(self._palette_name)
        return self._palette

    @property
    def name(self) -> str:
        """
        :return: Name of the current palette
        """
        return self._palette_name

    @property
    def version(self):
        """
        :return: Version of palette used in SecretColors library
        """
        return self._value.get_version()

    @property
    def creator_url(self) -> str:
        """
        :return: URL citing original creator
        """
        return self._value.get_creator_url()

    @property
    def get_color_dict(self) -> dict:
        d = {}
        for x in self.colors.values():
            d[x.name] = self._send(x.get())
        return d

    @property
    def get_color_list(self) -> list:
        return [self._send(x.get()) for x in self.colors.values()]

    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_index += 1
        try:
            return self.get_color_list[self.__iter_index - 1]
        except IndexError:
            self.__iter_index = 0
            raise StopIteration

    @property
    def colors(self) -> Dict[str, Color]:
        if self._colors is None:
            colors = {}
            for c, v in self._value.get_all_colors().items():
                cr = Color(c, v, self._value.get_shades())
                cr.default = self._value.get_core_shade()
                colors[c] = cr
            self._colors = colors
            self.log.info(f"All colors from '{self.name}' palette generated")
        return self._colors

    @deprecated(
        "This function is deprecated in favour of 'color_in_between from "
        "SecretColors.utils'")
    def color_between(self, *args, **kwargs):
        self.log.deprecated("Deprecated function")
        self.log.error("Sorry! This function is removed from the Palette "
                       "Class in favour of "
                       "'color_in_between from SecretColors.utils'")

    def _send(self, colors, **kwargs) -> Union[ColorString, List[ColorString]]:
        # TODO
        return colors

    def _generate_additional_colors(self):
        # First get names of all available colors
        previous = len(self.colors.keys())
        for p in [_get_palette(x) for x in ALL_PALETTES]:
            for c, v in p.get_all_colors().items():
                if c not in self.colors.keys():
                    cr = Color(c, v, p.get_shades())
                    cr.default = p.get_core_shade()
                    self._colors[c] = cr
                    self.log.info(
                        f"Color '{c}' extracted from '{p.get_palette_name()}'")

        self.log.info(f"Total of {len(self.colors) - previous} new colors "
                      f"added to the current color list")

    def _extract(self, name: str) -> Color:
        name = name.strip().lower()
        if name not in self.colors.keys():
            self.log.warn(f"Color '{name}' not found in current palette. "
                          f"Checking if it is present in other available "
                          f"palettes.")
            self._generate_additional_colors()

        # If color is still not present, then it is an error
        if name not in self.colors.keys():
            self.log.error(f"Unable to find '{name}'. Please check "
                           f"spelling error. Currently available colors: "
                           f"{list(self.colors.keys())}", exception=KeyError)

        return self.colors[name]

    def _extract_color_list(self, name, no_of_colors: int, *,
                            starting_shade: float = None,
                            ending_shade: float = None,
                            reverse: bool = False,
                            **kwargs) -> List[ColorString]:

        # If staring and ending shades are not provided, take the ones
        # present in the default shades

        if starting_shade is None:
            starting_shade = self._value.get_shades()[-1]
        if ending_shade is None:
            ending_shade = self._value.get_shades()[0]

        shades = np.linspace(starting_shade, ending_shade, no_of_colors)
        if reverse:
            shades = reversed(shades)

        return [self._extract(name).shade(s) for s in shades]

    def random(self, no_of_colors: int = 1, *,
               shade: float = None,
               alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None,
               gradient: bool = True,
               avoid: list = None,
               reverse: bool = False,
               print_colors: bool = False, **kwargs) -> List[ColorString]:

        _param_deprecation(self.log, "ignore_gray", **kwargs)
        _param_deprecation(self.log, "force_gray", **kwargs)

        if self.seed:
            np.random.seed(self.seed)
        if avoid is None:
            avoid = ["white", "black"]
        if starting_shade is None:
            starting_shade = self._value.get_shades()[-1]
        if ending_shade is None:
            ending_shade = self._value.get_shades()[0]

        # remove the restricted colors provided by 'avoid'
        accepted_colors = []
        for x in self.colors.values():
            if x.name not in avoid:
                accepted_colors.append(x)
        # Select random colors
        colors = np.random.choice(accepted_colors, no_of_colors)
        # If shade is specified, directly return the selected colors
        if shade is not None:
            return self._send([x.shade(shade) for x in colors], alpha=alpha,
                              print_colors=print_colors)

        # Select the shade
        shades = np.random.randint(starting_shade, ending_shade, no_of_colors)
        # If gradient is true, sort the shades
        if gradient:
            shades = sorted(shades)
        if reverse:
            shades = reversed(shades)

        return self._send([x[0].shade(x[1]) for x in zip(colors, shades)],
                          alpha=alpha, print_colors=print_colors)

    def random_balanced(self, no_of_colors: int = 1) -> List[ColorString]:
        return self.random(no_of_colors, shade=self._value.get_core_shade())

    def random_gradient(self, no_of_colors: int = 3, *,
                        shade: float = None,
                        alpha: float = 1,
                        print_colors: bool = False,
                        complementary=True,
                        **kwargs) -> List[ColorString]:

        _param_deprecation(self.log, "ignore_gray", **kwargs)
        if self.seed:
            np.random.seed(self.seed)

        colors = np.random.choice(list(self.colors.values()), 2)
        if shade is None:
            shade = self._value.get_core_shade()
        colors = [x.shade(shade) for x in colors]
        if complementary:
            colors[1] = ColorString(get_complementary(colors[0]))

        if no_of_colors < 3:
            return self._send(colors[:no_of_colors], alpha=alpha,
                              print_colors=print_colors)

        no_of_colors = no_of_colors - 2
        mid_colors = color_in_between(colors[0], colors[1], no_of_colors)
        mid_colors = [ColorString(x) for x in mid_colors]
        mid_colors.insert(0, colors[0])
        mid_colors.append(colors[1])
        return self._send(mid_colors, alpha=alpha, print_colors=print_colors)

    @staticmethod
    @deprecated("This method will be removed from Palette class in future. "
                "Please use ColorMap class for this purpose")
    def cmap_from(matplotlib, hex_color_list: list):
        """Creates custom cmap from given hex_color list.
        Use :class:`~ColorMap` for more refined control. Color inputs should
        be HEX format.

        :param matplotlib: matplotlib object (https://matplotlib.org/)
        :param hex_color_list: List of colors in Hex format
        :return: *LinearSegmentedColormap* segment which can be used with
            *matplotlib* plots.
        """
        if type(hex_color_list) is not list:
            raise Exception("Please provide list of colors")
        try:
            return matplotlib.colors.LinearSegmentedColormap.from_list(
                "cMap_secret_colors", hex_color_list)
        except AttributeError:
            raise Exception("Add 'matplotlib' as a first argument. For "
                            "example, import matplotlib; palette.cmap_from("
                            "matplotlib, "
                            "palette.red());")

    def _common_color(self, name, kwargs):
        del kwargs["self"]
        color = self._extract(name)
        if kwargs["no_of_colors"] > 1:
            if kwargs["gradient"]:
                colors = self._extract_color_list(name, **kwargs)
            else:
                if self.seed:
                    np.random.seed(self.seed)
                shades = np.random.randint(self._value.get_shades()[-1],
                                           self._value.get_shades()[0],
                                           kwargs["no_of_colors"])
                colors = [color.shade(x) for x in shades]
            return self._send(colors)
        else:
            shade = color.default
            if kwargs["shade"]:
                shade = kwargs["shade"]
            return self._send(color.shade(shade))

    @document
    def red(self, *, shade: float = None, no_of_colors: int = 1,
            gradient=True, alpha: float = None, starting_shade: float = None,
            ending_shade: float = None):
        return self._common_color("red", locals())

    @document
    def blue(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None, starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("blue", locals())


def run():
    p = Palette(PALETTE_CLARITY)
    print(p.blue())
