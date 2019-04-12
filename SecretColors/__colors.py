"""
SecretColors 2019
Author: Rohit Suratekar

IBM Color Palette
(https://www.ibm.com/design/language/elements/color/)
Last Update: 10 April 2019
This contain colors from v2 as well as v1

Material Design Colors
(https://material.io/design/color/#color-theme-creation)

"""

from SecretColors.__color import Color

PALETTE_IBM = "ibm"
PALETTE_MATERIAL = "material"

ALL_PALETTES = [PALETTE_IBM, PALETTE_MATERIAL]

TYPE_CORE = "core"  # Regular Color
TYPE_GRAY = "gray"  # White, Black and shades of Grey
TYPE_EXTRA = "extra"  # Special palette specific colors

MODE_HEX = "hex"
MODE_RGB = "rgb"
MODE_HSL = "hsl"


class ParentPalette:
    """
    Base class to create new colors
    """

    def get_all_colors(self) -> list:
        """
        :return: List of all colors
        """
        raise NotImplementedError

    def get_palette_name(self) -> str:
        """
        :return: Name of the color palette
        """
        raise NotImplementedError

    def get_creator_url(self) -> str:
        """
        :return: URL of the original resource
        """
        raise NotImplementedError

    def get_shades(self) -> list:
        """
        :return: List of original shades. Note: This will be normalized
        between 0 - 100
        """
        raise NotImplementedError

    def get_core_shade(self) -> int:
        """
        :return: Shade of core color
        """
        raise NotImplementedError

    def get_version(self) -> int:
        """
        :return: Palette version used in this library
        """
        raise NotImplementedError

    def get_last_update(self) -> str:
        """
        :return: Date of last modification happened in this library
        """
        raise NotImplementedError


class IBMPalette(ParentPalette):
    """
    IBM Color Palette
    """

    def get_last_update(self):
        return "10 April 2019"

    def get_version(self):
        return 2

    def get_shades(self):
        return self.shades

    def get_core_shade(self):
        return self.core

    def get_creator_url(self) -> str:
        return "https://www.ibm.com/design/language/elements/color/"

    def get_all_colors(self):
        return [Color(x, self.shades, self.core) for x in self.colors]

    def get_palette_name(self) -> str:
        return "IBM Color Palette"

    shades = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    core = 60
    colors = [
        {
            'n': 'red',
            't': TYPE_CORE,
            'c': ['#2c080a', '#570408', '#750e13', '#a51920', '#da1e28',
                  '#fb4b53', '#ff767c', '#ffa4a9', '#fcd0d3', '#fff0f1']
        },
        {
            'n': 'magenta',
            't': TYPE_CORE,
            'c': ['#2a0a16', '#57002b', '#760a3a', '#a11950', '#d12765',
                  '#ee538b', '#fa75a6', '#ffa0c2', '#ffcfe1', '#fff0f6']
        },
        {
            'n': 'purple',
            't': TYPE_CORE,
            'c': ['#1e1033', '#38146b', '#4f2196', '#6e32c9', '#8a3ffc',
                  '#a66efa', '#bb8eff', '#d0b0ff', '#e6d6ff', '#f7f1ff']
        },
        {
            'n': 'blue',
            't': TYPE_CORE,
            'c': ['#051243', '#061f80', '#0530ad', '#054ada', '#0062ff',
                  '#408bfc', '#6ea6ff', '#97c1ff', '#c9deff', '#edf4ff']
        },
        {
            'n': 'cyan',
            't': TYPE_CORE,
            'c': ['#07192b', '#002b50', '#003d73', '#0058a1', '#0072c3',
                  '#1191e6', '#30b0ff', '#6ccaff', '#b3e6ff', '#e3f6ff']
        },
        {
            'n': 'teal',
            't': TYPE_CORE,
            'c': ['#081a1c', '#003137', '#004548', '#006161', '#007d79',
                  '#009c98', '#00bab6', '#20d5d2', '#92eeee', '#dbfbfb']
        },
        {
            'n': 'green',
            't': TYPE_CORE,
            'c': ['#081b09', '#01330f', '#054719', '#10642a', '#198038',
                  '#24a148', '#3dbb61', '#56d679', '#9deeb2', '#dafbe4']
        },
        {
            'n': 'cool-gray',
            't': TYPE_GRAY,
            'c': ['#13171a', '#242a2e', '#373d42', '#50565b', '#697077',
                  '#868d95', '#9fa5ad', '#b9bfc7', '#d5d9e0', '#f2f4f8']
        },
        {
            'n': 'gray',
            't': TYPE_GRAY,
            'c': ['#171717', '#282828', '#3d3d3d', '#565656', '#6f6f6f',
                  '#8c8c8c', '#a4a4a4', '#bebebe', '#dcdcdc', '#f3f3f3']
        },
        {
            'n': 'warm-gray',
            't': TYPE_GRAY,
            'c': ['#1a1717', '#2b2828', '#403c3c', '#595555', '#726e6e',
                  '#8f8b8b', '#a7a2a2', '#c1bcbb', '#e0dbda', '#f7f3f1']
        },
        {
            'n': 'black',
            't': TYPE_GRAY,
            'c': ['#000000']
        },
        {
            'n': 'white',
            't': TYPE_GRAY,
            'c': ['#ffffff']
        },
        {
            'n': 'ultramarine',
            't': TYPE_EXTRA,
            'c': ['#20214f', '#252e6a', '#2e3f8f', '#3151b7', '#3c6df0',
                  '#648fff', '#89a2f6', '#b0bef3', '#d1d7f4', '#e7e9f7']
        },
        {
            'n': 'cerulean',
            't': TYPE_EXTRA,
            'c': ['#1b2834', '#1d364d', '#1c496d', '#175d8d', '#047cc0',
                  '#009bef', '#56acf2', '#95c4f3', '#c2dbf4', '#deedf7']
        },
        {
            'n': 'aqua',
            't': TYPE_EXTRA,
            'c': ['#122a2e', '#13393e', '#164d56', '#17616b', '#188291',
                  '#12a3b4', '#00b6cb', '#71cddd', '#a0e3f0', '#d1f0f7']
        },
        {
            'n': 'lime',
            't': TYPE_EXTRA,
            'c': ['#1f2a10', '#283912', '#374c1a', '#426200', '#5b8121',
                  '#73a22c', '#81b532', '#95d13c', '#b4e876', '#d7f4bd']
        },
        {
            'n': 'yellow',
            't': TYPE_CORE,
            'c': ['#372118', '#452f18', '#5b421a', '#70541b', '#91721f',
                  '#b3901f', '#c6a21a', '#e3bc13', '#fed500', '#fbeaae']
        },
        {
            'n': 'gold',
            't': TYPE_EXTRA,
            'c': ['#2f261c', '#42301b', '#5b421c', '#74521b', '#9c6d1e',
                  '#c4881c', '#e39d14', '#ffb000', '#ffd191', '#f5e8db']
        },
        {
            'n': 'orange',
            't': TYPE_CORE,
            'c': ['#33241c', '#482e1a', '#653d1b', '#814b19', '#ad6418',
                  '#db7c00', '#fe8500', '#fcaf6d', '#fdcfad', '#f5e8de']
        },
        {
            'n': 'peach',
            't': TYPE_EXTRA,
            'c': ['#3a201b', '#56251a', '#782f1c', '#993a1d', '#c45433',
                  '#fe6100', '#fc835c', '#faad96', '#f8d0c3', '#f7e7e2']
        },
        {
            'n': 'violet',
            't': TYPE_CORE,
            'c': ['#321c4c', '#44216a', '#602797', '#7732bb', '#9753e1',
                  '#b07ce8', '#bf93eb', '#d2b5f0', '#e2d2f4', '#ece8f5']
        },
        {
            'n': 'indigo',
            't': TYPE_CORE,
            'c': ['#272149', '#352969', '#473793', '#5a3ec8', '#785ef0',
                  '#9b82f3', '#ae97f4', '#c7b6f7', '#dcd4f7', '#e9e8ff']

        }

    ]


class MaterialPalette(ParentPalette):
    """
    Material Design Color Palette
    """

    def get_all_colors(self):
        return [Color(x, self.shades, self.core) for x in self.colors]

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

    shades = [900, 800, 700, 600, 500, 400, 300, 200, 100, 50]
    core = 500
    colors = [
        {
            'n': 'red',
            't': TYPE_CORE,
            'c': ['#b71c1c', '#c62828', '#d32f2f', '#e53935', '#f44336',
                  '#ef5350', '#e57373', '#ef9a9a', '#ffcdd2', '#ffebee']
        },
        {
            'n': 'pink',
            't': TYPE_CORE,
            'c': ['#880e4f', '#ad1457', '#c2185b', '#d81b60', '#e91e63',
                  '#ec407a', '#f06292', '#f48fb1', '#f8bbd0', '#fce4ec']
        },
        {
            'n': 'purple',
            't': TYPE_CORE,
            'c': ['#4a148c', '#6a1b9a', '#7b1fa2', '#8e24aa', '#9c27b0',
                  '#ab47bc', '#ba68c8', '#ce93d8', '#e1bee7', '#f3e5f5']
        },
        {
            'n': 'deep-purple',
            't': TYPE_EXTRA,
            'c': ['#311b92', '#4527a0', '#512da8', '#5e35b1', '#673ab7',
                  '#7e57c2', '#9575cd', '#b39ddb', '#d1c4e9', '#ede7f6']
        },
        {
            'n': 'indigo',
            't': TYPE_CORE,
            'c': ['#1a237e', '#283593', '#303f9f', '#3949ab', '#3f51b5',
                  '#5c6bc0', '#7986cb', '#9fa8da', '#c5cae9', '#e8eaf6']
        },
        {
            'n': 'blue',
            't': TYPE_CORE,
            'c': ['#0d47a1', '#1565c0', '#1976d2', '#1e88e5', '#2196f3',
                  '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb', '#e3f2fd']
        },
        {
            'n': 'light-blue',
            't': TYPE_EXTRA,
            'c': ['#01579b', '#0277bd', '#0288d1', '#039be5', '#03a9f4',
                  '#29b6f6', '#4fc3f7', '#81d4fa', '#b3e5fc', '#e1f5fe']
        },
        {
            'n': 'cyan',
            't': TYPE_CORE,
            'c': ['#006064', '#00838f', '#0097a7', '#00acc1', '#00bcd4',
                  '#26c6da', '#4dd0e1', '#80deea', '#b2ebf2', '#e0f7fa']
        },
        {
            'n': 'teal',
            't': TYPE_CORE,
            'c': ['#004d40', '#00695c', '#00796b', '#00897b', '#009688',
                  '#26a69a', '#4db6ac', '#80cbc4', '#b2dfdb', '#e0f2f1']
        },
        {
            'n': 'green',
            't': TYPE_CORE,
            'c': ['#1b5e20', '#2e7d32', '#388e3c', '#43a047', '#4caf50',
                  '#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9', '#e8f5e9']
        },
        {
            'n': 'light-green',
            't': TYPE_EXTRA,
            'c': ['#33691e', '#558b2f', '#689f38', '#7cb342', '#8bc34a',
                  '#9ccc65', '#aed581', '#c5e1a5', '#dcedc8', '#f1f8e9']
        },
        {
            'n': 'lime',
            't': TYPE_EXTRA,
            'c': ['#827717', '#9e9d24', '#afb42b', '#c0ca33', '#cddc39',
                  '#d4e157', '#dce775', '#e6ee9c', '#f0f4c3', '#f9fbe7']
        },
        {
            'n': 'yellow',
            't': TYPE_CORE,
            'c': ['#f57f17', '#f9a825', '#fbc02d', '#fdd835', '#ffeb3b',
                  '#ffee58', '#fff176', '#fff59d', '#fff9c4', '#fffde7']
        },
        {
            'n': 'amber',
            't': TYPE_EXTRA,
            'c': ['#ff6f00', '#ff8f00', '#ffa000', '#ffb300', '#ffc107',
                  '#ffca28', '#ffd54f', '#ffe082', '#ffecb3', '#fff8e1']
        },
        {
            'n': 'orange',
            't': TYPE_CORE,
            'c': ['#e65100', '#ef6c00', '#f57c00', '#fb8c00', '#ff9800',
                  '#ffa726', '#ffb74d', '#ffcc80', '#ffe0b2', '#fff3e0']
        },
        {
            'n': 'deep-orange',
            't': TYPE_EXTRA,
            'c': ['#bf360c', '#d84315', '#e64a19', '#f4511e', '#ff5722',
                  '#ff7043', '#ff8a65', '#ffab91', '#ffccbc', '#fbe9e7']
        },
        {
            'n': 'brown',
            't': TYPE_CORE,
            'c': ['#3e2723', '#4e342e', '#5d4037', '#6d4c41', '#795548',
                  '#8d6e63', '#a1887f', '#bcaaa4', '#d7ccc8', '#efebe9']
        },
        {
            'n': 'gray',
            't': TYPE_GRAY,
            'c': ['#212121', '#424242', '#616161', '#757575', '#9e9e9e',
                  '#bdbdbd', '#e0e0e0', '#eeeeee', '#f5f5f5', '#fafafa']
        },
        {
            'n': 'blue-gray',
            't': TYPE_GRAY,
            'c': ['#263238', '#37474f', '#455a64', '#546e7a', '#607d8b',
                  '#78909c', '#90a4ae', '#b0bec5', '#cfd8dc', '#eceff1']
        },
        {
            'n': 'black',
            't': TYPE_GRAY,
            'c': ['#000000']
        },
        {
            'n': 'white',
            't': TYPE_GRAY,
            'c': ['#ffffff']
        }

    ]
