#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main palette class

import random
from typing import Dict, Optional

from SecretColors.data.constants import *
from SecretColors.data.names.w3 import W3_DATA
from SecretColors.data.names.x11 import X11_DATA
from SecretColors.data.palettes import (IBMPalette, MaterialPalette, MaterialAccentPalette,
                                        ClarityPalette, ColorBrewer,
                                        ParentPalette, TableauPalette,
                                        SpectrumPalette, LatitudePalette)
from SecretColors.helpers.decorators import deprecated, color_docs
from SecretColors.helpers.logging import Log
from SecretColors.models.base import Color
from SecretColors.models.objects import ColorString, ColorTuple
from SecretColors.utils import get_complementary, color_in_between


def _get_palette(name: str) -> ParentPalette:
    name = name.strip().lower()
    if name == PALETTE_IBM:
        return IBMPalette()
    elif name == PALETTE_MATERIAL:
        return MaterialPalette()
    elif name == PALETTE_MATERIAL_ACCENT:
        return MaterialAccentPalette()
    elif name == PALETTE_CLARITY:
        return ClarityPalette()
    elif name == PALETTE_BREWER:
        return ColorBrewer()
    elif name == PALETTE_TABLEAU:
        return TableauPalette()
    elif name == PALETTE_SPECTRUM:
        return SpectrumPalette()
    elif name == PALETTE_LATITUDE:
        return LatitudePalette()
    raise ValueError(f"Unknown palette '{name}'. Currently available "
                     f"palettes: {ALL_PALETTES}")


def _validate_object(obj, cls, item_name):
    if not isinstance(obj, cls):
        raise TypeError(f"'{item_name}' should be {type(cls)}. You have "
                        f"provided {type(obj)}")


def _linspace(st, sp, n):
    """
    Mimics numpy.linspace function
    Taken from : https://stackoverflow.com/a/12334459
    """
    if n == 1:
        yield sp
        return
    h = (sp - st) / (n - 1)
    for i in range(n):
        yield st + h * i


def _param_deprecation(log: Log, item: str, **kwargs):
    if item in kwargs:
        log.deprecated(f"'{item}' argument is deprecated and it will have no "
                       f"impact on the workflow.")


class Palette:
    """
    :class:`~SecretColors.Palette` is main class of this library. It provides
    easy
    access to huge variety of color manipulations. Entire class is based on
    internal color database which has been developed based on many Design
    Systems and famous color palettes. Essentially, we made a simple utility
    which can copy and paste colors from famous color palettes ;)

    Currently, this library supports following Palettes which can be provided
    at the time of generation of Palette Object.

    * **ibm** - IBM Color Palette v2 + v1 [*Default*]
    * **material** - Google Material Design Color Palettes
    * **material-accent** - Accent colors of Google Material Design Color Palettes
    * **brewer** - ColorBrewer Color Palette
    * **clarity** - VMWare Clarity Palette
    * **tableau** - Tableau Color Palette
    * **spectrum** - Adobe Spectrum Color Palette
    * **latitude** - Flexport Latitude Color Palette

    .. code-block:: python
        :emphasize-lines: 2, 5

        from SecretColors import Palette
        p = Palette() # Generates Default color palette i.e. IBM Color Palette
        ibm = Palette("ibm") # Generates IBM Palette
        ibm.red() # Returns '#fa4d56'
        material = Palette("material") # Generates Material Palette
        material.red() # Returns '#f44336'

    You can specify *color_mode* to control color output format. Currently,
    this library supports following color modes

    * **hex** - Hex Format [*Default*]
    * **rgb** - RGB Format (values between 0 and 1)
    * **rgba** - RGB with Alpha/Transparency (values between 0 and 1)
    * **ahex** - Hex with Alpha/Transparency (Appended before hex)
    * **hexa** - Hex with Alpha/Transparency (Appended after hex)

    .. code-block:: python

        p1 = Palette() # Default Color mode (hex)
        p1.green() # '#24a148'
        p2 = Palette(color_mode="hexa")
        p2.green() # '#24a148ff'
        p3 = Palette(color_mode="ahex")
        p3.green() # '#ff24a148'
        p4 = Palette(color_mode="rgb")
        p4.green() # (0.141, 0.631, 0.282)
        p5 = Palette(color_mode="rgba")
        p5.green() # (0.141, 0.631, 0.282, 1)

    Note: *matplotlib* can accepts "hex", "rgb" or "hexa"

    """

    def __init__(self, name: str = PALETTE_IBM,
                 color_mode: str = MODE_HEX, *,
                 show_warning: bool = False,
                 seed: float = None,
                 log: Log = None, **kwargs):

        """
        Initialize the Palette class

        :param name: Name of the palette (default: ibm)
        :type name: str
        :param color_mode: Color mode which will define the output format of each color (default: hex)
        :type color_mode: str
        :param show_warning: If True, log will be shown. (default: False)
        :type show_warning: bool
        :param seed: Seed for the random number generator of this palette.
            Global :mod:`random` state is never modified.
        :param log: Log Object
        :param kwargs: Other Arguments (useful if you are subclassing)
        """

        _validate_object(name, str, "name")
        _validate_object(color_mode, str, "color_mode")

        self._palette_name = name.strip().lower()
        if log is None:
            log = Log(show_log=show_warning)
        else:
            _validate_object(log, Log, "log")

        self.log = log
        if self._palette_name not in ALL_PALETTES:
            self.log.error(f"Unknown palette '{name}'. Currently available "
                           f"palettes: {ALL_PALETTES}", exception=ValueError)
        self.color_mode = color_mode.strip().lower()
        if self.color_mode not in ALL_COLOR_MODES:
            self.log.error(f"Unknown color_mode '{color_mode}'. Currently "
                           f"available modes: {ALL_COLOR_MODES}",
                           exception=ValueError)

        _param_deprecation(self.log, "allow_gray_shades", **kwargs)

        self.log.info(f"New '{name}' palette is initialized successfully.")
        self._palette = None
        self._colors = None
        self._additional = None
        self._seed = seed
        self._rng = random.Random(seed)
        if seed is not None:
            self.log.info(f"Random seed set for : {seed}")

    def __str__(self):
        return f"Palette({self.name})"

    @property
    def _value(self) -> ParentPalette:
        if self._palette is None:
            self._palette = _get_palette(self.name)
        return self._palette

    @property
    def name(self) -> str:
        """
        :return: Name of the current palette
        :rtype: str
        """
        return self._palette_name

    @property
    def version(self):
        """
        :return: Version of palette used in SecretColors library
        :rtype: str
        """
        return self._value.get_version()

    @property
    def creator_url(self) -> str:
        """
        :return: URL citing original creator
        :rtype: str
        """
        return self._value.get_creator_url()

    @property
    def color_dict(self) -> dict:
        """ Returns dictionary of color names and their respective default
        shades
        """
        return {x.name: self._send(x.get()) for x in self.colors.values()}

    @property
    def color_list(self) -> list:
        """Returns list of all colors with their default shade
        """
        return [self._send(x.get()) for x in self.colors.values()]

    @property
    @deprecated("Use 'color_dict' instead.")
    def get_color_dict(self) -> dict:
        """Deprecated alias of :attr:`color_dict`"""
        return self.color_dict

    @property
    @deprecated("Use 'color_list' instead.")
    def get_color_list(self) -> list:
        """Deprecated alias of :attr:`color_list`"""
        return self.color_list

    def cycle(self, version: int = 1, skip_first: int = 0):
        """
        Creates infinite color cycle

        Inspiration is taken from : https://tsitsul.in/blog/coloropt/

        >>> color_cycle = Palette().cycle()
        >>> next(color_cycle) # First Color
        >>> next(color_cycle) # Next Color

        This will go infinitely. After few colors it will start repeating.
        You can get qualitative colors like following

        >>> my_colors = [next(color_cycle) for x in range(10)] # Ten colors

        You may use in the for loop. However, be careful. It is infinite
        cycle. You need to break the loop by yourself.

        ..  danger::
            This method creates inifinite number of colors. Be careful while using it in the loop

        :param skip_first: number of colors to be skipped from start. Only
            works for first 18 colors.
        :param version: color sequence version
        """
        selected = [self.red(),
                    self.blue(),
                    self.yellow(shade=30),
                    self.green(),
                    self.teal(shade=40),
                    self.magenta(),
                    self.orange(shade=30),
                    self.red(shade=30),
                    self.indigo(),
                    self.cyan(shade=30),
                    self.brown(shade=30),
                    self.green(shade=30),
                    self.gray(shade=40),
                    self.amber(shade=30),
                    self.aqua(shade=40),
                    self.red_orange(shade=40),
                    self.cerulean(shade=40),
                    self.green_light()
                    ]

        if skip_first < len(selected):
            for i in range(skip_first):
                selected.pop(0)

        # First default colors
        for c in selected:
            yield c

        # Define colors
        objs = [self.yellow, self.red, self.blue, self.green, self.teal,
                self.magenta, self.orange, self.red, self.indigo, self.cyan,
                self.brown, self.green, self.gray, self.amber, self.aqua,
                self.red_orange, self.cerulean, self.green_light]
        start_shade = 40

        # Start infinite
        initial_offset = 0
        while True:
            for c in objs:
                if c(shade=start_shade) not in selected:
                    yield c(shade=start_shade)
                    selected.append(c(shade=start_shade))
            start_shade += 5
            if start_shade > 100:
                start_shade = initial_offset + 10
                initial_offset += 1
                if initial_offset > 80:
                    initial_offset = 0
                    selected = []

    def __iter__(self):
        return iter(self.color_list)

    @property
    def seed(self):
        """Current random seed (if any)"""
        return self._seed

    @seed.setter
    def seed(self, value):
        """
        Set seed for the random number generator of this palette

        :param value: Seed value
        """
        self._seed = value
        self._rng.seed(value)
        self.log.info(f"Random seed set for : {value}")

    @property
    def colors(self) -> Dict[str, Color]:
        """
        Returns dictionary of all colorname and their respective
        :class:`~SecretColors.models.base.Color` class.
        """
        if self._colors is None:
            colors = {}
            for c, v in self._value.get_all_colors().items():
                cr = Color(c, v, self._value.get_shades())
                cr.default = self._value.get_core_shade()
                colors[c] = cr
            self._colors = colors
            self.log.info(f"All colors from '{self.name}' palette generated")
        return self._colors

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
            a = int(round(value.alpha * 255))
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

    @property
    def _additional_colors(self) -> Dict[str, Color]:
        if self._additional is None:
            additional = {}
            for p in [_get_palette(x) for x in ALL_PALETTES if x != self.name]:
                for c, v in p.get_all_colors().items():
                    if c in self.colors or c in additional:
                        continue
                    cr = Color(c, v, p.get_shades())
                    cr.default = p.get_core_shade()
                    additional[c] = cr
            self._additional = additional
            self.log.info(f"{len(additional)} colors from other palettes "
                          f"are available for lookup")
        return self._additional

    def _find(self, name: str) -> Optional[Color]:
        key = name.strip().lower()
        candidates = [key]
        if key in SYNONYM:
            candidates.append(SYNONYM[key])
        for c in candidates:
            if c in self.colors:
                return self.colors[c]
            if c in self._additional_colors:
                self.log.warn(f"Color '{c}' is not available in "
                              f"'{self.name}' palette. Using it from other "
                              f"palettes.")
                return self._additional_colors[c]
        return None

    def _extract(self, name: str) -> Color:
        color = self._find(name)
        if color is None:
            self.log.error(f"Unable to find '{name}'. Please check "
                           f"spelling error. Currently available colors: "
                           f"{list(self.colors.keys())}", exception=KeyError)
        return color

    def _shade_range(self, starting_shade, ending_shade):
        if starting_shade is None:
            starting_shade = min(self._value.get_shades())
        if ending_shade is None:
            ending_shade = max(self._value.get_shades())
        return starting_shade, ending_shade

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

        if no_of_colors < 1:
            self.log.error("'no_of_colors' should be at least 1",
                           exception=ValueError)
        if seed is not None:
            self.seed = seed
        if avoid is None:
            avoid = ["white", "black"]

        accepted_colors = [x for x in self.colors.values()
                           if x.name not in avoid]
        if len(accepted_colors) == 0:
            self.log.error("No colors left to choose from after applying "
                           "'avoid'", exception=ValueError)
        colors = [self._rng.choice(accepted_colors)
                  for _ in range(no_of_colors)]

        range_given = starting_shade is not None or ending_shade is not None
        if shade is not None and not (no_of_colors > 1 and range_given):
            shades = [shade] * no_of_colors
        else:
            low, high = sorted(self._shade_range(starting_shade,
                                                 ending_shade))
            # Prefer the palette's own shades when there are enough of them
            possible_shades = [x for x in self._value.get_shades()
                               if low <= x <= high]
            if no_of_colors <= len(possible_shades):
                shades = [self._rng.choice(possible_shades)
                          for _ in range(no_of_colors)]
            else:
                shades = [self._rng.uniform(low, high)
                          for _ in range(no_of_colors)]
            if gradient:
                shades = sorted(shades)
            if reverse:
                shades = list(reversed(shades))

        result = [c.shade(s) for c, s in zip(colors, shades)]
        if no_of_colors == 1 and not force_list:
            result = result[0]
        return self._send(result, alpha=alpha, print_colors=print_colors)

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

        pool = list(self.colors.values())
        colors = self._rng.sample(pool, 2) if len(pool) > 1 else pool * 2
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

    def _common_color(self, name, **options):
        return self._render(self._extract(name), **options)

    def _render(self, color: Color, *, shade: float = None,
                no_of_colors: int = 1, gradient: bool = True,
                alpha: float = None, starting_shade: float = None,
                ending_shade: float = None):
        if no_of_colors < 1:
            self.log.error("'no_of_colors' should be at least 1",
                           exception=ValueError)
        if no_of_colors == 1:
            if shade is None:
                shade = color.default
            return self._send(color.shade(shade), alpha=alpha)

        low, high = self._shade_range(starting_shade, ending_shade)
        if gradient:
            shades = list(_linspace(low, high, int(no_of_colors)))
        else:
            low, high = sorted((low, high))
            shades = [self._rng.uniform(low, high)
                      for _ in range(int(no_of_colors))]
        return self._send([color.shade(s) for s in shades], alpha=alpha)

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
        return Color(name, [self._extract("white").get(), data[name],
                            self._extract("black").get()],
                     [0, 50, 100])

    def get(self, color_name: str, *,
            shade: float = None, no_of_colors: int = 1,
            gradient=True, alpha: float = None,
            starting_shade: float = None, ending_shade: float = None,
            naming: str = "w3", strict_search: bool = False):
        """
        This is general methode to retrieve the arbitrary color from the
        palette. Following steps will be taken,


        * It will first check color name present in the current color palette.
        * If it is not present, it will search color name in all other available color palettes.
        * Then it will also look for common spelling variants of the color through SYNONYM constant from `SecretColors.data.constants` (for example, gray and grey). If any such synonym found, it will return that color.
        * Finally it will go through standard color names used in CSS (in case of 'w3') and X11 system (in case of 'x11') and return it.

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

        color = None if strict_search else self._find(color_name)
        if color is None:
            color = self._named_color(color_name.strip(),
                                      naming.strip().lower(), strict_search)

        return self._render(color, shade=shade, no_of_colors=no_of_colors,
                            gradient=gradient, alpha=alpha,
                            starting_shade=starting_shade,
                            ending_shade=ending_shade)

    @color_docs
    def red(self, *, shade: float = None, no_of_colors: int = 1,
            gradient=True, alpha: float = None, starting_shade: float = None,
            ending_shade: float = None):
        return self._common_color("red", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def blue(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None, starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("blue", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def green(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None, starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("green", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def magenta(self, *, shade: float = None, no_of_colors: int = 1,
                gradient=True, alpha: float = None,
                starting_shade: float = None,
                ending_shade: float = None):
        return self._common_color("magenta", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def purple(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("purple", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def cyan(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("cyan", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def teal(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("teal", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gray_cool(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("cool-gray", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gray_neutral(self, *, shade: float = None, no_of_colors: int = 1,
                     gradient=True, alpha: float = None,
                     starting_shade: float = None,
                     ending_shade: float = None):
        return self._common_color("neutral-gray", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gray(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("gray", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gray_warm(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("warm-gray", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def red_orange(self, *, shade: float = None, no_of_colors: int = 1,
                   gradient=True, alpha: float = None,
                   starting_shade: float = None,
                   ending_shade: float = None):
        return self._common_color("red-orange", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def black(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("black", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def white(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("white", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def ultramarine(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("ultramarine", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def cerulean(self, *, shade: float = None, no_of_colors: int = 1,
                 gradient=True, alpha: float = None,
                 starting_shade: float = None,
                 ending_shade: float = None):
        return self._common_color("cerulean", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def aqua(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("aqua", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def lime(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("lime", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def yellow(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("yellow", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gold(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("gold", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def orange(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("orange", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def peach(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("peach", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def violet(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("violet", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def indigo(self, *, shade: float = None, no_of_colors: int = 1,
               gradient=True, alpha: float = None,
               starting_shade: float = None,
               ending_shade: float = None):
        return self._common_color("indigo", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def pink(self, *, shade: float = None, no_of_colors: int = 1,
             gradient=True, alpha: float = None,
             starting_shade: float = None,
             ending_shade: float = None):
        return self._common_color("pink", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def purple_deep(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("deep-purple", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def blue_light(self, *, shade: float = None, no_of_colors: int = 1,
                   gradient=True, alpha: float = None,
                   starting_shade: float = None,
                   ending_shade: float = None):
        return self._common_color("light-blue", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def green_light(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("light-green", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def amber(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("amber", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def orange_deep(self, *, shade: float = None, no_of_colors: int = 1,
                    gradient=True, alpha: float = None,
                    starting_shade: float = None,
                    ending_shade: float = None):
        return self._common_color("deep-orange", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def brown(self, *, shade: float = None, no_of_colors: int = 1,
              gradient=True, alpha: float = None,
              starting_shade: float = None,
              ending_shade: float = None):
        return self._common_color("brown", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)

    @color_docs
    def gray_blue(self, *, shade: float = None, no_of_colors: int = 1,
                  gradient=True, alpha: float = None,
                  starting_shade: float = None,
                  ending_shade: float = None):
        return self._common_color("blue-gray", shade=shade,
                                  no_of_colors=no_of_colors, gradient=gradient,
                                  alpha=alpha, starting_shade=starting_shade,
                                  ending_shade=ending_shade)
