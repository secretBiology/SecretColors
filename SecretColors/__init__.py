#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
from importlib import metadata as _metadata

from SecretColors.models.palette import Palette, ColorMatch
from SecretColors.cmaps.parent import ColorMap
from SecretColors.models.objects import ColorWheel, ColorString, ColorTuple, ColorList
from SecretColors.selection import check_colors, distinct_colors, ColorReport, DistinctnessWarning

try:
    __version__ = _metadata.version("SecretColors")
except _metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Palette", "ColorMap", "ColorWheel", "distinct_colors",
           "check_colors", "ColorMatch", "ColorString", "ColorTuple", "ColorList",
           "ColorReport", "DistinctnessWarning", "__version__"]
