#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main palette class

from typing import Dict, List

import numpy as np

from SecretColors.data.constants import *
from SecretColors.data.names.w3 import W3_DATA
from SecretColors.data.names.x11 import X11_DATA
from SecretColors.data.palettes import (IBMPalette, MaterialPalette,
                                        ClarityPalette, ColorBrewer,
                                        ParentPalette, TableauPalette)
from SecretColors.helpers.decorators import deprecated, document
from SecretColors.helpers.logging import Log
from SecretColors.models.base import Color
from SecretColors.models.objects import ColorString, ColorTuple
from SecretColors.utils import get_complementary, color_in_between


def _get_palette(name: str) -> ParentPalette:
    name = name.strip().lower()
    if name == PALETTE_MATERIAL:
        return MaterialPalette()
    elif name == PALETTE_CLARITY:
        return ClarityPalette()
    elif name == PALETTE_BREWER:
        return ColorBrewer()
    elif name == PALETTE_TABLEAU:
        return TableauPalette()
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
        self._seed = seed
        if self._seed:
            self.log.info(f"Random seed set for : {seed}")
            np.random.seed(self._seed)

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
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        np.random.seed(value)
        self.log.info(f"Random seed set for : {value}")

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
                       "'color_in_between from SecretColors.utils'",
                       exception=AttributeError)

    def _convert(self, value: ColorString, alpha=None):
        if alpha is not None:
            if alpha < 0 or alpha > 1:
                self.log.error("Alpha value should be between 0 to 1",
                               exception=ValueError)
            value.alpha = alpha
            if self.color_mode in [MODE_RGB, MODE_HEX]:
                self.log.warn("Alpha value ignored because color mode is set "
                              f"to {self.color_mode}. Please select "
                              f"color_mode which supports alpha values.")
        if self.color_mode == MODE_HEX:
            return value
        elif self.color_mode == MODE_RGB:
            return ColorTuple(value.rgb)
        elif self.color_mode == MODE_HEX_A or self.color_mode == MODE_AHEX:
            a = int(round(value.alpha * 100))
            if self.color_mode == MODE_HEX_A:
                n = "{}{:02x}".format(value.hex, a)
            else:
                n = "#{:02x}{}".format(a, value.hex[1:])
            cs = ColorString(n)
            cs.alpha = value.alpha
            return cs
        elif self.color_mode == MODE_RGBA:
            return ColorTuple(value.rgba)
        else:
            self.log.deprecated(f"Color mode '{self.color_mode}' is not "
                                f"implemented here. Please contact developer"
                                f" and report this bug")
        return value

    def _send(self, colors, **kwargs):
        alpha = None
        if "alpha" in kwargs.keys():
            alpha = kwargs["alpha"]
        pc = False
        if "print_colors" in kwargs.keys():
            pc = kwargs["print_colors"]
        if isinstance(colors, ColorString):
            c1 = self._convert(colors, alpha=alpha)
            if pc:
                print(c1)
            return c1
        else:
            c2 = [self._convert(x, alpha=alpha) for x in colors]
            if pc:
                print(c2)
            return c2

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
        name = name.strip()
        if name not in self.colors.keys():
            self.log.warn(f"Color '{name}' not found in current palette. "
                          f"Checking if it is present in other available "
                          f"palettes.")
            self._generate_additional_colors()

        if name not in self.colors.keys():
            if name in SYNONYM.keys():
                self.log.info(f"{SYNONYM[name]} is used instead {name}")
                return self.colors[SYNONYM[name]]

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
            starting_shade = min(self._value.get_shades())
        if ending_shade is None:
            ending_shade = max(self._value.get_shades())

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
               force_list: bool = False,
               print_colors: bool = False,
               seed=None,
               **kwargs):

        """
        Generate random color(s) from current palette.

        >>> p = Palette()
        >>> p.random() # Single random color
        >>> p.random(no_of_colors=5)  # 5 random colors
        >>> p.random(shade=20) # Random color whos shade is 20
        >>> p.random(shade=60, no_of_colors=8) # 8 random colors whose shade is 60
        >>> p.random(starting_shade=50, ending_shade=80, no_of_colors=4) #Random colors whos shades are between 50-80
        >>> p.random(no_of_colors=4, gradient=False) # 4 completely random colors with random shades
        >>> p.random(no_of_colors=40, avoid=["blue"]) # 40 random colors but do not use "blue"
        >>> p.random(no_of_colors=10, seed=100) # Generate 10 random color with seed 100
        >>> p.random(force_list=True) # List containing single random color
        >>> p.random(print_colors=True) # Print color on the console
        >>> p.random(no_of_colors=5, reverse=True) # 5 random colors whos shades should arange in darker to lighter

        :param no_of_colors: Number of colors (default: 1)
        :param shade: Shade of the color (default: palette's default). This
        will be ignored when number of colors are greater than 1 and
        starting_shade /ending_shade arguments are provided
        :param alpha: Transparency value (beteen 0-1). This will only be
        considered if palette 'color_mode' supports Alpha channel. This will
        be applied to all colors.
        :param starting_shade: Starting shade of colors (used when number of
        colors are more than 1.)
        :param ending_shade: Ending shade of colors (used when number of
        colors are more than 1.)
        :param gradient: If True, all shades (not colors) will be sorted in
        ascending order. (default: True)
        :param avoid: List of colors which should not be considered while
        generating random numbers. (default: white, black)
        :param reverse: If True, shades will be ordered in descending order
        :param force_list: If True, return type will always be list. Else
        when no of colors is 1, this function will return str/tuple.
        :param print_colors: If True, colors generated will be printed on
        the console.
        :param seed: Seed for random number generator (will override the
        global palette seed)
        :param kwargs: Other named arguments
        :return: Str/Tuple/list of random colors depending above options
        """

        _param_deprecation(self.log, "ignore_gray", **kwargs)
        _param_deprecation(self.log, "force_gray", **kwargs)

        if seed is not None:
            self.seed = seed
        if avoid is None:
            avoid = ["white", "black"]

        use_only_shade = True
        if shade is not None and starting_shade is not None:
            use_only_shade = False
        if shade is not None and ending_shade is not None:
            use_only_shade = False

        if starting_shade is None:
            starting_shade = min(self._value.get_shades())
        if ending_shade is None:
            ending_shade = max(self._value.get_shades())

        # remove the restricted colors provided by 'avoid'
        accepted_colors = []
        for x in self.colors.values():
            if x.name not in avoid:
                accepted_colors.append(x)
        # Select random colors
        colors = np.random.choice(accepted_colors, no_of_colors)
        # If shade is specified, directly return the selected colors
        if shade is not None:
            if no_of_colors == 1 and not force_list:
                return self._send(colors[0].shade(shade), alpha=alpha,
                                  print_colors=print_colors)
            return self._send([x.shade(shade) for x in colors], alpha=alpha,
                              print_colors=print_colors)

        # Select the shade
        shades = np.random.randint(starting_shade, ending_shade, no_of_colors)
        # If gradient is true, sort the shades
        if gradient:
            shades = list(sorted(shades))
        if reverse:
            shades = list(reversed(shades))

        if use_only_shade:
            shades = [shade for _ in range(len(shades))]

        if no_of_colors == 1 and not force_list:
            return self._send(colors[0].shade(shades[0]), alpha=alpha,
                              print_colors=print_colors)
        return self._send([x[0].shade(x[1]) for x in zip(colors, shades)],
                          alpha=alpha, print_colors=print_colors)

    def random_balanced(self, no_of_colors: int = 1):
        """
        Generates balanced random colors by defining shade. It essentially
        just predefines the shade to palettes default shade.

        :param no_of_colors: Number of colors
        :return: str/tuple/list based on number of colors and global
        'color_mode'
        """
        return self.random(no_of_colors, shade=self._value.get_core_shade())

    def random_gradient(self, no_of_colors: int = 3, *,
                        shade: float = None,
                        alpha: float = 1,
                        print_colors: bool = False,
                        complementary=True,
                        **kwargs):

        """
        Generates random gradient between two colors

        >>> p = Palette()
        >>> p.random_gradient() # Random gradient between two colors
        >>> p.random_gradient(no_of_colors=5) # Generates gradient between 2 colors and also adds 3 more colors between them
        >>> p.random_gradient(complementary=False) # Use totally random colors for the gradient

        :param no_of_colors: Number of in-between colors (default: 3)
        :param shade: Shades of color
        :param alpha: Alpha value between 0-1 (will ne applied to all colors)
        :param print_colors: If True, prints colors on the console
        :param complementary: If True, generates gradient between two
        complementary colors. (default: True)
        :param kwargs: Other named arguments
        :return: List of colors representing gradient
        """

        _param_deprecation(self.log, "ignore_gray", **kwargs)

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
                shades = np.random.randint(self._value.get_shades()[-1],
                                           self._value.get_shades()[0],
                                           kwargs["no_of_colors"])
                colors = [color.shade(x) for x in shades]
            return self._send(colors, **kwargs)
        else:
            shade = color.default
            if kwargs["shade"]:
                shade = kwargs["shade"]
            return self._send(color.shade(shade), **kwargs)

    def _named_color(self, name: str, system: str, strict: bool):
        both = [W3_DATA, X11_DATA]
        if system == "x11":
            both = list(reversed(both))
        if strict:
            # If it is strict search, take only named data
            data = both[0]
        else:
            # If it is not strict search, merge both names such that one
            # will get priority over another
            data = {**both[1], **both[0]}

        if name not in data.keys():
            raise KeyError(f"Unfortunately, '{name}' is not found in "
                           f"available naming datasets. Please check "
                           f"spelling mistake. This search is case sensitive"
                           f" if 'strict_search' option is enabled.")
        return Color(name, [self.white(), data[name], self.black()],
                     [0, 50, 100])

    def get(self, color_name: str, *,
            shade: float = None, no_of_colors: int = 1,
            gradient=True, alpha: float = None,
            starting_shade: float = None, ending_shade: float = None,
            naming: str = "w3", strict_search: bool = False):
        """
        This is general methode to retrieve the arbitrary color from the
        palette. Following steps will be taken,


        (1) It will first check color name present in the current color
        palette.
        (2) If it is not present, it will search color name in all other
        available color palettes.
        (3) Then it will also look for common spelling variants of the color
        through SYNONYM constant from `SecretColors.data.constants`
        (for example, gray and grey). If any such synonym found,
        it will return that color.
        (4) Finally it will go through standard color names used in CSS (in
        case of 'w3') and X11 system (in case of 'x11') and return it.

        >>> p = Palette()  # IBM Palette
        >>> p.get("red") # Default IBM Palette red color (#fa4d56)
        >>> p.get("amber") # Amber is not present in IBM so it will return from Material palette (#ffc107)
        >>> p.get("grey") # It is common variant of 'gray' so it will return regular gray (#8d8d8d)
        >>> p.get("k") # It also recognize Matplotlib's standard single character colors. (#000000)
        >>> p.get("aquamarine") # This is not present in any available
        >>> # palette. So it will look in common name database and if
        >>> # available there, it will return (#7fffd4)

        if `strict_search` option is True, it will ONLY search in the
        standard color names provided by respective naming system (w3 or x11).

        >>> p = Palette()
        >>> p.get("gray") # Standard IBM palette gray (#8d8d8d)
        >>> p.get("gray", strict_search=True) # w3 common color gray (#808080)
        >>> p.get("gray",naming="x11", strict_search=True) # common gray from 'x11' colors (#bebebe)

        Be aware, `strict_search` color name is case sensitive. So take a
        look at exact color name in respective documentations. These
        standard names have lot of variants, always refer documentation
        if getting undesirable results. Current database was updated on 27
        August 2020.

        w3: https://www.w3.org/TR/css-color-3/#svg-color
        x11: https://gitlab.freedesktop.org/xorg/app/rgb/raw/master/rgb.txt

        >>> p = Palette()
        >>> p.get("GhostWhite",naming="x11", strict_search=True) # returns #f8f8ff
        >>> p.get("ghostwhite", naming="x11", strict_search=True) # Error

        Default naming system is set to 'w3'.

        Color name found in naming system will be converted into its own
        pallet by padding white and black at the end. This will enable users
        to use all usual methods like shades, alpha, etc

        >>> p = Palette()
        >>> p.get("GhostWhite")  # returns #f8f8ff
        >>> p.get("GhostWhite", shade=80)  # returns #636366

        :param color_name: Name of the color
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
        :param naming: Naming system (currently supports w3 or x11). [
        Default: w3). If name is not found in one system, will be searched
        in another system.
        :param strict_search: If True, name will be searched only in given
        naming system. Enabling this will return the default color from
        given system. Palette colors will be ignored.
        :return: ColorString / ColorTuple according to the palette
        'color_mode'
        """

        if naming.lower().strip() not in ["w3", "x11"]:
            raise ValueError("Currently only two naming systems are "
                             "supported: 'w3' and 'x11'")

        try:
            if strict_search:
                raise KeyError()
            if color_name not in self.colors:
                self._generate_additional_colors()
            if color_name not in self.colors:
                if color_name in SYNONYM.keys():
                    color_name = SYNONYM[color_name]
                else:
                    raise KeyError()
            color = self._extract(color_name.lower().strip())
            self.log.warn(f"Color {color_name} is not available in current "
                          f"palette, searching in named list")
        except KeyError:
            color = self._named_color(color_name,
                                      naming.strip().lower(), strict_search)
            self._colors[color.name] = color

        return self._common_color(color.name, locals())

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

    @document
    def green(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None, starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("green", locals())

    @document
    def magenta(self, *, shade: float = None, no_of_colors: int = 1,
                gradient=True, alpha: float = None,
                starting_shade: float = None,
                ending_shade: float = None):
        return self._common_color("magenta", locals())

    @document
    def purple(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("purple", locals())

    @document
    def cyan(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("cyan", locals())

    @document
    def teal(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("teal", locals())

    @document
    def gray_cool(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("cool-gray", locals())

    @document
    def gray_neutral(self, *, shade: float = None, no_of_colors: int = 1,
                     gradient=True, alpha: float = None,
                     starting_shade: float = None,
                     ending_shade: float = None):
        return self._common_color("neutral-gray", locals())

    @document
    def gray(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("gray", locals())

    @document
    def gray_warm(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("warm-gray", locals())

    @document
    def red_orange(self, *, shade: float = None, no_of_colors: int = 1,
                   gradient=True, alpha: float = None,
                   starting_shade: float = None,
                   ending_shade: float = None):
        return self._common_color("red-orange", locals())

    @document
    def black(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("black", locals())

    @document
    def white(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("white", locals())

    @document
    def ultramarine(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("ultramarine", locals())

    @document
    def cerulean(self, *, shade: float = None, no_of_colors: int = 1,
                 gradient=True, alpha: float = None,
                 starting_shade: float = None,
                 ending_shade: float = None):
        return self._common_color("cerulean", locals())

    @document
    def aqua(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("aqua", locals())

    @document
    def lime(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("lime", locals())

    @document
    def yellow(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("yellow", locals())

    @document
    def gold(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("gold", locals())

    @document
    def orange(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("orange", locals())

    @document
    def peach(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("peach", locals())

    @document
    def violet(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("violet", locals())

    @document
    def indigo(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("indigo", locals())

    @document
    def pink(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("pink", locals())

    @document
    def purple_deep(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("deep-purple", locals())

    @document
    def blue_light(self, *, shade: float = None, no_of_colors: int = 1,
                   gradient=True, alpha: float = None,
                   starting_shade: float = None,
                   ending_shade: float = None):
        return self._common_color("light-blue", locals())

    @document
    def green_light(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("light-green", locals())

    @document
    def amber(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("amber", locals())

    @document
    def orange_deep(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("deep-orange", locals())

    @document
    def brown(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("brown", locals())

    @document
    def gray_blue(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("blue-gray", locals())


def run():
    p = Palette()
    print(p.random_gradient())
