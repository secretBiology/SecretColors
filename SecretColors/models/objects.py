#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# All objects related this project

from typing import Union

from SecretColors.utils import (hex_to_rgb, rgb_to_hex,
                                color_in_between, text_color,
                                hsl_to_hex, hex_to_hsl, rgb_to_rgb255,
                                rgb_to_hsl)


def _validate(color: tuple, base):
    if len(color) not in [3, 4]:
        raise ValueError(f"{base} is not a valid Hex or RGB/RGBA tuple")

    if max(color) > 1 or min(color) < 0:
        raise ValueError(f"RGB/RGBA tuple should have values between 0-1. If "
                         f"you have 255 based color, please convert it to 0-1 "
                         f"and then provide it as an input")

    if len(color) == 3:
        return color[0], color[1], color[2], 1

    return color


class ColorOutput:
    def __init__(self, base: Union[str, tuple]):
        self._base = base
        if isinstance(base, str):
            self.is_tuple = False
            self._tuple = hex_to_rgb(base.strip())
        elif isinstance(base, tuple):
            self.is_tuple = True
            self._tuple = base
        else:
            raise TypeError(f"Currently color object can only be "
                            f"string or tuple. Your provided type "
                            f"is {type(base)}")

        # Validate and get rgba
        self.r, self.g, self.b, self._a = _validate(self._tuple, base)

    @property
    def alpha(self):
        return self._a

    @alpha.setter
    def alpha(self, value):
        self._a = value

    @property
    def rgba(self) -> tuple:
        return self.r, self.g, self.b, self.alpha

    @property
    def rgb(self) -> tuple:
        return self.r, self.g, self.b

    @property
    def hsl(self) -> tuple:
        return rgb_to_hsl(self.r, self.g, self.b)

    @property
    def hsla(self) -> tuple:
        h, s, l = rgb_to_hsl(self.r, self.g, self.b)
        return h, s, l, self.alpha

    @property
    def rgb255(self) -> tuple:
        return rgb_to_rgb255(self.r, self.g, self.b)

    @property
    def hex(self) -> str:
        if self.is_tuple:
            return rgb_to_hex(self.r, self.g, self.b)

        if self._base.startswith("#"):
            if len(self._base) in [4, 7]:
                return self._base
            else:
                return self._base[:7]
        else:
            if len(self._base) in [3, 6]:
                return self._base
            else:
                return self._base[:6]

    @staticmethod
    def _new_hex(c1: str, other) -> str:
        if isinstance(other, ColorOutput):
            return color_in_between(c1, other.hex)[0]
        elif isinstance(other, str):
            return color_in_between(c1, other)[0]
        elif isinstance(other, tuple):
            return color_in_between(c1, rgb_to_hex(*other))[0]
        else:
            raise TypeError(f"Expected ColorObject, str or tuple but got "
                            f"{type(other)}")

    def __add__(self, other):
        return ColorString(self._new_hex(self.hex, other))

    def __radd__(self, other):
        return self.__add__(other)


class ColorString(ColorOutput, str):
    def __init__(self, base: Union[str, tuple]):
        super().__init__(base)


class ColorTuple(ColorOutput, tuple):
    def __init__(self, base: Union[str, tuple]):
        super().__init__(base)


class ColorWheel:
    """
    ColorWheel class is more 'scientific' than using
    :class:`SecretColors.Palette`. This provides very useful
    and easy color manipulation tools. This class essentially mimics the
    typical color wheel. You can 'rotate' the wheel in different directions
    and axis to get appropriate colors. Following code shows the simplest use

    .. code-block:: python

        cw = ColorWheel("#fa4d56")  # Initialize your 'base color'
        print(cw.color)  # Prints #fa4d56
        cw.rotate_hue(180)  # Rotates Hue by 180 degree
        print(cw.color) # Prints #4dfaf1 (which is on the opposite side of  color wheel_)
        cw.rotate_hue(-180)  # Rotate Hue by -180 degree
        print(cw.color) # Back to #fa4d56
        cw.rotate_lightness(10) # Rotates Lightness by 10
        print(cw.color) # Prints #fa5b63
        cw.rotate_saturation(-50) # Rotate saturation by -50
        print(cw.color)  # Prints #ef676e

    .. tip::
        When your provide negative rotation values, essentially you are
        rotating wheel anti-clockwise. Essentially, 0-360 degree represents
        0-100% of value. When you go above 360 or below 0, it will
        automatically wrap it around.

    Sometimes, rotation might be little confusing while dealing with
    lightness. Hence we have special methods which are
    user-friendly

    .. code-block:: python

        cw = ColorWheel("#fa4d56")  # Initialize your 'base color'
        cw.make_darker(30)  # Make current color darker by 30%
        print(cw.color)  # Prints #df0612, darker shade of #fa4d56
        cw.make_lighter(10)  # Make current color lighter by 30%
        print(cw.color)  # Prints #f80915, lighter shade of #df0612

    You can perform infinite amount of manipulations. Only thing you should
    remember that, ColorWheel will return the 'current' color. So each time
    you perform manipulation, color will change. However, at anytime if you
    want to reset color to the original color (which you used to initialize
    the ColorWheel) you can simply use :func:`~SecretColors.ColorWheel.reset`.

    There are many useful methods which you can use to find colors with
    specific color harmony (like monochromatic, complementary, etc).

    """

    def __init__(self, hex_color: str):
        """
        Initialize ColorWheel with Hex color. This will be your base color
        on which all further manipulations can be done.

        :param hex_color: hex color
        """
        self._original_hex = hex_color
        self.hue, self.saturation, self.lightness = hex_to_hsl(hex_color)

    def reset(self):
        """Resets all adjustments/manipulation to your original color
            (which you used while creating this class in
            :func:`SecretColors.ColorWheel.__init__` )
        """
        self.hue, self.saturation, self.lightness = hex_to_hsl(
            self._original_hex)

    @property
    def color(self) -> str:
        """Returns current color (which has all the manipulations)
        """
        return hsl_to_hex(self.hue, self.saturation, self.lightness)

    def __repr__(self):
        return (f"ColorWheel( _original_hex : {self._original_hex}, "
                f"color : {self.color} )")

    def __iter__(self):
        yield self.color

    @staticmethod
    def _rotate(value: float, angle: float) -> float:
        value = value * 360
        value += angle
        value = abs(value % 360)
        return value / 360

    def rotate_hue(self, angle: float):
        """
        Rotates Hue with given angle

        :param angle: Angle of rotation
        :type angle: float
        """
        self.hue = self._rotate(self.hue, angle)

    def rotate_saturation(self, angle: float):
        """
        Rotates Saturation with given angle

        :param angle: Angle of rotation
        :type angle: float
        """
        self.saturation = self._rotate(self.saturation, angle)

    def rotate_lightness(self, angle: float):
        """
        Rotates Lightness with given angle

        :param angle: Angle of ratation
        :type angle: float
        """
        self.lightness = self._rotate(self.lightness, angle)

    def make_darker(self, percentage: float):
        """
        Makes color darker by reducing lightness

        :param percentage: Percentage change
        :type percentage: float
        """
        av = self.lightness * percentage / 100
        self.lightness -= av

    def make_lighter(self, percentage: float):
        """
        Makes color lighter by increasing lightness

        :param percentage: Percentage change
        :type percentage: float
        """
        av = (1 - self.lightness) * percentage / 100
        self.lightness += av

    def _make_color_list(self, *args, is_revered: bool) -> list:
        color_list = [self.color]
        for angle in args:
            hue = self._rotate(self.hue, angle)
            color_list.append(hsl_to_hex(hue, self.saturation, self.lightness))
        if is_revered:
            return list(reversed(color_list))
        else:
            return color_list

    def complementary(self, is_reversed: bool = False) -> list:
        """
        Generates two complementary colors. Out of which, one will be your
        current color

        :param is_reversed: If True, return list will be reversed
        :type is_reversed: bool
        :return: List of two complementary colors
        """
        return self._make_color_list(180, is_revered=is_reversed)

    def triadic(self, is_reserved: bool = False) -> list:
        """
        Generate triadic colors. Out of which, one will be your current
        color

        :param is_reserved: If True, return list will be reversed
        :type is_reserved: bool
        :return: List of 3 triadic colors
        """
        return self._make_color_list(120, 240, is_revered=is_reserved)

    def tetradic(self, is_reversed: bool = False) -> list:
        """
        Generates tetradic colors. Out of which, one will be your current
        color.

        :param is_reversed: If True, return list will be reversed
        :type is_reversed: bool
        :return: List of 4 tetradic colors
        """
        return self._make_color_list(90, 180, 270, is_revered=is_reversed)

    def analogous(self, loc="first", is_reversed: bool = False) -> list:
        """
        Generate list of analogous colors. Out of which, one will be your
        current color. Location of where current color should be in these 3
        colors can be decided by :paramref:`loc` argument.

        :param loc: Location of current color in the analogous colors.
            Available options: [first, middle, last]. (default: first)
        :type loc: str
        :param is_reversed: If True, return list will be reversed.
        :type is_reversed: bool
        :return: List of 3 analogous colors
        """
        factor = 1
        if loc.strip().lower() in ["last", "l"]:
            factor = -1
        a1 = self._rotate(self.hue, 30 * factor)
        a2 = self._rotate(self.hue, 60 * factor)
        if loc.strip().lower() in ["middle", "m"]:
            a2 = self._rotate(self.hue, -30)
            colors = [
                hsl_to_hex(a1, self.saturation, self.lightness),
                self.color,
                hsl_to_hex(a2, self.saturation, self.lightness)
            ]
        else:
            colors = [
                self.color,
                hsl_to_hex(a1, self.saturation, self.lightness),
                hsl_to_hex(a2, self.saturation, self.lightness)
            ]

        if is_reversed:
            return list(reversed(colors))
        else:
            return colors

    def text_color(self) -> str:
        """Simply returns black or white color based on the color contrast
        of back/white with current color. This will be useful when you are
        writing text on any colored background.

        :return: White of Black color (based on contrast)
        """
        return text_color(self.color)
