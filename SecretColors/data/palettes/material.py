#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
#  Material Design Colors
#  (https://material.io/design/color/#color-theme-creation)
#
#  Material Design palette was originally developed in 2014.

from SecretColors.data.palettes.parent import ParentPalette


class MaterialPalette(ParentPalette):
    """
    Material Design Color Palette
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self):
        return "Material Design Colors"

    def get_creator_url(self):
        return "https://material.io/tools/color"

    def get_shades(self):
        return self.shades

    def get_core_shade(self):
        return self.core

    def get_version(self):
        return 1

    def get_last_update(self):
        return "7 September 2018"

    # shades = [900, 800, 700, 600, 500, 400, 300, 200, 100, 50]
    # We will directly use the normalized shades instead handling it in class
    shades = [90, 80, 70, 60, 50, 40, 30, 20, 10, 5]
    core = 50
    colors = [
        {
            'n': 'red',
            'c': ['#b71c1c', '#c62828', '#d32f2f', '#e53935', '#f44336',
                  '#ef5350', '#e57373', '#ef9a9a', '#ffcdd2', '#ffebee']
        },
        {
            'n': 'pink',
            'c': ['#880e4f', '#ad1457', '#c2185b', '#d81b60', '#e91e63',
                  '#ec407a', '#f06292', '#f48fb1', '#f8bbd0', '#fce4ec']
        },
        {
            'n': 'purple',
            'c': ['#4a148c', '#6a1b9a', '#7b1fa2', '#8e24aa', '#9c27b0',
                  '#ab47bc', '#ba68c8', '#ce93d8', '#e1bee7', '#f3e5f5']
        },
        {
            'n': 'deep-purple',
            'c': ['#311b92', '#4527a0', '#512da8', '#5e35b1', '#673ab7',
                  '#7e57c2', '#9575cd', '#b39ddb', '#d1c4e9', '#ede7f6']
        },
        {
            'n': 'indigo',
            'c': ['#1a237e', '#283593', '#303f9f', '#3949ab', '#3f51b5',
                  '#5c6bc0', '#7986cb', '#9fa8da', '#c5cae9', '#e8eaf6']
        },
        {
            'n': 'blue',
            'c': ['#0d47a1', '#1565c0', '#1976d2', '#1e88e5', '#2196f3',
                  '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb', '#e3f2fd']
        },
        {
            'n': 'light-blue',
            'c': ['#01579b', '#0277bd', '#0288d1', '#039be5', '#03a9f4',
                  '#29b6f6', '#4fc3f7', '#81d4fa', '#b3e5fc', '#e1f5fe']
        },
        {
            'n': 'cyan',
            'c': ['#006064', '#00838f', '#0097a7', '#00acc1', '#00bcd4',
                  '#26c6da', '#4dd0e1', '#80deea', '#b2ebf2', '#e0f7fa']
        },
        {
            'n': 'teal',
            'c': ['#004d40', '#00695c', '#00796b', '#00897b', '#009688',
                  '#26a69a', '#4db6ac', '#80cbc4', '#b2dfdb', '#e0f2f1']
        },
        {
            'n': 'green',
            'c': ['#1b5e20', '#2e7d32', '#388e3c', '#43a047', '#4caf50',
                  '#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9', '#e8f5e9']
        },
        {
            'n': 'light-green',
            'c': ['#33691e', '#558b2f', '#689f38', '#7cb342', '#8bc34a',
                  '#9ccc65', '#aed581', '#c5e1a5', '#dcedc8', '#f1f8e9']
        },
        {
            'n': 'lime',
            'c': ['#827717', '#9e9d24', '#afb42b', '#c0ca33', '#cddc39',
                  '#d4e157', '#dce775', '#e6ee9c', '#f0f4c3', '#f9fbe7']
        },
        {
            'n': 'yellow',
            'c': ['#f57f17', '#f9a825', '#fbc02d', '#fdd835', '#ffeb3b',
                  '#ffee58', '#fff176', '#fff59d', '#fff9c4', '#fffde7']
        },
        {
            'n': 'amber',
            'c': ['#ff6f00', '#ff8f00', '#ffa000', '#ffb300', '#ffc107',
                  '#ffca28', '#ffd54f', '#ffe082', '#ffecb3', '#fff8e1']
        },
        {
            'n': 'orange',
            'c': ['#e65100', '#ef6c00', '#f57c00', '#fb8c00', '#ff9800',
                  '#ffa726', '#ffb74d', '#ffcc80', '#ffe0b2', '#fff3e0']
        },
        {
            'n': 'deep-orange',
            'c': ['#bf360c', '#d84315', '#e64a19', '#f4511e', '#ff5722',
                  '#ff7043', '#ff8a65', '#ffab91', '#ffccbc', '#fbe9e7']
        },
        {
            'n': 'brown',
            'c': ['#3e2723', '#4e342e', '#5d4037', '#6d4c41', '#795548',
                  '#8d6e63', '#a1887f', '#bcaaa4', '#d7ccc8', '#efebe9']
        },
        {
            'n': 'gray',
            'c': ['#212121', '#424242', '#616161', '#757575', '#9e9e9e',
                  '#bdbdbd', '#e0e0e0', '#eeeeee', '#f5f5f5', '#fafafa']
        },
        {
            'n': 'blue-gray',
            'c': ['#263238', '#37474f', '#455a64', '#546e7a', '#607d8b',
                  '#78909c', '#90a4ae', '#b0bec5', '#cfd8dc', '#eceff1']
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
