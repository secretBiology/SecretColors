#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Tableau v9 color maps
#  Hex values taken from their legacy help page
#  https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm#Version_9.x_(legacy)_color_palette_hex_values
#
#  Note: Current version of their color palette is v10
#  Red and Gray palettes are restructured to fit the common shade difference
#  Shades are calculated such that they will be distributed between 0 to 100

from SecretColors.data.palettes.parent import ParentPalette


class TableauPalette(ParentPalette):
    """
    Tableau v9 palettes
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self) -> str:
        return "Tableau Palette"

    def get_creator_url(self) -> str:
        return "https://help.tableau.com/current/pro/desktop/en-us" \
               "/formatting_create_custom_colors.htm#Version_9.x_(" \
               "legacy)_color_palette_hex_values "

    def get_shades(self) -> list:
        return self.shades

    def get_core_shade(self) -> int:
        return self.core

    def get_version(self) -> int:
        return 1

    def get_last_update(self) -> str:
        return "25 August 2020"

    shades = [91, 78, 65, 52, 39, 26, 13]
    core = 52
    colors = [
        {
            'n': 'red',
            'c': ['#b10c1d', '#c21417', '#cf1719', '#d8392c', '#e35745',
                  '#f57667', '#f89a90']
        },
        {
            "n": "green",
            "c": ['#09622a', '#1a7232', '#27823b', '#339444', '#69a761',
                  '#94bb83', '#bccfb4']
        },
        {
            "n": "gray",
            "c": ['#1e1e1e', '#333333', '#4b4b4b', '#666666', '#838383',
                  '#a2a2a2', '#c3c3c3']
        },
        {
            "n": "blue",
            "c": ['#26456e', '#1c5998', '#1c73b1', '#3a87b7', '#67add4',
                  '#7bc8e2', '#b4d4da']

        },
        {
            "n": "orange",
            "c": ['#7b3014', '#a33202', '#d74401', '#f06511', '#fd8938',
                  '#fdab67', '#f0c294']
        },
        {
            'n': 'black',
            'c': ['#000000', '#000000', '#000000', '#000000', '#000000',
                  '#000000', '#000000']
        },
        {
            'n': 'white',
            'c': ['#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff',
                  '#ffffff', '#ffffff']
        }

    ]
