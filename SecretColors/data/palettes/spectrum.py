#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# Adobe Spectrum 2 Color Palette (light theme)
# https://spectrum.adobe.com/page/color-palette/
# Source: https://github.com/adobe/spectrum-design-data
#   packages/tokens/src/color-palette.json
# Copyright Adobe, Apache License 2.0
#
# Spectrum steps 100-1600 are normalized to 0-100 (step / 16). Core color is
# step 900. Spectrum's 'gray' is a UI neutral scale with different steps, hence
# the 'silver' hue (which has all 16 steps) is used as 'gray'.

from SecretColors.data.palettes.parent import ParentPalette


class SpectrumPalette(ParentPalette):
    """
    Adobe Spectrum 2 Color Palette
    """

    def get_all_colors(self) -> dict:
        return {x["n"]: x["c"] for x in self.colors}

    def get_palette_name(self) -> str:
        return "Adobe Spectrum Color Palette"

    def get_creator_url(self) -> str:
        return "https://spectrum.adobe.com/page/color-palette/"

    def get_shades(self) -> list:
        return self.shades

    def get_core_shade(self) -> float:
        return self.core

    def get_version(self) -> int:
        return 2

    def get_last_update(self) -> str:
        return "13 October 2026"

    shades = [100.0, 93.75, 87.5, 81.25, 75.0, 68.75, 62.5, 56.25, 50.0, 43.75, 37.5, 31.25, 25.0, 18.75, 12.5, 6.25]
    core = 56.25
    colors = [
        {
            'n': 'red',
            'c': ['#1d0502', '#3b0b04', '#501006', '#68150a', '#811b0e',
                  '#9c2113', '#b72818', '#d73220', '#f03823', '#ff513d',
                  '#ff7665', '#ff9d91', '#ffbcb4', '#ffd6d1', '#ffebe8',
                  '#fff6f5']
        },
        {
            'n': 'orange',
            'c': ['#190800', '#341200', '#491800', '#5f2000', '#762900',
                  '#903300', '#a73e00', '#c24e00', '#d45b00', '#e86a00',
                  '#fc7d00', '#ffa213', '#ffc15e', '#ffda9e', '#ffeccf',
                  '#fff6e7']
        },
        {
            'n': 'yellow',
            'c': ['#120b00', '#281900', '#382300', '#4b2f00', '#5d3b00',
                  '#724800', '#865500', '#9e6600', '#af7400', '#c18300',
                  '#d29500', '#e6af00', '#f5c700', '#ffde2c', '#fff197',
                  '#fff8cc']
        },
        {
            'n': 'chartreuse',
            'c': ['#0b0e00', '#191e00', '#232b00', '#2f3900', '#3c4700',
                  '#495700', '#566700', '#667a00', '#728900', '#809900',
                  '#8fac00', '#a3c400', '#b6db00', '#d0ec46', '#eaf6ad',
                  '#f6fbde']
        },
        {
            'n': 'celery',
            'c': ['#040f00', '#0c2100', '#132e00', '#1b3c03', '#234b06',
                  '#2c5c09', '#346d0c', '#408111', '#489014', '#52a119',
                  '#5db41f', '#6ece2a', '#81e43a', '#9df75c', '#c5ff9c',
                  '#ebffdc']
        },
        {
            'n': 'green',
            'c': ['#000f0c', '#002119', '#002e22', '#003d2c', '#014c34',
                  '#025d3c', '#036e45', '#05834e', '#079355', '#0ba45d',
                  '#12b867', '#2bd17d', '#6be3a2', '#adeec5', '#d7f7e1',
                  '#edfcf1']
        },
        {
            'n': 'seafoam',
            'c': ['#000f0e', '#00211d', '#002e28', '#003c36', '#014b43',
                  '#035c50', '#056c5c', '#07816d', '#099078', '#0ba286',
                  '#0db595', '#10cfa9', '#5ce1c2', '#a9edd8', '#d3f6ea',
                  '#ebfbf6']
        },
        {
            'n': 'cyan',
            'c': ['#000e14', '#001f2b', '#002b3b', '#00394e', '#004762',
                  '#005779', '#046691', '#0b78b3', '#1286cd', '#1d95e7',
                  '#30a7fe', '#5cc0ff', '#8ad5ff', '#b7e7fc', '#d9f4fd',
                  '#eefafe']
        },
        {
            'n': 'blue',
            'c': ['#070b1e', '#0e1843', '#0c1f69', '#10288c', '#1532ad',
                  '#1d3ecf', '#274dea', '#3b63fb', '#4b75ff', '#5d89ff',
                  '#729efd', '#8eb9fc', '#accffd', '#cbe2fe', '#e5f0fe',
                  '#f5f9ff']
        },
        {
            'n': 'indigo',
            'c': ['#110036', '#1f0062', '#2a0081', '#3706a0', '#4513bf',
                  '#5424db', '#6338ee', '#7155fa', '#7a6afd', '#8480fe',
                  '#9197fe', '#a7b2ff', '#c0c9ff', '#d8deff', '#ebeeff',
                  '#f7f8ff']
        },
        {
            'n': 'purple',
            'c': ['#17002d', '#2c0054', '#3b006f', '#4b0090', '#5d00b1',
                  '#730dcc', '#8628d9', '#9a47e2', '#a65ce7', '#b272eb',
                  '#bf8aee', '#d0a7f3', '#ddc1f6', '#ebdaf9', '#f4ebfc',
                  '#fbf7fe']
        },
        {
            'n': 'fuchsia',
            'c': ['#1d0023', '#360042', '#480058', '#5c046d', '#710f83',
                  '#871b9a', '#9c28af', '#b539c8', '#c844dc', '#df4df5',
                  '#ec69ff', '#f393ff', '#f7b5ff', '#fad3ff', '#fde9ff',
                  '#fef6ff']
        },
        {
            'n': 'magenta',
            'c': ['#23000c', '#400016', '#56001e', '#6f0028', '#880033',
                  '#a3053e', '#ba1650', '#d92361', '#f02d6e', '#ff4885',
                  '#ff709f', '#ff98bb', '#ffb9d0', '#ffd5e3', '#ffe8f0',
                  '#fff5f8']
        },
        {
            'n': 'pink',
            'c': ['#210015', '#3e0027', '#530035', '#690344', '#800c55',
                  '#981668', '#b01f7b', '#ce2a92', '#e434a3', '#f24cb8',
                  '#ff67cc', '#ff94db', '#ffb5e6', '#ffd3f0', '#ffe8f7',
                  '#fff6fc']
        },
        {
            'n': 'turquoise',
            'c': ['#000f11', '#002023', '#002c31', '#003b41', '#014a51',
                  '#035a62', '#056b74', '#087e89', '#0a8d99', '#0c9eab',
                  '#0fb1c0', '#27cad8', '#6fdde4', '#a9eced', '#d1f5f5',
                  '#eefbfb']
        },
        {
            'n': 'cinnamon',
            'c': ['#180802', '#341204', '#481906', '#5c230b', '#6e3015',
                  '#803e20', '#934d2b', '#aa5e38', '#b86d46', '#c67e58',
                  '#d4916c', '#e5aa88', '#edc4ac', '#f4dacb', '#f9ece5',
                  '#fdf7f3']
        },
        {
            'n': 'brown',
            'c': ['#100c04', '#261a09', '#34250d', '#463111', '#583d15',
                  '#674c23', '#775b32', '#8b6d42', '#9a7b4d', '#ab8a5a',
                  '#be9b68', '#d6b17b', '#e5c89d', '#efddc3', '#f7eee1',
                  '#fcf7f2']
        },
        {
            'n': 'gray',
            'c': ['#0c0c0c', '#1c1c1c', '#272727', '#343434', '#424242',
                  '#515151', '#606060', '#727272', '#808080', '#8f8f8f',
                  '#a0a0a0', '#b7b7b7', '#cccccc', '#dfdfdf', '#efefef',
                  '#f7f7f7']
        }
    ]
