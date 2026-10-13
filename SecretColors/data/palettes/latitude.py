#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# Flexport Latitude Design System Color Palette
# Source: Latitude 'colors.js' (archived fork of flexport/latitude)
#   https://github.com/auxdesigner/latitude/blob/master/colors.js
# Copyright (c) 2019 Flexport, MIT License
#
# Latitude steps 10-60 are normalized to 15-90 (step * 1.5). Core color is
# step 40.

from SecretColors.data.palettes.parent import ParentPalette


class LatitudePalette(ParentPalette):
    """
    Flexport Latitude Color Palette
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self) -> str:
        return "Flexport Latitude Color Palette"

    def get_creator_url(self) -> str:
        return "https://github.com/auxdesigner/latitude"

    def get_shades(self) -> list:
        return self.shades

    def get_core_shade(self) -> int:
        return self.core

    def get_version(self) -> int:
        return 1

    def get_last_update(self) -> str:
        return "13 October 2026"

    shades = [90, 75, 60, 45, 30, 15]
    core = 60
    colors = [
        {
            'n': 'red',
            'c': ['#800000', '#ba0202', '#d92736', '#fa5959', '#fda6a6',
                  '#fff5f5']
        },
        {
            'n': 'orange',
            'c': ['#5c2500', '#a64300', '#da5a00', '#f5954d', '#fac69d',
                  '#fff7f0']
        },
        {
            'n': 'green',
            'c': ['#008062', '#1db595', '#45dabe', '#82f2da', '#baf8ea',
                  '#f5fffc']
        },
        {
            'n': 'blue',
            'c': ['#0f2943', '#326089', '#6294be', '#94c1df', '#c2e0ef',
                  '#f5fcff']
        },
        {
            'n': 'indigo',
            'c': ['#00108c', '#031aba', '#0723d8', '#566ae5', '#a2acf2',
                  '#f5f6ff']
        },
        {
            'n': 'purple',
            'c': ['#43005c', '#7700a6', '#9200da', '#af50f5', '#cea1fa',
                  '#f9f5ff']
        },
        {
            'n': 'gray',
            'c': ['#39414d', '#4b5564', '#67768d', '#c5d2e7', '#dae3f3',
                  '#f7f9fd']
        }
    ]
