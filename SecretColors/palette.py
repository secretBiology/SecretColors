"""
SecretColors 2019
Author: Rohit Suratekar

All basic functions and main classes
"""

import random
import warnings

from SecretColors.__colors import *
from SecretColors.utils import *


def _warn(message: str, show_warning: bool = True) -> None:
    """
    Simple function to generate warning
    :param message: Message you want to send
    :param show_warning: If False, warnings will be suppressed
    """
    if show_warning:
        m = message + "\nTo suppress warning use 'show_warning=False' in " \
                      "constructor of the palette"
        ##
        warnings.warn(m)


class Palette:
    """
    Base Palette Class
    """

    def __init__(self, name: str = PALETTE_IBM, allow_gray_shades: bool = True,
                 show_warning: bool = True, color_mode: str = MODE_HEX):
        """
        Generates Palette Object
        :param name: Name of the palette
        :param allow_gray_shades: If True, shades of gray, white and black
        are included in the gradient formation or random color generation
        :param show_warning: If True, warnings will be shown
        :param color_mode: Color Mode in which output will be provided
        """

        self.__palette = self.__get_palette(name)
        self.__colors = {}
        for c in self.__palette.get_all_colors():
            self.__colors[c.name] = c

        self.__allow_gray = allow_gray_shades
        self._show_warning = show_warning
        self.color_mode = color_mode

    @staticmethod
    def __get_palette(name: str) -> ParentPalette:
        """
        :param name: Name of the color palette
        :return: respective palette class
        """
        if name == PALETTE_IBM:
            return IBMPalette()
        elif name == PALETTE_MATERIAL:
            return MaterialPalette()
        elif name == PALETTE_BREWER:
            return ColorBrewer()
        elif name == PALETTE_CLARITY:
            return ClarityPalette()
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
            for c in self.__get_palette(p).get_all_colors():
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
        :return: Version of the current palette in THIS library
        """
        return self.__palette.get_version()

    @property
    def creator_url(self):
        """
        :return: URL citing original creator
        """
        return self.__palette.get_creator_url()

    @property
    def standard_colors(self):
        """
        :return: Standard colors from the palette
        """
        d = {}
        for x in self.__colors.values():
            if self.__allow_gray:
                d[x.name] = x.hex
            else:
                if x.type != TYPE_GRAY:
                    d[x.name] = x.hex
        return d

    def __convert(self, hex_name: str):
        """
        Converts Hex into palette's current color-mode

        :param hex_name: Name of color in Hex format
        :return: color in palette's color mode
        """
        if self.color_mode == MODE_HEX:
            return hex_name
        elif self.color_mode == MODE_RGB:
            return hex_to_rgb(hex_name)
        elif self.color_mode == MODE_HSL:
            return hex_to_hsl(hex_name)
        else:
            raise Exception("Invalid Color Mode or this color mode is not "
                            "supported yet")

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
            _warn("Current palette do not have this color. Using it from other "
                  "palettes. ", self._show_warning)
            return self.__all_colors()[name.lower().strip()]

    @staticmethod
    def __random_pick(color: Color,
                      shade: float = None,
                      no_of_colors: int = 1,
                      gradient=False,
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
                 force_gray: bool = False):

        box = [x for x in self.__colors.values() if x.type != TYPE_GRAY]

        if force_gray:
            box = [x for x in self.__colors.values()]

        if no_of_colors == 1:
            return self.__random_pick(random.sample(box, 1)[0],
                                      shade=shade,
                                      starting_shade=starting_shade,
                                      ending_shade=end_shade)
        elif no_of_colors < len(box):
            return_box = []
            for c in random.sample(box, no_of_colors):
                return_box.append(
                    self.__random_pick(c, shade=shade,
                                       starting_shade=starting_shade,
                                       ending_shade=end_shade))

            return return_box

        else:
            extra_box = []
            for i in range(no_of_colors):
                c = random.sample(box, 1)[0]
                extra_box.append(
                    self.__random_pick(c, shade=shade,
                                       starting_shade=starting_shade,
                                       ending_shade=end_shade))

            return extra_box

    def random(self, no_of_colors: int = 1,
               shade: float = None,
               starting_shade: float = 0,
               ending_shade: float = 100,
               force_gray: bool = False):
        """
        Generates random color. First it will try to pick color existed in
        the given palette. However, with other options, you can refine the
        desired output. By default, shades of gray, white and black colors
        are excluded from random function

        :param no_of_colors: Number of Colors
        :param shade: Shade of Color
        :param starting_shade: Starting Shade
        :param ending_shade: End Shade
        :param force_gray: If True, it will add grays, whites and blacks
        while picking random colors
        :return: Color/List of colors
        """
        return self.__return_colors(
            self.__random(no_of_colors=no_of_colors,
                          shade=shade,
                          starting_shade=starting_shade,
                          end_shade=ending_shade,
                          force_gray=force_gray))

    def random_balanced(self, no_of_colors: int = 1):
        """
        Essentially `random()` function with shade=50. Shade 50 colors are
        generally neutral and visually appealing. Hence use this function for
        regular analysis instead `random()`

        :param no_of_colors: Number of colors
        :return: Color/List of colors
        """
        return self.random(shade=50, no_of_colors=no_of_colors)

    def __common_color(self, name: str,
                       shade: float = None,
                       no_of_colors: int = 1,
                       gradient=False,
                       starting_shade: float = 0,
                       ending_shade: float = 100):
        c = self.__get_color(name)

        if no_of_colors > 1 and shade is not None:
            _warn("Shade will be ignored when number of colors are more than 1")

        if shade is None:
            shade = c.core_shade_value

        return self.__random_pick(c,
                                  no_of_colors=no_of_colors,
                                  shade=shade,
                                  gradient=gradient,
                                  starting_shade=starting_shade,
                                  ending_shade=ending_shade
                                  )

    def random_gradient(self, no_of_colors: int = 1, shade: float = None,
                        complementary=True):
        """
        Generates random gradient between two colors. By default it uses two
        random complementary colors. However you can change it to make
        complete random by setting `complementary` to False

        :param no_of_colors: Number of colors in your gradient
        :param shade: Keep shade value between 0 to 100 if you want random
        colors from specific shade
        :param complementary: If True, two colors picked will be
        complementary to each other
        :return: List of colors
        """
        if complementary:
            r1 = self.__random(shade=shade)
            r2 = get_complementary(r1)
        else:
            r1, r2 = self.__random(shade=shade, no_of_colors=2)
        return self.color_between(r1, r2, no_of_colors,
                                  include_both=True)

    def color_between(self, color1_hex: str,
                      color2_hex: str,
                      no_of_colors: int,
                      include_first: bool = False,
                      include_last: bool = False,
                      include_both: bool = False):

        """
        Generates list of colors between given colors. You can use this to
        make gradients as well

        :param color1_hex: Starting color
        :param color2_hex: End Color
        :param no_of_colors: Total number of colors
        :param include_first: Keep True, if you want to include starting
        color in final list
        :param include_last: Keep True, if you want to include end color in
        final list
        :param include_both: Keep True, if you want to include both starting
        and end colors in your final list. If kept True, it will override
        `include_first` and `include_last` values
        :return: List of colors
        """

        if include_both and no_of_colors < 2:
            raise Exception("If you want to include both colors, number of "
                            "colors should be at least 2")

        if no_of_colors == 1:
            if include_first:
                return self.__return_colors([color1_hex])
            elif include_last:
                return self.__return_colors([color2_hex])

        if no_of_colors == 2 and (include_both or (include_first and
                                                   include_last)):
            return self.__return_colors([color1_hex, color2_hex])

        adjust_factor = 1
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
        return self.__return_colors(c)

    def __return_colors(self, obj):
        """
        :param obj: Single string or list of strings
        :return: Colors according to color mode
        """
        if type(obj) is str:
            return self.__convert(obj)
        elif type(obj) is list:
            return [self.__convert(x) for x in obj]
        else:
            _warn("Unable to convert current object")
            return obj

    @staticmethod
    def cmap_from(matplotlib, hex_color_list: list):
        """
        Creates custom cmap from given hex_color list.
        Use SecretColors.palette.ColorMap for more refined control

        :param matplotlib: from "import matplotlib"
        :param hex_color_list: List of colors in Hex format
        :return: LinearSegmentedColormap segment
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
            starting_shade: float = 0,
            ending_shade: float = 100):
        """
        Red Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def blue(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
            Blue Color from the palette
           :param shade: Shade of the color (0,100). Default is based on core
           color of the palette
           :param no_of_colors: Total number of colors (color shades)
           :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def green(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Green Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def magenta(self,
                shade: float = None,
                no_of_colors: int = 1,
                gradient=True,
                starting_shade: float = 0,
                ending_shade: float = 100):
        """
        Magenta Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def purple(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Purple Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def cyan(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Cyan Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def teal(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Teal Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gray_cool(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Cool Gray Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gray_neutral(self,
                     shade: float = None,
                     no_of_colors: int = 1,
                     gradient=True,
                     starting_shade: float = 0,
                     ending_shade: float = 100):
        """
        Neutral Gray Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gray(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Gray Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gray_warm(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Warm Gray Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def red_orange(self,
                   shade: float = None,
                   no_of_colors: int = 1,
                   gradient=True,
                   starting_shade: float = 0,
                   ending_shade: float = 100):
        """
        Red Orange Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def black(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Black Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def white(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        White Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def ultramarine(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Ultramarine Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def cerulean(self,
                 shade: float = None,
                 no_of_colors: int = 1,
                 gradient=True,
                 starting_shade: float = 0,
                 ending_shade: float = 100):
        """
        Cerulean Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def aqua(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Aqua Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def lime(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Lime Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def yellow(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Yellow Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gold(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Gold Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def orange(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Orange Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def peach(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Peach Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def violet(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Violet Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def indigo(self,
               shade: float = None,
               no_of_colors: int = 1,
               gradient=True,
               starting_shade: float = 0,
               ending_shade: float = 100):
        """
        Indigo Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def pink(self,
             shade: float = None,
             no_of_colors: int = 1,
             gradient=True,
             starting_shade: float = 0,
             ending_shade: float = 100):
        """
        Pink Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def purple_deep(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Deep-Purple Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def blue_light(self,
                   shade: float = None,
                   no_of_colors: int = 1,
                   gradient=True,
                   starting_shade: float = 0,
                   ending_shade: float = 100):
        """
        Light-Blue Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def green_light(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Light Green Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def amber(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Amber Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def orange_deep(self,
                    shade: float = None,
                    no_of_colors: int = 1,
                    gradient=True,
                    starting_shade: float = 0,
                    ending_shade: float = 100):
        """
        Deep Orange Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def brown(self,
              shade: float = None,
              no_of_colors: int = 1,
              gradient=True,
              starting_shade: float = 0,
              ending_shade: float = 100):
        """
        Brown Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))

    def gray_blue(self,
                  shade: float = None,
                  no_of_colors: int = 1,
                  gradient=True,
                  starting_shade: float = 0,
                  ending_shade: float = 100):
        """
        Blue Gray Color from the palette
        :param shade: Shade of the color (0,100). Default is based on core
        color of the palette
        :param no_of_colors: Total number of colors (color shades)
        :param gradient: If set True, color will be output in gradient manner
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
                                starting_shade=starting_shade,
                                ending_shade=ending_shade))


class ColorMap:
    """
    Simple class to create colormaps for matplotlib
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

    def __derive_map(self, color_list: list, is_qualitative=False):
        """
        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :return: Colormap which can be directly used with matplotlib
        """
        if is_qualitative:
            return self.__get_listed_segment(color_list)
        else:
            return self.__get_linear_segment(color_list)

    def from_list(self, color_list: list, is_qualitative: bool = False):
        """
        You can create your own colormap with list of own colors

        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :return: Colormap which can be directly used with matplotlib
        """
        return self.__derive_map(color_list, is_qualitative)

    def warm(self, starting_shade: float = 0, ending_shade: float = 100,
             no_of_colors: int = 10,
             is_qualitative: bool = False):
        """
        :param starting_shade: Minimum shade of Orange
        :param ending_shade: Maximum shade of Orange
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :return: Matplotlib cmap wrapper
        """
        return self.__derive_map(self.palette.orange(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative)

    def calm(self, starting_shade: float = 0, ending_shade: float = 100,
             no_of_colors: int = 10,
             is_qualitative: bool = False):
        """
        :param starting_shade: Minimum shade
        :param ending_shade: Maximum shade
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :return: Matplotlib cmap wrapper
        """

        return self.__derive_map(self.palette.cerulean(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative)

    def greens(self, starting_shade: float = 0, ending_shade: float = 100,
               no_of_colors: int = 10,
               is_qualitative: bool = False):
        """
        :param starting_shade: Minimum shade
        :param ending_shade: Maximum shade
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :return: Matplotlib cmap wrapper
        """

        return self.__derive_map(self.palette.green(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative)

    def hot(self, starting_shade: float = 0, ending_shade: float = 100,
            no_of_colors: int = 10,
            is_qualitative: bool = False):
        """
        :param starting_shade: Minimum shade
        :param ending_shade: Maximum shade
        :param no_of_colors: Number of colors to make colormap
        :param is_qualitative: True if colormap is qualitative
        :return: Matplotlib cmap wrapper
        """

        return self.__derive_map(self.palette.red(
            no_of_colors=no_of_colors,
            starting_shade=starting_shade,
            ending_shade=ending_shade
        ), is_qualitative)
