#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# All objects related this project

from SecretColors.helpers.decorators import deprecated_aliases
from SecretColors._display import _swatch_html

from SecretColors._color import ColorValue, ColorLike
from SecretColors._validation import number
from typing import Union

from SecretColors.utils import (hex_to_rgb, rgb_to_hex, mix, text_color,
                                hsl_to_hex, hex_to_hsl, rgb_to_rgb255,
                                rgb_to_hsl)


class ColorOutput:
    """Immutable canonical color with builtin-compatible output wrappers.

    Use :meth:`with_alpha` to derive a new color instead of assigning channels.
    """

    def __init__(self, base: Union[str, tuple], *, alpha_first=False):
        if not hasattr(self, "_value"):
            if not isinstance(base, (str, tuple)):
                raise TypeError("Expected a hex string or RGB/RGBA tuple")
            object.__setattr__(self, "_value", ColorValue.parse(base, alpha_first=alpha_first))
            object.__setattr__(self, "_alpha_first", alpha_first)
            object.__setattr__(self, "_is_tuple", isinstance(base, tuple))

    def __setattr__(self, name, value):
        raise AttributeError("Colors are immutable; use with_alpha() or create a new color")

    def __delattr__(self, name):
        raise AttributeError("Colors are immutable; create a new color")

    @property
    def is_tuple(self):
        return isinstance(self, tuple) or getattr(self, "_is_tuple", False)

    @property
    def r(self):
        return self._value.rgba[0]

    @property
    def g(self):
        return self._value.rgba[1]

    @property
    def b(self):
        return self._value.rgba[2]

    @property
    def alpha(self):
        return self._value.rgba[3]

    @property
    def rgba(self) -> tuple[float, float, float, float]:
        return self._value.rgba

    @property
    def rgb(self) -> tuple[float, float, float]:
        return self._value.rgb

    @property
    def hsl(self) -> tuple:
        return rgb_to_hsl(*self.rgb)

    @property
    def hsla(self) -> tuple:
        return (*self.hsl, self.alpha)

    @property
    def rgb255(self) -> tuple:
        return rgb_to_rgb255(*self.rgb)

    @property
    def hex(self) -> str:
        return self._value.hex()

    @property
    def hexa(self) -> str:
        return self._value.hex(alpha=True)

    @property
    def ahex(self) -> str:
        return self._value.hex(alpha=True, alpha_first=True)

    def with_alpha(self, alpha: float) -> "ColorString | ColorTuple":
        value = self._value.with_alpha(alpha)
        if isinstance(self, tuple):
            return ColorTuple(value.rgba)
        return ColorString(value.hex(alpha=True, alpha_first=self._alpha_first),
                           alpha_first=self._alpha_first)

    def blend(self, other, ratio: float = 0.5, *, space: str = "rgb") -> "ColorString":
        """Blend RGB channels; alpha is interpolated separately.

        For source-over transparency compositing use ``utils.composite``.
        """
        if not isinstance(other, (ColorOutput, str, tuple)):
            raise TypeError("Expected a color object, hex string or RGB/RGBA tuple")
        target = ColorValue.parse(other)
        result = ColorString(mix(self.rgb, target.rgb, ratio, space=space))
        alpha = self.alpha + (target.rgba[3] - self.alpha) * ratio
        return result.with_alpha(alpha) if alpha < 1 else result

    def _repr_html_(self) -> str:
        return _swatch_html([self], [repr(self)])

    def __reduce__(self):
        return (_restore_color, (type(self), self.rgba, self._alpha_first,
                                len(self) if isinstance(self, (str, tuple)) else None))


def _restore_color(cls, rgba, alpha_first, length):
    if issubclass(cls, tuple):
        return cls(rgba[:length])
    if issubclass(cls, str):
        return cls(ColorValue.parse(rgba).hex(alpha=length == 9 or rgba[3] < 1,
                                             alpha_first=alpha_first),
                   alpha_first=alpha_first)
    return cls(rgba)


class ColorString(ColorOutput, str):
    def __new__(cls, base: Union[str, tuple], *, alpha_first=False):
        value = ColorValue.parse(base, alpha_first=alpha_first)
        raw = base.strip().removeprefix("#") if isinstance(base, str) else ""
        alpha = len(raw) in (4, 8) or (isinstance(base, tuple) and len(base) == 4)
        serialized = value.hex(alpha=alpha or value.rgba[3] < 1,
                               alpha_first=alpha_first)
        obj = str.__new__(cls, serialized)
        object.__setattr__(obj, "_value", ColorValue.parse(serialized, alpha_first=alpha_first))
        object.__setattr__(obj, "_alpha_first", alpha_first)
        return obj


class ColorTuple(ColorOutput, tuple):
    def __new__(cls, base: Union[str, tuple], *, alpha_first=False):
        value = ColorValue.parse(base, alpha_first=alpha_first)
        raw = base.strip().removeprefix("#") if isinstance(base, str) else ""
        alpha = len(raw) in (4, 8) or (isinstance(base, tuple) and len(base) == 4)
        obj = tuple.__new__(cls, value.rgba if alpha or value.rgba[3] < 1 else value.rgb)
        object.__setattr__(obj, "_value", value)
        object.__setattr__(obj, "_alpha_first", alpha_first)
        return obj




class ColorList(list[ColorLike]):
    """Regular list of colors with validated, alpha-aware notebook swatches."""

    def _repr_html_(self) -> str:
        return _swatch_html(self, [repr(c) for c in self])


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
        0-100% of value. Hue wraps around when you go above 360 or below 0,
        whereas saturation and lightness are clamped between 0-100%.

    Sometimes, rotation might be little confusing while dealing with
    lightness. Hence we have special methods which are
    user-friendly

    .. code-block:: python

        cw = ColorWheel("#fa4d56")  # Initialize your 'base color'
        cw.make_darker(30)  # Make current color darker by 30%
        print(cw.color)  # Prints #df0612, darker shade of #fa4d56
        cw.make_lighter(10)  # Make current color lighter by 10%
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
    def color(self) -> ColorString:
        """Returns current color (which has all the manipulations)
        """
        return ColorString(hsl_to_hex(self.hue, self.saturation,
                                      self.lightness))

    def __repr__(self):
        return (f"ColorWheel( _original_hex : {self._original_hex}, "
                f"color : {self.color} )")

    def _repr_html_(self) -> str:
        return _swatch_html([self.color], [repr(self)])

    def __iter__(self):
        yield self.color

    @staticmethod
    def _rotate(value: float, angle: float) -> float:
        angle = number(angle, "angle")
        return ((value * 360 + angle) % 360) / 360

    @staticmethod
    def _shift(value: float, angle: float) -> float:
        angle = number(angle, "angle")
        return min(1.0, max(0.0, value + angle / 360))

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
        self.saturation = self._shift(self.saturation, angle)

    def rotate_lightness(self, angle: float):
        """
        Rotates Lightness with given angle

        :param angle: Angle of ratation
        :type angle: float
        """
        self.lightness = self._shift(self.lightness, angle)

    def make_darker(self, percentage: float):
        """
        Makes color darker by reducing lightness

        :param percentage: Percentage change
        :type percentage: float
        """
        percentage = number(percentage, "percentage", minimum=0, maximum=100)
        av = self.lightness * percentage / 100
        self.lightness -= av

    def make_lighter(self, percentage: float):
        """
        Makes color lighter by increasing lightness

        :param percentage: Percentage change
        :type percentage: float
        """
        percentage = number(percentage, "percentage", minimum=0, maximum=100)
        av = (1 - self.lightness) * percentage / 100
        self.lightness += av

    def _make_color_list(self, *args, reverse: bool) -> list:
        color_list = ColorList([self.color])
        for angle in args:
            hue = self._rotate(self.hue, angle)
            color_list.append(ColorString(hsl_to_hex(hue, self.saturation,
                                                     self.lightness)))
        if reverse:
            color_list.reverse()
        return color_list

    @deprecated_aliases(is_reversed='reverse')
    def complementary(self, reverse: bool = False) -> list:
        """
        Generates two complementary colors. Out of which, one will be your
        current color

        :param reverse: If True, return list will be reversed
        :type reverse: bool
        :return: List of two complementary colors
        """
        return self._make_color_list(180, reverse=reverse)

    @deprecated_aliases(is_reserved='reverse', is_reversed='reverse')
    def triadic(self, reverse: bool = False) -> list:
        """
        Generate triadic colors. Out of which, one will be your current
        color

        :param reverse: If True, return list will be reversed
        :type reverse: bool
        :return: List of 3 triadic colors
        """
        return self._make_color_list(120, 240, reverse=reverse)

    @deprecated_aliases(is_reversed='reverse')
    def tetradic(self, reverse: bool = False) -> list:
        """
        Generates tetradic colors. Out of which, one will be your current
        color.

        :param reverse: If True, return list will be reversed
        :type reverse: bool
        :return: List of 4 tetradic colors
        """
        return self._make_color_list(90, 180, 270, reverse=reverse)

    @deprecated_aliases(is_reversed='reverse')
    def analogous(self, loc="first", reverse: bool = False) -> list:
        """
        Generate list of analogous colors. Out of which, one will be your
        current color. Location of where current color should be in these 3
        colors can be decided by `loc` argument.

        :param loc: Location of current color in the analogous colors.
            Available options: [first, middle, last]. (default: first)
        :type loc: str
        :param reverse: If True, return list will be reversed.
        :type reverse: bool
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

        colors = ColorList(ColorString(c) for c in colors)
        if reverse:
            colors.reverse()
        return colors

    def text_color(self) -> str:
        """Simply returns black or white color based on the color contrast
        of back/white with current color. This will be useful when you are
        writing text on any colored background.

        :return: White of Black color (based on contrast)
        """
        return text_color(self.color)
