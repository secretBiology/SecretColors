#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
from importlib import metadata as _metadata

from SecretColors.models.palette import Palette
from SecretColors.cmaps.parent import ColorMap
from SecretColors.models.objects import ColorWheel

try:
    __version__ = _metadata.version("SecretColors")
except _metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Palette", "ColorMap", "ColorWheel", "__version__"]
