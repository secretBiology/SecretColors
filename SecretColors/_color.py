"""Canonical color parsing and serialization, independent of display objects."""

from dataclasses import dataclass
from typing import Literal, TypeAlias

from SecretColors._validation import number

RGB: TypeAlias = tuple[float, float, float]
RGBA: TypeAlias = tuple[float, float, float, float]
ColorLike: TypeAlias = str | RGB | RGBA
ColorMode: TypeAlias = Literal["hex", "hexa", "ahex", "rgb", "rgba"]
InterpolationSpace: TypeAlias = Literal["rgb", "lab", "lch"]


@dataclass(frozen=True)
class ColorValue:
    rgba: RGBA

    @classmethod
    def parse(cls, color, *, alpha_first=False):
        if isinstance(color, cls):
            return color
        # Our builtin-compatible wrappers retain the encoding information.
        value = getattr(color, "_value", None)
        if isinstance(value, cls):
            return value
        if isinstance(color, str):
            raw = color.strip().removeprefix("#")
            if len(raw) in (3, 4):
                raw = "".join(c * 2 for c in raw)
            if len(raw) not in (6, 8) or any(c not in "0123456789abcdefABCDEF" for c in raw):
                raise ValueError(f"Invalid hex color: {color!r}")
            if alpha_first and len(raw) == 8:
                raw = raw[2:] + raw[:2]
            channels = tuple(int(raw[i:i + 2], 16) / 255 for i in range(0, len(raw), 2))
        elif isinstance(color, (tuple, list)):
            channels = tuple(color)
        else:
            raise TypeError("Expected a hex string or RGB/RGBA tuple")
        if len(channels) not in (3, 4):
            raise ValueError("Colors require 3 RGB or 4 RGBA channels")
        values = tuple(number(c, "channel", minimum=0, maximum=1) for c in channels)
        return cls(values + (1.0,) if len(values) == 3 else values)

    @property
    def rgb(self) -> RGB:
        return self.rgba[:3]

    def hex(self, *, alpha=False, alpha_first=False) -> str:
        values = self.rgba if alpha else self.rgb
        parts = [f"{round(c * 255):02x}" for c in values]
        if alpha and alpha_first:
            parts = parts[-1:] + parts[:-1]
        return "#" + "".join(parts)

    def with_alpha(self, alpha):
        return ColorValue((*self.rgb, number(alpha, "alpha", minimum=0, maximum=1)))

    def over(self, background):
        bg = ColorValue.parse(background)
        a, ba = self.rgba[3], bg.rgba[3]
        out_a = a + ba * (1 - a)
        rgb = tuple((c * a + b * ba * (1 - a)) / out_a if out_a else 0.0
                    for c, b in zip(self.rgb, bg.rgb))
        return ColorValue((*rgb, out_a))
