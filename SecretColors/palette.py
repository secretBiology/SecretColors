"""
SecretColors 2019\n
Author: Rohit Suratekar

for more and up-to date information,
visit: https://github.com/secretBiology/SecretColors


This module provides all basic functions and main classes.

"""

import random

from SecretColors.__colors import *
from SecretColors.utils import *
from SecretColors.utils import _warn


class Palette:
    """Base Palette Class

    Currently this library supports following Palettes which can be provided
    at the time of generation of Palette Object.

    * **ibm** - IBM Color Palette v2 + v1 [*Default*, for now]
    * **material** - Google Material Design Color Palettes
    * **brewer** - ColorBrewer Color Palette
    * **clarity** - VMWare Clarity Palette

    >>> from SecretColors import Palette
    >>> p = Palette() # Generates Default color palette i.e. IBM Color Palette
    >>> ibm = Palette("ibm") # Generates IBM Palette
    >>> ibm.red() # Returns '#fb4b53'
    >>> material = Palette("material") # Generates Material Palette
    >>> material.red() # Returns '#f44336'

    You can specify *color_mode* to control color output format. Currently
    this library supports following color modes

    * **hex** - Hex Format [*Default*]
    * **rgb** - RGB Format (values between 0 to 1)
    * **hsl** - HSL Format (values between 0 to 1)
    * **rgba** - RGB with Alpha/Transparency (values between 0 to 1)
    * **ahex** - Hex with Alpha/Transparency (Appended before hex)
    * **hexa** - Hex with Alpha/Transparency (Appended after hex)
    * **hsla** - HSL with Alpha/Transparency (values between 0 to 1)
    * **rgb255** - RGB Format (values between 0 to 255)

    >>> p1 = Palette() # Default Color mode (hex)
    >>> p1.green() # '#24a148'
    >>> p2 = Palette(color_mode="hexa")
    >>> p2.green() # '#24a148ff'
    >>> p3 = Palette(color_mode="ahex")
    >>> p3.green() # '#ff24a148'
    >>> p4 = Palette(color_mode="rgb")
    >>> p4.green() # (0.141, 0.631, 0.282)
    >>> p5 = Palette(color_mode="rgba")
    >>> p5.green() # '(0.141, 0.282, 0.631, 1)'

    Note: *matplotlib* can accepts "hex", "rgb" or "hexa"

    In future, default color palette will be replaced with custom color
    palette which should take best colors from all palettes and make even
    better color palette.


    """

    def __init__(self, name: str = PALETTE_IBM, allow_gray_shades: bool = True,
                 show_warning: bool = True, color_mode: str = MODE_HEX):
        """Generates Palette Object

        :param name: Name of the palette
        :param allow_gray_shades: If True, shades of gray, white and black
            are included in the gradient formation or random color generation
        :param show_warning: If True, warnings will be shown
        :param color_mode: Color Mode in which output will be provided
        """

        self.__palette = self.__get_palette(name.strip().lower(), show_warning)
        self.__colors = {}
        for c in self.__palette.get_all_colors():
            self.__colors[c.name] = c

        self.__allow_gray = allow_gray_shades
        self.__iter_index = 0
        self.__show_warning = show_warning
        self.color_mode = color_mode

    @staticmethod
    def __get_palette(name: str, show_warning: bool) -> ParentPalette:
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
            raise Exception(
                "Invalid Color Palette. Available Palettes are: {}".format(
                    ALL_PALETTES
                ))

    def __all_colors(self) -> dict:
        """
        :return: Dictionary of colors from all palettes
        """
        d = {}
        for p in ALL_PALETTES:
            for c in self.__get_palette(p,
                                        self.__show_warning).get_all_colors():
                d[c.name] = c
        return d

    @property
    def name(self):
        """
        :return: Name of the current palette
        """
        return self.__palette.get_palette_name()

    @property
    def version(self):
        """
        :return: Version of the current palette in THIS library. Original
            version can be different from this.
        """
        return self.__palette.get_version()

    @property
    def creator_url(self):
        """
        :return: URL citing original creator
        """
        return self.__palette.get_creator_url()

    @property
    def get_color_dict(self) -> dict:
        """Returns dictionary of colors available from current palette

        >>> p = Palette()
        >>> p.get_color_list # {'red': '#fb4b53', 'magenta': '#ee538b'...}

        Similar to :func:`~get_color_list` but outputs as a dictionary

        :return: Dictionary of colors from the palette with their names as a key
        """
        d = {}
        for x in self.__colors.values():
            if self.__allow_gray:
                d[x.name] = x.hex
            else:
                if x.type != TYPE_GRAY:
                    d[x.name] = x.hex
        return d

    def test(self):
        return self.__colors["red"]

    @property
    def get_color_list(self) -> list:
        """Returns list of colors available from current palette

        >>> p = Palette()
        >>> p.get_color_list # ['#fb4b53', '#ee538b', '#a66efa'...]

        Similar to :func:`~get_color_dict` but outputs as a list

        :return: List of all standard colors
        """
        d = []
        for x in self.__colors.values():
            if self.__allow_gray:
                d.append(x.hex)
            else:
                if x.type != TYPE_GRAY:
                    d.append(x.hex)
        return d

    def __convert(self, hex_name: str, alpha: float = 1,
                  print_colors: bool = False):
        """
        Converts Hex into palette's current color-mode

        :param hex_name: Name of color in Hex format
        :param print_colors: If True, prints the color
        :return: color in palette's color mode
        """
        if alpha != 1 and (
                self.color_mode not in [MODE_AHEX, MODE_HSLA, MODE_RGBA,
                                        MODE_HEX_A]):
            _warn("Transparency will be ignored. Please use color mode which "
                  "supports transparency.")

        def __format_color():
            if self.color_mode == MODE_HEX:
                return hex_name
            elif self.color_mode == MODE_RGB:
                return hex_to_rgb(hex_name)
            elif self.color_mode == MODE_HSL:
                return hex_to_hsl(hex_name)
            elif self.color_mode == MODE_RGBA:
                return hex_to_rgba(hex_name, alpha)
            elif self.color_mode == MODE_AHEX:
                return hex_to_ahex(hex_name, alpha)
            elif self.color_mode == MODE_HSLA:
                return hex_to_hsla(hex_name, alpha)
            elif self.color_mode == MODE_HEX_A:
                return hex_to_hex_a(hex_name, alpha)
            elif self.color_mode == MODE_RGB255:
                return hex_to_rgb255(hex_name)
            else:
                raise Exception("Invalid Color Mode or this color mode is not "
                                "supported yet")

        c = __format_color()
        if print_colors:
            print(c)
        return c

    def __get_color(self, name: str):
        """
        Get specific color from the palette based on its name. If color is
        not available in the current palette, it will search in other palette.

        :param name: Name of the colors
        :return: Color Object
        """
        try:
            return self.__colors[name.lower().strip()]
        except KeyError:
            _warn("Current palette do not have '{}'. Using it from other "
                  "palettes. ".format(name), self.__show_warning)
            return self.__all_colors()[name.lower().strip()]

    @staticmethod
    def __random_pick(color: Color,
                      shade: float = None,
                      no_of_colors: int = 1,
                      gradient=False,
                      alpha: float = 1,
                      starting_shade: float = 0,
                      ending_shade: float = 100):
        """
        Picks up shade from the palette

        :param color: Color Object
        :param shade: Shade
        :param no_of_colors: Number of colors
        :param gradient: If True, arranges colors in gradient instead random
        :param starting_shade: starting shade
        :param ending_shade: ending shade
        :return: Color/List of colors (in Hex)
        """
        if shade is not None and no_of_colors == 1:
            return color.shade(shade)
        else:

            if gradient:
                k = color.gradient(starting_shade=starting_shade,
                                   ending_shade=ending_shade,
                                   no_of_colors=no_of_colors)
            else:
                k = color.random_between(starting_shade,
                                         ending_shade,
                                         no_of_colors)
            if len(k) == 1:
                return k[0]
            else:
                return k

    def __random(self, no_of_colors: int = 1,
                 shade: float = None,
                 starting_shade: float = 0,
                 end_shade: float = 100,
                 alpha: float = 1,
                 force_gray: bool = False):

        box = [x for x in self.__colors.values() if x.type != TYPE_GRAY]

        if force_gray:
            box = [x for x in self.__colors.values()]

        if no_of_colors == 1:
            return self.__random_pick(random.sample(box, 1)[0],
                                      shade=shade,
                                      alpha=alpha,
                                      starting_shade=starting_shade,
                                      ending_shade=end_shade)
        elif no_of_colors < len(box):
            return_box = []
            for c in random.sample(box, no_of_colors):
                return_box.append(
                    self.__random_pick(c, shade=shade,
                                       alpha=alpha,
                                       starting_shade=starting_shade,
                                       ending_shade=end_shade))

            return return_box

        else:
            extra_box = []
            for i in range(no_of_colors):
                c = random.sample(box, 1)[0]
                extra_box.append(
                    self.__random_pick(c, shade=shade,
                                       alpha=alpha,
                                       starting_shade=starting_shade,
                                       ending_shade=end_shade))

            return extra_box

    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_index += 1
        try:
            return self.get_color_list[self.__iter_index - 1]
        except IndexError:
            self.__iter_index = 0
            raise StopIteration

    def random(self, no_of_colors: int = 1,
               shade: float = None,
               starting_shade: float = 0,
               ending_shade: float = 100,
               alpha: float = 1,
               force_gray: bool = False,
               print_colors: bool = False):
        """Generates random color.

        First it will try to pick color existed in
        the given palette. However, with other options, you can refine the
        desired output. By default, shades of gray, white and black colors
        are excluded from random function.


        >>> p = Palette()
        >>> p.random() # '#90dbe9'
        >>> p.random(no_of_colors=3) # ['#8fca39', '#64a0fe', '#7430b6']
        >>> p.random(no_of_colors=2, shade=20) # ['#b3e6ff', '#c2dbf4']

        :param no_of_colors: Number of Colors
        :param shade: Shade of Color
        :param starting_shade: Starting Shade
        :param ending_shade: End Shade
        :param alpha: Transparency (will be used only in an appropriate mode)
        :param force_gray: If True, it will add grays, whites and blacks
            while picking random colors
        :param print_colors: If True, prints color generated
        :return: Color/List of colors
        """
        return self.__return_colors(
            self.__random(no_of_colors=no_of_colors,
                          shade=shade,
                          starting_shade=starting_shade,
                          end_shade=ending_shade,
                          alpha=alpha,
                          force_gray=force_gray), alpha=alpha,
            print_colors=print_colors)

    def random_balanced(self, no_of_colors: int = 1,
                        print_colors: bool = False):
        """Returns 'balanced' colors

        Essentially :func:`~random` function with shade=50. Shade 50 colors are
        generally neutral and visually appealing. Hence use this function for
        regular analysis instead :func:`~random` . Any parameter passed
        as a 'shade' will be ignored

        :param no_of_colors: Number of colors
        :param print_colors: If True, colors will be printed
        :return: Color/List of colors
        """
        return self.random(shade=50, no_of_colors=no_of_colors,
                           print_colors=print_colors)

    def __common_color(self, name: str,
                       shade: float = None,
                       no_of_colors: int = 1,
                       gradient=False,
                       starting_shade: float = 0,
                       ending_shade: float = 100,
                       alpha: float = 1):
        c = self.__get_color(name)

        if no_of_colors > 1 and shade is not None:
            _warn("Shade will be ignored when number of colors are more than 1")

        if shade is None:
            shade = c.core_shade_value

        return self.__random_pick(c,
                                  no_of_colors=no_of_colors,
                                  shade=shade,
                                  gradient=gradient,
                                  alpha=alpha,
                                  starting_shade=starting_shade,
                                  ending_shade=ending_shade
                                  )

    def random_gradient(self, no_of_colors: int = 1, shade: float = None,
                        complementary=True, alpha: float = 1,
                        print_colors: bool = False):
        """Generates random gradient between two colors.

        By default it uses two random complementary colors. However you can
        change it to make complete random by setting *complementary* to False

        >>> p = Palette()
        >>> p.random_gradient(no_of_colors=3) # ['#03b2c6', '#646364', '#c51603']

        :param alpha: Transparency (between 0 to 1)
        :param no_of_colors: Number of colors in your gradient
        :param shade: Keep shade value between 0 to 100 if you want random
            colors from specific shade
        :param complementary: If True, two colors picked will be
            complementary to each other
        :param print_colors: If True, Colors will be printed
        :return: List of colors
        """

        if complementary:
            r1 = self.__random(shade=shade)
            r2 = get_complementary(r1)
        else:
            r1, r2 = self.__random(shade=shade, no_of_colors=2)
        return self.color_between(r1, r2, no_of_colors,
                                  include_both=True, alpha=alpha,
                                  print_colors=print_colors)

    def color_between(self, color1_hex: str, color2_hex: str, no_of_colors: int,
                      alpha: float = 1, include_first: bool = False,
                      include_last: bool = False, include_both: bool =
                      False, print_colors: bool = False) -> list:

        """Generates list of colors between given colors.

        This can be used to make gradients as well. :func:`~random_gradient`
        uses this function to generate gradient after selecting random colors.

        >>> p = Palette()
        >>> p.color_between(p.red(),p.yellow(), no_of_colors=1) # ['#d66d38']

        Important : Color inputs should be in HEX format

        :param color1_hex: Transparency (between 0 to 1)
        :param color2_hex: Starting color
        :param no_of_colors: End Color
        :param alpha: Total number of colors
        :param include_first: Keep True, if you want to include starting
            color in final list
        :param include_last: Keep True, if you want to include end color in
            final list
        :param include_both: Keep True, if you want to include both starting
            and end colors in your final list. If kept True, it will
            override`include_first` and `include_last` values
        :param print_colors: If True, Colors will be printed
        :return: List of colors
        """

        if include_both and no_of_colors < 2:
            raise Exception("If you want to include both colors, number of "
                            "colors should be at least 2")

        if no_of_colors == 1:
            if include_first:
                return self.__return_colors([color1_hex], alpha=alpha,
                                            print_colors=print_colors)
            elif include_last:
                return self.__return_colors([color2_hex], alpha=alpha,
                                            print_colors=print_colors)

        if no_of_colors == 2 and (include_both or (include_first and
                                                   include_last)):
            return self.__return_colors([color1_hex, color2_hex],
                                        alpha=alpha, print_colors=print_colors)

        adjust_factor = 0
        if include_both:
            adjust_factor -= 2
        else:
            if include_first:
                adjust_factor -= 1
            if include_last:
                adjust_factor -= 1

        c = color_in_between(color1_hex, color2_hex,
                             no_of_colors + adjust_factor)

        if include_both or (include_first and include_last):
            c.insert(0, color1_hex)
            c.append(color2_hex)
        else:
            if include_first:
                c.insert(0, color1_hex)
            elif include_last:
                c.append(color2_hex)
        return self.__return_colors(c, alpha=alpha, print_colors=print_colors)

    def __return_colors(self, obj, alpha: float = 1,
                        print_colors: bool = False):
        """ Returns Colors with provided mode
        :param obj: Single string or list of strings
        :param alpha: Transparency
        :param print_colors: If True, color will be printed
        :return: Colors according to color mode
        """
        if type(obj) is str:
            return self.__convert(obj, alpha=alpha, print_colors=print_colors)
        elif type(obj) is list:
            return [self.__convert(x, alpha=alpha, print_colors=print_colors)
                    for x in obj]
        else:
            _warn("Unable to convert current object")
            return obj

    @staticmethod
    def cmap_from(matplotlib, hex_color_list: list):
        """Creates custom cmap from given hex_color list.

        Use :class:`~ColorMap` for more refined control. Color inputs should
        be HEX format.

        >>> import matplotlib
        >>> p =  Palette()
        >>> color_list = [p.aqua(), p.yellow(), p.gray()]
        >>> p.cmap_from(matplotlib, color_list) # <matplotlib.colors.LinearSegmentedColormap object at 0x000002623B6A1898>

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

    def red(self,
            shade: float = None,
            no_of_colors: int = 1,
            gradient=True,
            alpha: float = 1,
            starting_shade: float = 0,
            ending_shade: float = 100):
        """
        Red Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner        
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("red",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def blue(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Blue Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("blue",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def green(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Green Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("green",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def magenta(self,
                shade: float = None,
                no_of_colors: int = 1,
                gradient=True,
                alpha: float = 1,
                starting_shade: float = 0,
                ending_shade: float = 100):
        """
        Magenta Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("magenta",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def purple(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               alpha: float = 1,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Purple Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("purple",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def cyan(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Cyan Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("cyan",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def teal(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Teal Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("teal",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gray_cool(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  alpha: float = 1,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Cool Gray Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("cool-gray",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gray_neutral(self,
                     shade: float = None,
                     no_of_colors: int = 1,
                     gradient=True,
                     alpha: float = 1,
                     starting_shade: float = 0,
                     ending_shade: float = 100):
        """
        Neutral Gray Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("neutral-gray",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gray(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Gray Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("gray",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gray_warm(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  alpha: float = 1,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Warm Gray Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("warm-gray",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def red_orange(self,
                   shade: float = None,
                   no_of_colors: int = 1,
                   gradient=True,
                   alpha: float = 1,
                   starting_shade: float = 0,
                   ending_shade: float = 100):
        """
        Red Orange Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("red-orange",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def black(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Black Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("black",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def white(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        White Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("white",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def ultramarine(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    alpha: float = 1,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Ultramarine Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("ultramarine",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def cerulean(self,
                 shade: float = None,
                 no_of_colors: int = 1,
                 gradient=True,
                 alpha: float = 1,
                 starting_shade: float = 0,
                 ending_shade: float = 100):
        """
        Cerulean Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("cerulean",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def aqua(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Aqua Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("aqua",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def lime(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Lime Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("lime",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def yellow(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               alpha: float = 1,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Yellow Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("yellow",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gold(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Gold Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("gold",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def orange(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               alpha: float = 1,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Orange Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("orange",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def peach(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Peach Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("peach",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def violet(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               alpha: float = 1,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Violet Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("violet",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def indigo(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               alpha: float = 1,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Indigo Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("indigo",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def pink(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             alpha: float = 1,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Pink Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("pink",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def purple_deep(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    alpha: float = 1,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Deep-Purple Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("deep-purple",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def blue_light(self,
                   shade: float = None,
                   no_of_colors: int = 1,
                   gradient=True,
                   alpha: float = 1,
                   starting_shade: float = 0,
                   ending_shade: float = 100):
        """
        Light-Blue Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("light-blue",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def green_light(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    alpha: float = 1,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Light Green Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("light-green",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def amber(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Amber Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("amber",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def orange_deep(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    alpha: float = 1,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Deep Orange Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("deep-orange",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def brown(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              alpha: float = 1,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Brown Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("brown",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)

    def gray_blue(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  alpha: float = 1,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Blue Gray Color from the palette

        :param shade: Shade of the color (0,100). Default is based on core
            color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param alpha: Transparency (between 0 to 1) Only works in Modes which
            have transparency channels like RGBA, AHEX, HSLA
        :param starting_shade: Minimum shade value (when creating multiple
            colors)
        :param ending_shade: Maximum shade value  (when creating multiple
            colors)
        :return: String, tuple or List of color(s) depending on options
        """
        return self.__return_colors(
            self.__common_color("blue-gray",
                                shade=shade,
                                no_of_colors=no_of_colors,
                                gradient=gradient,
                                alpha=alpha,
                                starting_shade=starting_shade,
                                ending_shade=ending_shade), alpha)


class ColorMap:
    """
    Simple class to create colormaps for matplotlib

    This allows you flexibility of :class:`~Palette` class to make colormaps
    which can be used in regular *matplotlib* workflow.

    >>> import matplotlib
    >>> import matplotlib.pylab as plt
    >>> import numpy as np
    >>> from SecretColors import Palette, ColorMap
    >>> p = Palette()
    >>> c = ColorMap(matplotlib, p)
    >>> data = np.random.rand(100, 100)
    >>> plt.pcolor(data, cmap=c.warm())
    >>> plt.show()

    You can also create qualitative colormap by setting up
    'is_qualitative=True' option

    >>> color_list = [p.red(), p.blue()]
    >>> plt.pcolor(data, cmap=c.from_list(color_list, is_qualitative=True))

    Reverse the colormap by adding 'is_reversed=True'

    >>> plt.pcolor(data, cmap=c.greens(is_reversed=True))

    Currently this class supports very less built in colormaps. However you
    can create your own by using very flexible function :func:`~from_list`.
    """

    def __init__(self, matplotlib, palette: Palette):
        """
        :param matplotlib: This is base module (import matplotlib)
        :param palette: SecretColor Palette
        """
        self.__mat = matplotlib
        self.palette = palette
        self.__default_no_of_colors = 10

    def __get_linear_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: LinearSegmentedColormap
        """
        try:
            return self.__mat.colors.LinearSegmentedColormap.from_list(
                "secret_color", color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def __get_listed_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: ListedColormap
        """
        try:
            return self.__mat.colors.ListedColormap(color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def __derive_map(self, color_list: list,
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
            return self.__get_listed_segment(color_list)
        else:
            return self.__get_linear_segment(color_list)

    def from_list(self, color_list: list, is_qualitative: bool = False,
                  is_reversed=False):
        """
        You can create your own colormap with list of own colors

        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :param is_reversed: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """
        return self.__derive_map(color_list, is_qualitative, is_reversed)

    def warm(self, starting_shade: float = 0, ending_shade: float = 100,
             no_of_colors: int = 10,
             is_qualitative: bool = False, is_reversed=False):
        """
        :param starting_shade: Minimum shade of Orange
        :param ending_shade: Maximum shade of Orange
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :param is_reversed: Reverses the order of color in Colormap
        :return: Matplotlib cmap wrapper
        """
        return self.__derive_map(self.palette.orange(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade), is_qualitative, is_reversed)

    def calm(self, starting_shade: float = 0, ending_shade: float = 100,
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

        return self.__derive_map(self.palette.cerulean(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative, is_reversed)

    def greens(self, starting_shade: float = 0, ending_shade: float = 100,
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

        return self.__derive_map(self.palette.green(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative, is_reversed)

    def hot(self, starting_shade: float = 0, ending_shade: float = 100,
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

        return self.__derive_map(self.palette.red(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative, is_reversed)
