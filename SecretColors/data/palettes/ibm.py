#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  IBM Color Palette
#  (https://www.ibm.com/design/language/elements/color/)
#  Last Update: 10 April 2019
#  This contain colors from v2 as well as v1

from SecretColors.data.palettes.parent import ParentPalette


class IBMPalette(ParentPalette):
    """
    IBM Color Palette
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_last_update(self):
        return "22 August 2020"

    def get_version(self):
        return 3

    def get_shades(self):
        return self.shades

    def get_core_shade(self):
        return self.core

    def get_creator_url(self) -> str:
        return "https://www.ibm.com/design/language/elements/color/"

    def get_palette_name(self) -> str:
        return "IBM Color Palette"

    shades = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    core = 50
    colors = [
        {
            'n': 'red',
            'c': ['#2d0709', '#520408', '#750e13', '#a2191f', '#da1e28',
                  '#fa4d56', '#ff8389', '#ffb3b8', '#ffd7d9', '#fff1f1'],
            'c_old': ['#2c080a', '#570408', '#750e13', '#a51920', '#da1e28',
                      '#fb4b53', '#ff767c', '#ffa4a9', '#fcd0d3', '#fff0f1']
        },
        {
            'n': 'magenta',
            'c': ['#2a0a18', '#510224', '#740937', '#9f1853', '#d12771',
                  '#ee5396', '#ff7eb6', '#ffafd2', '#ffd6e8', '#fff0f7'],
            'c_old': ['#2a0a16', '#57002b', '#760a3a', '#a11950', '#d12765',
                      '#ee538b', '#fa75a6', '#ffa0c2', '#ffcfe1', '#fff0f6']
        },
        {
            'n': 'purple',
            'c': ['#1c0f30', '#31135e', '#491d8b', '#6929c4', '#8a3ffc',
                  '#a56eff', '#be95ff', '#d4bbff', '#e8daff', '#f6f2ff'],
            'c_old': ['#1e1033', '#38146b', '#4f2196', '#6e32c9', '#8a3ffc',
                      '#a66efa', '#bb8eff', '#d0b0ff', '#e6d6ff', '#f7f1ff']
        },
        {
            'n': 'blue',
            'c': ['#001141', '#001d6c', '#002d9c', '#0043ce', '#0f62fe',
                  '#4589ff', '#78a9ff', '#a6c8ff', '#d0e2ff', '#edf5ff'],
            'c_old': ['#051243', '#061f80', '#0530ad', '#054ada', '#0062ff',
                      '#408bfc', '#6ea6ff', '#97c1ff', '#c9deff', '#edf4ff']
        },
        {
            'n': 'cyan',
            'c': ['#061727', '#012749', '#003a6d', '#00539a', '#0072c3',
                  '#1192e8', '#33b1ff', '#82cfff', '#bae6ff', '#e5f6ff'],
            'c_old': ['#07192b', '#002b50', '#003d73', '#0058a1', '#0072c3',
                      '#1191e6', '#30b0ff', '#6ccaff', '#b3e6ff', '#e3f6ff']
        },
        {
            'n': 'teal',
            'c': ['#081a1c', '#022b30', '#004144', '#005d5d', '#007d79',
                  '#009d9a', '#08bdba', '#3ddbd9', '#9ef0f0', '#d9fbfb'],
            'c_old': ['#081a1c', '#003137', '#004548', '#006161', '#007d79',
                      '#009c98', '#00bab6', '#20d5d2', '#92eeee', '#dbfbfb']
        },
        {
            'n': 'green',
            'c': ['#071908', '#022d0d', '#044317', '#0e6027', '#198038',
                  '#24a148', '#42be65', '#6fdc8c', '#a7f0ba', '#defbe6'],
            'c_old': ['#081b09', '#01330f', '#054719', '#10642a', '#198038',
                      '#24a148', '#3dbb61', '#56d679', '#9deeb2', '#dafbe4']
        },
        {
            'n': 'cool-gray',
            'c': ['#121619', '#21272a', '#343a3f', '#4d5358', '#697077',
                  '#878d96', '#a2a9b0', '#c1c7cd', '#dde1e6', '#f2f4f8'],
            'c_old': ['#13171a', '#242a2e', '#373d42', '#50565b', '#697077',
                      '#868d95', '#9fa5ad', '#b9bfc7', '#d5d9e0', '#f2f4f8']
        },
        {
            'n': 'gray',
            'c': ['#161616', '#262626', '#393939', '#525252', '#6f6f6f',
                  '#8d8d8d', '#a8a8a8', '#c6c6c6', '#e0e0e0', '#f4f4f4'],
            'c_old': ['#171717', '#282828', '#3d3d3d', '#565656', '#6f6f6f',
                      '#8c8c8c', '#a4a4a4', '#bebebe', '#dcdcdc', '#f3f3f3']
        },
        {
            'n': 'warm-gray',
            'c': ['#171414', '#272525', '#3c3838', '#565151', '#736f6f',
                  '#8f8b8b', '#ada8a8', '#cac5c4', '#e5e0df', '#f7f3f2'],
            'c_old': ['#1a1717', '#2b2828', '#403c3c', '#595555', '#726e6e',
                      '#8f8b8b', '#a7a2a2', '#c1bcbb', '#e0dbda', '#f7f3f1']
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
        {
            'n': 'ultramarine',
            'c': ['#20214f', '#252e6a', '#2e3f8f', '#3151b7', '#3c6df0',
                  '#648fff', '#89a2f6', '#b0bef3', '#d1d7f4', '#e7e9f7']
        },
        {
            'n': 'cerulean',
            'c': ['#1b2834', '#1d364d', '#1c496d', '#175d8d', '#047cc0',
                  '#009bef', '#56acf2', '#95c4f3', '#c2dbf4', '#deedf7']
        },
        {
            'n': 'aqua',
            'c': ['#122a2e', '#13393e', '#164d56', '#17616b', '#188291',
                  '#12a3b4', '#00b6cb', '#71cddd', '#a0e3f0', '#d1f0f7']
        },
        {
            'n': 'lime',
            'c': ['#1f2a10', '#283912', '#374c1a', '#426200', '#5b8121',
                  '#73a22c', '#81b532', '#95d13c', '#b4e876', '#d7f4bd']
        },
        {
            'n': 'yellow',
            'c': ['#372118', '#452f18', '#5b421a', '#70541b', '#91721f',
                  '#b3901f', '#c6a21a', '#e3bc13', '#fed500', '#fbeaae']
        },
        {
            'n': 'gold',
            'c': ['#2f261c', '#42301b', '#5b421c', '#74521b', '#9c6d1e',
                  '#c4881c', '#e39d14', '#ffb000', '#ffd191', '#f5e8db']
        },
        {
            'n': 'orange',
            'c': ['#33241c', '#482e1a', '#653d1b', '#814b19', '#ad6418',
                  '#db7c00', '#fe8500', '#fcaf6d', '#fdcfad', '#f5e8de']
        },
        {
            'n': 'peach',
            'c': ['#3a201b', '#56251a', '#782f1c', '#993a1d', '#c45433',
                  '#fe6100', '#fc835c', '#faad96', '#f8d0c3', '#f7e7e2']
        },
        {
            'n': 'violet',
            'c': ['#321c4c', '#44216a', '#602797', '#7732bb', '#9753e1',
                  '#b07ce8', '#bf93eb', '#d2b5f0', '#e2d2f4', '#ece8f5']
        },
        {
            'n': 'indigo',
            'c': ['#272149', '#352969', '#473793', '#5a3ec8', '#785ef0',
                  '#9b82f3', '#ae97f4', '#c7b6f7', '#dcd4f7', '#e9e8ff']

        }

    ]
