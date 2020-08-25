#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

PALETTE_IBM = "ibm"
PALETTE_MATERIAL = "material"
PALETTE_BREWER = "brewer"
PALETTE_CLARITY = "clarity"
PALETTE_TABLEAU = "tableau"

# Order of following palette will be used to extract the additional color
ALL_PALETTES = [PALETTE_IBM, PALETTE_MATERIAL, PALETTE_BREWER,
                PALETTE_CLARITY, PALETTE_TABLEAU]

MODE_HEX = "hex"
MODE_RGB = "rgb"
MODE_HSL = "hsl"
MODE_RGBA = "rgba"  # With Transparency
MODE_AHEX = "ahex"  # With Transparency
MODE_HSLA = "hsla"  # With Transparency
MODE_HEX_A = "hexa"  # With Transparency

ALL_COLOR_MODES = [MODE_HEX, MODE_AHEX, MODE_RGB, MODE_RGBA, MODE_HSL,
                   MODE_HSLA, MODE_HEX_A]

SYNONYM = {
    "grey": "gray",
    "r": "red",
    "b": "blue",
    "g": "green",
    "c": "cyan",
    "m": "magenta",
    "y": "yellow",
    "k": "black",
    "w": "white"
}
