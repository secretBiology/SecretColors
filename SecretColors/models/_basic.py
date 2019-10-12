#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# Basic Models

from SecretColors.utils import hex_to_hsl, hsl_to_hex, text_color


class ColorWheel:

    def __init__(self, hex_color: str):
        self._original_hex = hex_color
        self.hue, self.saturation, self.lightness = hex_to_hsl(hex_color)

    def reset(self):
        self.hue, self.saturation, self.lightness = hex_to_hsl(
            self._original_hex)

    @property
    def color(self) -> str:
        c = hsl_to_hex(self.hue, self.saturation, self.lightness)
        return c

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
