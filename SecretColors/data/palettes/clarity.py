#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# VMWare Clarity Palette
# https://vmware.github.io/clarity/documentation/v0.13/color
# Core color is considered as 70
#
# Latest Clarity color palette (v1.0 version 4)
# has removed all old colors and just kept 4-5 colors needed for their UI. (
# that too in HSL format!!!!). However, we will continue to use their v0.13
# color palette.

from SecretColors.data.palettes.parent import ParentPalette


class ClarityPalette(ParentPalette):
    """
    VMWare Clarity pelette
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self) -> str:
        return "VMWare Clarity Color Palette"

    def get_creator_url(self) -> str:
        return "https://vmware.github.io/clarity/documentation/v0.13/color"

    def get_shades(self) -> list:
        return self.shades

    def get_core_shade(self) -> int:
        return self.core

    def get_version(self) -> int:
        return 1

    def get_last_update(self) -> str:
        return "12 April 2019"

    shades = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    core = 70
    colors = [
        {
            'n': 'red',
            'c': ['#a32100', '#c92100', '#e12200', '#f52f22', '#f54f47',
                  '#f76f6c', '#f89997', '#f8b7b6', '#f5dbd9', '#fff0ee']
        },
        {
            'n': 'pink',
            'c': ['#9b0d54', '#b0105b', '#c41261', '#d91468', '#ed186f',
                  '#f1428a', '#f46ca5', '#f897bf', '#fbc1da', '#ffebf5']
        },
        {
            'n': 'purple',
            'c': ['#4d007a', '#660092', '#781da0', '#8939ad', '#9b56bb',
                  '#ad73c8', '#be90d6', '#d0ace4', '#e1c9f1', '#f3e6ff']
        },
        {
            'n': 'ultramarine',
            'c': ['#0f1e82', '#1a23a0', '#343dac', '#4e56b8', '#6870c4',
                  '#838acf', '#9da3db', '#b7bde7', '#d1d6f3', '#ebf0ff']
        },
        {
            'n': 'blue',
            'c': ['#003d79', '#004d8a', '#0065ab', '#0079b8', '#0095d3',
                  '#49afd9', '#89cbdf', '#a6d8e7', '#c5e5ef', '#e1f1f6']
        },
        {
            'n': 'cyan',
            'c': ['#004a70', '#005680', '#006690', '#0081a7', '#009cbf',
                  '#00b7d6', '#36c9e1', '#6ddbeb', '#a3edf6', '#ccfbff']
        },
        {
            'n': 'teal',
            'c': ['#006668', '#007e7a', '#00968b', '#00ab9a', '#00bfa9',
                  '#00d4b8', '#38dfc8', '#6fead9', '#a7f4e9', '#defff9']
        },
        {
            'n': 'green',
            'c': ['#1d5100', '#266900', '#2f8400', '#48960c', '#62a420',
                  '#60b515', '#85c81a', '#aadb1e', '#c7e59c', '#dff0d0']
        },
        {
            'n': 'yellow',
            'c': ['#c47d00', '#d28f00', '#dfa100', '#edb200', '#fac400',
                  '#fdd006', '#ffdc0b', '#ffe860', '#fef3b5', '#fffce8']
        },
        {
            'n': 'orange',
            'c': ['#aa4500', '#c25400', '#d36000', '#e46c00', '#f57600',
                  '#ff8400', '#ff9c32', '#ffb565', '#ffcd97', '#ffe5c9']
        },
        {
            'n': 'red-orange',
            'c': ['#cd3517', '#de400f', '#ee4a08', '#ff5500', '#ff681c',
                  '#ff8142', '#ff9a69', '#ffb38f', '#ffccb5', '#ffe5dc']
        },
        {
            'n': 'warm-gray',
            'c': ['#5b4d47', '#6c5f59', '#80746d', '#948981', '#a89e95',
                  '#bbb3a9', '#cfc8bd', '#e3ddd1', '#f4f1e6', '#faf9f5']
        },
        {
            'n': 'neutral-gray',
            'c': ['#313131', '#444444', '#565656', '#737373', '#9a9a9a',
                  '#cccccc', '#dddddd', '#eeeeee', '#f2f2f2', '#fafafa']
        },
        {
            'n': 'cool-gray',
            'c': ['#25333d', '#314351', '#495a67', '#61717d', '#798893',
                  '#919fa8', '#a9b6be', '#c1cdd4', '#d9e4ea', '#f3f6fa']
        },
        {
            'n': 'black',
            'c': ['#000000', '#000000', '#000000', '#000000', '#000000',
                  '#000000', '#000000', '#000000', '#000000', '#000000']
        },
        {
            'n': 'white',
            'c': ['#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff',
                  '#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff']
        },
    ]
