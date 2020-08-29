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
MODE_RGBA = "rgba"  # With Transparency
MODE_AHEX = "ahex"  # With Transparency
MODE_HEX_A = "hexa"  # With Transparency

ALL_COLOR_MODES = [MODE_HEX, MODE_AHEX, MODE_RGB, MODE_RGBA, MODE_HEX_A]

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

DIV_COLOR_PAIRS = [
    (("red", [60, 40]), ("yellow", [10]), ("green", [40, 60])),
    (("red", [70, 40]), ("white", [10]), ("gray", [20, 100])),
    (("red", [80, 50, 30]), ("white", [10]), ("blue", [30, 50, 80])),
    (("purple", [80, 50, 30]), ("yellow", [10]), ("green", [30, 50, 80])),
    (("pink", [80, 20]), ("white", [10]), ("green", [20, 70])),
    (("brown", [80, 20]), ("white", [10]), ("teal", [20, 80])),
]
