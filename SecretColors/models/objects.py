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
                                hsl_to_hex, hex_to_hsl)


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
        self.r, self.g, self.b, self.a = _validate(self._tuple, base)

    @property
    def rgba(self) -> tuple:
        return self.r, self.g, self.b, self.a

    @property
    def rgb(self) -> tuple:
        return self.r, self.g, self.b

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

    def __init__(self, hex_color: str):
        self._original_hex = hex_color
        self.hue, self.saturation, self.lightness = hex_to_hsl(hex_color)

    def reset(self):
        self.hue, self.saturation, self.lightness = hex_to_hsl(
            self._original_hex)

    @property
    def color(self) -> str:
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
        self.hue = self._rotate(self.hue, angle)

    def rotate_saturation(self, angle: float):
        self.saturation = self._rotate(self.saturation, angle)

    def rotate_lightness(self, angle: float):
        self.lightness = self._rotate(self.lightness, angle)

    def make_darker(self, percentage: float):
        av = self.lightness * percentage / 100
        self.lightness -= av

    def make_lighter(self, percentage: float):
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
        # Make in HSV space
        return self._make_color_list(180, is_revered=is_reversed)

    def triadic(self, is_reserved: bool = False) -> list:
        return self._make_color_list(120, 240, is_revered=is_reserved)

    def tetradic(self, is_reversed: bool = False) -> list:
        return self._make_color_list(90, 180, 270, is_revered=is_reversed)

    def analogous(self, loc="first", is_reversed: bool = False) -> list:
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
        return text_color(self.color)
