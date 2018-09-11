"""
Main Color Palette classes
"""
import random
import warnings

from SecretColors._color_data import *
from SecretColors.utils import *

COLOR_MODE_RGB = "rgb"
COLOR_MODE_HEX = "hex"
COLOR_MODE_HSV = "hsv"


def _warn(message: str, show_warning: bool = True) -> None:
    """
    Simple function to generate warning
    :param message: Message you want to send
    :param show_warning: If False, warnings will be suppressed
    """
    if show_warning:
        warnings.warn(message + " To suppress warning use " +
                      "'show_warning=False' in constructor of palette")


def _convert_color(color: str, color_mode: str, show_warning: bool):
    """
    General function to change color modes
    :param color: Hex color
    :param color_mode: Color Mode (rgb, hex, hsv)
    :param show_warning: If False, warnings will be suppressed
    :return: String (in case of hex) or tuple (in rgb and hsv) of color
    """
    if color_mode == COLOR_MODE_HEX:
        return color
    elif color_mode == COLOR_MODE_RGB:
        return hex_to_rgb(color)
    elif color_mode == COLOR_MODE_HSV:
        return hex_to_hsv(color)
    else:
        _warn("Invalid color_mode. Using default mode", show_warning)
        return color


class Grade:
    """
    Class to hold various grades of colors
    Currently supports following grade range

    for IBM Palette : [0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for Material Palette: [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    Any value below minimum will be considered as minimum while any value
    above maximum will be threshold to maximum. Any intermediate value will
    be converted nearest highest value
    e.g. value of 12 or 18 in IBM Palette will be considered as 20

    """

    def __init__(self, amount: int, color: str, color_mode: str,
                 special=False, show_warning: bool = True):
        """
        :param amount: Amount of grade
        :param color: Color value (hex)
        :param color_mode: Color Mode (rgb, hex, hsv)
        :param special: If it is special color (used in Material Palette)
        :param show_warning: If False, warnings will be suppressed
        """
        self.amount = amount
        self._color = color
        self.special = special
        self.color_mode = color_mode
        self.show_warning = show_warning

    @property
    def color(self):
        """
        :return: Color associated with this grade
        """
        return _convert_color(self._color, self.color_mode, self.show_warning)

    def __str__(self):
        return str(self.color)


class Color:
    """
    Color object which is child of Palette class.
    This holds information about color name and its grades
    """

    def __init__(self, name: str, show_warning: bool = True,
                 palette: str = PALETTE_IBM):
        """
        :param name: Name of color
        :param show_warning: If False, warnings will be suppressed
        :param palette: Name of Palette
        """
        self.name = name
        self.palette = palette
        self.core = -1
        self._grades = {}
        self._special = {}
        self._color_mode = COLOR_MODE_HEX
        self.show_warning = show_warning

    @property
    def grades(self) -> list:
        """
        :return: List of graded colors available in current palette
        """
        return [x for x in self._grades.values()]

    def add_grade(self, amount: int, color: str) -> None:
        """
        Add grade to current color

        :param amount: Grade amount
        :param color: Hex color
        """
        self._grades[amount] = Grade(amount, color, self._color_mode)

    def add_special(self, amount: int, color: str) -> None:
        """
        Add special form of grade to color.
        This is generally used in Material palette. These are the colors
        which starts with 'a' as a prefix to grades
        :param amount: Amount of grade
        :param color: Hex color
        """
        self._special[amount] = Grade(amount, color, self._color_mode,
                                      special=True)

    def get_grade(self, amount: int):
        """
        Returns grade of specified amount.
        If grade is not available, available grade is returned
        :param amount: Amount of grade
        :return: single object or list of objects
        """
        g_range = [x.amount for x in self._grades.values()]
        if amount <= min(g_range):
            return self._grades[min(g_range)]
        elif amount >= max(g_range):
            return self._grades[max(g_range)]
        else:
            for g in g_range:
                if amount <= g:
                    return self._grades[g]

    def color_mode(self, color_mode: str) -> None:
        """
        Sets color mode for current color
        :param color_mode: rgb, hex or hsv
        """
        for x in self._grades.values():
            x.color_mode = color_mode

    def __iter__(self):
        """
        You can iterate color object like 'for grade in color'.
        :return: iterator
        """
        for a in self._grades.values():
            yield a

    def __str__(self) -> str:
        """
        If used directly as a string, core color will be returned
        """
        return str(self._grades[self.core].color)

    def reversed(self) -> None:
        """
        Reverses the grade dictionary
        """
        keys = [x for x in self._grades.keys()]
        keys.reverse()
        self._grades = {k: self._grades[k] for k in keys}

    def get_gradient(self, no_of_colors: int, start_from: int = None):
        """
        Returns gradient of current color.
        This will first check if we can extract colors from existing
        grades. If yes, then colors are returned from available grades.
        If there are more number of requested colors in comparison to number
        of grades available for current color, then it will select minimum
        grade and maximum grade available and then calculates colors between
        them in RGB color space
        Similar calculation is done when start_from option is provided. If
        there is only single grade present, all colors returning will be same

        :param no_of_colors: Number of colors needed in gradient
        :param start_from: from which grade gradient should start
        :return: list of colors based on current color mode
        """
        g_range = [x for x in self._grades.keys()]
        required_colors = no_of_colors
        if start_from is not None:
            required_colors = len([x for x in g_range if x >= start_from])

        if required_colors > len(g_range) or required_colors == 0 or \
                required_colors < no_of_colors:
            if start_from is None or start_from >= max(g_range) or start_from \
                    <= min(g_range):
                c1 = self._grades[min(g_range)]
                c2 = self._grades[max(g_range)]
            else:
                c1 = self.get_grade(start_from)
                c2 = self._grades[max(g_range)]

            # If there are no distinct grades return same color
            if c1 == c2:
                return [c1.color] * no_of_colors

            return [_convert_color(x, self._color_mode, self.show_warning) for x
                    in color_in_between(c1.color, c2.color, no_of_colors + 1)]
        else:
            if start_from is not None and start_from <= max(g_range):
                g_range = [x for x in g_range if x >= start_from]

            g_range.sort()
            re_col = []
            for i in g_range:
                re_col.append(_convert_color(self._grades[i].color,
                                             self._color_mode,
                                             self.show_warning))
                if len(re_col) == no_of_colors:
                    return re_col


class Palette:
    """
    Represents color palette from existing values.
    Currently available palettes are :
    (1) IBM Color Palette (`ibm`) :Default
    (2) Google Material Design Color Palette (`material`)

    """

    def __init__(self, name=PALETTE_IBM, color_mode: str = COLOR_MODE_HEX,
                 show_warning: bool = True, remove_white: bool = True):
        """
        :param name: Name of the palette (ibm, material)
        :param color_mode: Color mode in which colors will output will be
        given . (rgb, hex, hsv)
        :param show_warning: If False, warnings will be suppressed
        :param remove_white: If True, white and its shades will be excluded
        in generating color palettes. :Default is True
        """

        self.name = name
        self.show_warning = show_warning
        self._colors = {}
        self._raw = ParentPalette()
        self._color_mode = color_mode
        self._other_colors = {}
        self.remove_white = remove_white

        self._all_palettes = [IBMPalette(), MaterialPalette()]

        if name not in [PALETTE_IBM, PALETTE_MATERIAL]:
            _warn("No such color palette exists. Using default palette",
                  self.show_warning)
            self.name = PALETTE_IBM

        for p in self._all_palettes:
            for data in p.colors:
                c = Color(data[p.name])
                c.core = data[p.core]
                c.palette = p.get_palette_name()
                for v in data[p.all]:
                    if v[p.special]:
                        c.add_special(v[p.grade], v[p.value])
                    else:
                        c.add_grade(v[p.grade], v[p.value])

                if data[p.name] != "white":
                    if self.name == p.get_palette_name():
                        self._colors[data[p.name]] = c
                    else:
                        self._other_colors[data[p.name]] = c
                elif not self.remove_white:
                    if self.name == p.get_palette_name():
                        self._colors[data[p.name]] = c
                    else:
                        self._other_colors[data[p.name]] = c

        self.change_color_mode(color_mode)

    def __iter__(self):
        """
        We can iterate over Color values like 'for color in palette'
        :return: iterator
        """
        for a in self._colors.values():
            yield a

    def change_color_mode(self, mode: str) -> None:
        """
        Changes color mode
        :param mode: rgb, hex, hsv (default: hex)
        """
        self._color_mode = mode
        for c in self._colors.values():
            c.color_mode(mode)

    @property
    def colors(self) -> list:
        """
        :return: List of all colors in current palette
        """
        return [x for x in self._colors.values()]

    def random(self, no_of_colors: int = 1, grade: int = None):
        """
        Generates random color from current palette.
        :param grade: If provided, grades are picked from this grade. If
        current grade is not available, nearby grade is picked up
        :param no_of_colors: Number of random colors you want to generate
        :return: single color or list of colors
        """
        all_grades = []
        if grade is None:
            for y in [x.grades for x in self.colors]:
                all_grades.extend(y)
        else:
            for y in self.colors:
                all_grades.append(y.get_grade(grade))
        random.shuffle(all_grades)
        if len(all_grades) > no_of_colors:
            if no_of_colors == 1:
                return all_grades[0].color
            else:
                return [x.color for x in all_grades[0:no_of_colors]]

        else:
            _warn("No of colors requested are more than current palette has. "
                  "Using custom gradient for providing requested colors",
                  self.show_warning)
            r = self.random(grade=grade)
            cols = color_in_between(r.color, get_complementary(r.color),
                                    no_of_colors)
            return [_convert_color(x, self._color_mode, self.show_warning) for x
                    in cols]

    def _get_color(self, name: str) -> Color:
        """
        Internal use function to get color based on its name.
        If color is not available in current palette, other palettes will be
        searched.

        :param name: name of color
        :return: Color object
        """
        for c in self.colors:
            if c.name == name:
                return c
        _warn("Current palette do not have this color. Using it from other "
              "palettes", self.show_warning)
        return self._other_colors[name]

    @staticmethod
    def _get_grade(color: Color, grade: int = None) -> Grade:
        """
        :param color: Color object
        :param grade: Amount of grade
        :return: Grade Object
        """
        return color.get_grade(grade)

    def _common_color(self, color_name: str, grade: int = None,
                      no_of_colors: int = 1, start_from: int = None):

        """
        :param color_name: Name of the color :param grade: Grade amount
        :param no_of_colors: Number of colors needed :param start_from:
        starting grade (used in case of more than 1 colors are requested)
        :return: single color or list of colors
        """
        if grade is None and no_of_colors == 1:
            c = self._get_color(color_name)
            if self._color_mode == COLOR_MODE_HEX:
                return _convert_color(str(c), self._color_mode,
                                      self.show_warning)
            else:
                return c._grades[c.core].color
        else:
            if no_of_colors == 1:
                g = self._get_grade(self._get_color(color_name), grade)
                return g.color
            else:
                return self._get_color(color_name).get_gradient(no_of_colors,
                                                                start_from)

    @staticmethod
    def gradient_between(hex_color1: str, hex_color2: str,
                         no_of_colors: int, excluding_input: bool = False):

        """
        Returns colors between input colors
        :param hex_color1: Color 1 in hex form
        :param hex_color2: Color 2 in hex form
        :param no_of_colors: Number of colors required
        :param excluding_input: If yes, input colors are excluded from the list
        :return: list of color or single color
        """
        if no_of_colors == 0:
            return []
        elif no_of_colors == 1:
            return color_in_between(hex_color1, hex_color2)
        elif no_of_colors == 2 and not excluding_input:
            return [hex_color1, hex_color2]
        elif no_of_colors == 2 and excluding_input:
            return color_in_between(hex_color1, hex_color2, no_of_colors + 1)
        else:
            col = []
            adjust = -1
            if excluding_input:
                adjust = 1
            else:
                col = [hex_color1]
            col.extend(
                color_in_between(hex_color1, hex_color2, no_of_colors + adjust))
            if not excluding_input:
                col.append(hex_color2)
            return col

    def red(self, grade: int = None, no_of_colors: int = 1,
            start_from: int = None):
        return self._common_color("red", grade, no_of_colors, start_from)

    def ultramarine(self, grade: int = None, no_of_colors: int = 1,
                    start_from: int = None):
        return self._common_color("ultramarine", grade, no_of_colors,
                                  start_from)

    def blue(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("blue", grade, no_of_colors, start_from)

    def cerulean(self, grade: int = None, no_of_colors: int = 1,
                 start_from: int = None):
        return self._common_color("cerulean", grade, no_of_colors, start_from)

    def aqua(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("aqua", grade, no_of_colors, start_from)

    def teal(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("teal", grade, no_of_colors, start_from)

    def green(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        return self._common_color("green", grade, no_of_colors, start_from)

    def lime(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("lime", grade, no_of_colors, start_from)

    def yellow(self, grade: int = None, no_of_colors: int = 1,
               start_from: int = None):
        return self._common_color("yellow", grade, no_of_colors, start_from)

    def gold(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("gold", grade, no_of_colors, start_from)

    def orange(self, grade: int = None, no_of_colors: int = 1,
               start_from: int = None):
        return self._common_color("orange", grade, no_of_colors, start_from)

    def peach(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        return self._common_color("peach", grade, no_of_colors, start_from)

    def magenta(self, grade: int = None, no_of_colors: int = 1,
                start_from: int = None):
        return self._common_color("magenta", grade, no_of_colors, start_from)

    def purple(self, grade: int = None, no_of_colors: int = 1,
               start_from: int = None):
        return self._common_color("purple", grade, no_of_colors, start_from)

    def violet(self, grade: int = None, no_of_colors: int = 1,
               start_from: int = None):
        return self._common_color("violet", grade, no_of_colors, start_from)

    def indigo(self, grade: int = None, no_of_colors: int = 1,
               start_from: int = None):
        return self._common_color("indigo", grade, no_of_colors, start_from)

    def gray(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("gray", grade, no_of_colors, start_from)

    def cool_gray(self, grade: int = None, no_of_colors: int = 1,
                  start_from: int = None):
        return self._common_color("cool-gray", grade, no_of_colors, start_from)

    def warm_gray(self, grade: int = None, no_of_colors: int = 1,
                  start_from: int = None):
        return self._common_color("warm-gray", grade, no_of_colors, start_from)

    def neutral_white(self, grade: int = None, no_of_colors: int = 1,
                      start_from: int = None):
        return self._common_color("neutral-white", grade, no_of_colors,
                                  start_from)

    def cool_white(self, grade: int = None, no_of_colors: int = 1,
                   start_from: int = None):
        return self._common_color("cool-white", grade, no_of_colors, start_from)

    def warm_white(self, grade: int = None, no_of_colors: int = 1,
                   start_from: int = None):
        return self._common_color("warm-white", grade, no_of_colors, start_from)

    def black(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        return self._common_color("black", grade, no_of_colors, start_from)

    def white(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        if self.remove_white:
            _warn(
                "To include white and it's shades, use 'remove_white=False' "
                "option")
            return _convert_color("#fff", self._color_mode, self.show_warning)
        else:
            return self._common_color("white", grade, no_of_colors, start_from)

    def pink(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("pink", grade, no_of_colors, start_from)

    def deep_purple(self, grade: int = None, no_of_colors: int = 1,
                    start_from: int = None):
        return self._common_color("deep-purple", grade, no_of_colors,
                                  start_from)

    def light_blue(self, grade: int = None, no_of_colors: int = 1,
                   start_from: int = None):
        return self._common_color("light-blue", grade, no_of_colors, start_from)

    def cyan(self, grade: int = None, no_of_colors: int = 1,
             start_from: int = None):
        return self._common_color("cyan", grade, no_of_colors, start_from)

    def light_green(self, grade: int = None, no_of_colors: int = 1,
                    start_from: int = None):
        return self._common_color("light-green", grade, no_of_colors,
                                  start_from)

    def amber(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        return self._common_color("amber", grade, no_of_colors, start_from)

    def deep_orange(self, grade: int = None, no_of_colors: int = 1,
                    start_from: int = None):
        return self._common_color("deep-orange", grade, no_of_colors,
                                  start_from)

    def brown(self, grade: int = None, no_of_colors: int = 1,
              start_from: int = None):
        return self._common_color("brown", grade, no_of_colors, start_from)

    def blue_gray(self, grade: int = None, no_of_colors: int = 1,
                  start_from: int = None):
        return self._common_color("blue-gray", grade, no_of_colors, start_from)

    def _color_from_hex(self, hex_color: str) -> list:
        """
        Iterate over all color grades available in package. If match is found
        color object is returned
        :param hex_color: Hex color to scan
        :return: list of gradient colors from palette or derived
        """
        for c in self.colors:
            for g in c.grades:
                if g.color == hex_color:
                    return c.get_gradient(no_of_colors=10)

        for c in self._other_colors.values():
            for g in c.grades:
                if g.color == hex_color:
                    return c.get_gradient(no_of_colors=10)

        # If couldn't find any hex color, make automatic between white, color of
        # interest and black
        return ["#f0f4f4", hex_color, "#000000"]

    def cmap_of(self, matplotlib, color):
        """
        Creates custom cmap from given hex_color.

        :param matplotlib: from "import matplotlib"
        :param color: hex color
        :return: LinearSegmentedColormap segment
        """
        try:
            return matplotlib.colors.LinearSegmentedColormap \
                .from_list(color + "_secret_color", self._color_from_hex(color))
        except AttributeError:
            raise Exception("Add 'matplotlib' as a first argument. For "
                            "example, import matplotlib; palette.cmap_of("
                            "matplotlib, "
                            "palette.red());")
