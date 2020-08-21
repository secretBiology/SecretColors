#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  ColorBrewer Color Palette
#  http://colorbrewer2.org/
#  Only SingleHue colors are considered here

from SecretColors.data.palettes.parent import ParentPalette


class ColorBrewer(ParentPalette):
    """
    Color Brewer Color Paletter
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self) -> str:
        return "Color Brewer Color Palette"

    def get_creator_url(self) -> str:
        return "http://colorbrewer2.org/"

    def get_shades(self) -> list:
        return self.shades

    def get_core_shade(self) -> int:
        return self.core

    def get_version(self) -> int:
        return 1

    def get_last_update(self) -> str:
        return "12 April 2019"

    shades = [90, 80, 70, 60, 50, 40, 30, 20, 10]
    core = 60
    colors = [
        {
            'n': 'blue',
            'c': ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6',
                  '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff']
        },
        {
            'n': 'purple',
            'c': ['#3f007d', '#54278f', '#6a51a3', '#807dba', '#9e9ac8',
                  '#bcbddc', '#dadaeb', '#efedf5', '#fcfbfd']
        },
        {
            'n': 'green',
            'c': ['#00441b', '#006d2c', '#238b45', '#41ab5d', '#74c476',
                  '#a1d99b', '#c7e9c0', '#e5f5e0', '#f7fcf5']
        },
        {
            'n': 'orange',
            'c': ['#7f2704', '#a63603', '#d94801', '#f16913', '#fd8d3c',
                  '#fdae6b', '#fdd0a2', '#fee6ce', '#fff5eb']
        },
        {
            'n': 'red',
            'c': ['#67000d', '#a50f15', '#cb181d', '#ef3b2c', '#fb6a4a',
                  '#fc9272', '#fcbba1', '#fee0d2', '#fff5f0']
        },
        {
            'n': 'gray',
            'c': ['#000000', '#252525', '#525252', '#737373', '#969696',
                  '#bdbdbd', '#d9d9d9', '#f0f0f0', '#ffffff']
        },
        {
            'n': 'black',
            'c': ['#000000', '#000000', '#000000', '#000000', '#000000',
                  '#000000', '#000000', '#000000', '#000000']
        },
        {
            'n': 'white',
            'c': ['#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff',
                  '#ffffff', '#ffffff', '#ffffff', '#ffffff']
        },
    ]
