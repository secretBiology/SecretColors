#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main classes will go in this file


class PaletteColor:
    def __init__(self, palette: str, shades: list):
        self.palette_name = palette
        self.shades = shades


class Color(PaletteColor):
    def __init__(self, name, color_list: list, palette: str, shades: list):
        super().__init__(palette, shades)
        self.name = name  # type: str
        self.color_list = color_list
