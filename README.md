# Secret Colors

[![PyPI version](https://badge.fury.io/py/SecretColors.svg)](https://badge.fury.io/py/SecretColors)

Library generated for making plots with better color palette. It uses 
famous color palettes 
and adds few helpful functions. 

### Installation 

    pip install SecretColors

### Usage
Simple use will be 
    
    from SecretColors.palette import IBMPalette
    palette = IBMPalette()
    palette.red() # Red color from IBM palette
    # Most of the color have 10 grades 1,10,20...90
    palette.red(grade=1) # Lighter Red Color
    palette.red(grade=90) # Darker Red Color
    palette.red(no_of_colors=2) # Two grades of Reds
    palette.random # Random color from the palette 
    palette.uniform_colors(10) # 10 colors from uniform gradient
    palette.uniform_colors_between(10, '#648fff', '#00aa5e') # 10 colors from
     uniform gradient between #648fff and #00aa5e

Plus it has few standard conversion methods

    from SecretColors.palette import *
    
    rgb_to_hex((0, 170, 94)) # Converts RGB to Hex
    rgb_to_hsv((0, 170, 94)) # Converts RGB to HSV
    hex_to_rgb('#00aa5e') # Converts Hex to RGB
    color_in_between('#00aa5e', '#95d13c') # Color beteen two in RGB space

### TODO

- [x] IBM Color Palette
- [x] Color gradients
- [ ] Google Material Design Palette
- [ ] Text contrast detection
- [ ] ColorBrewer Palette
- [ ] Matplotlib `cmap` helper functions

### Acknowledgments
Colors used in this library are partly taken from [IBM Design Language](https://www.ibm.com/design/language/resources/color-library/) and [Google 
Material Design](https://material.io/design/color/the-color-system.html)  