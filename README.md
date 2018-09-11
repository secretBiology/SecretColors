# Secret Colors

[![PyPI version](https://badge.fury.io/py/SecretColors.svg)](https://badge.fury.io/py/SecretColors)

Library generated for making plots with better color palette. It uses 
famous color palettes 
and adds few helpful functions. 

### Installation 

    pip install SecretColors

### Usage
Select different Palettes
    
    from SecretColors.palette import Palette
    ibm = Palette("ibm")  # IBM Palette
    material = Palette("material")  # Material Palette

Get Common Colors

    ibm.red()  # Default Red color from IBM palette (#008673)
    ibm.cerulean()  # Default Cerulean color from IBM palette (#009bef)

Shades of colors
    
    ibm.red(grade=10)  # Light Red with grade 10 (#fccec7)
    ibm.red(grade=80)  # Dark Red with grade 80 (#5c1f1b)
    ibm.red(grade=10000)  # Maximum/Minimum will be automatically adjusted (#3e1d1b)

Number of colors

    reds = ibm.red(no_of_colors=5)  # List of 3 Red colors from IBM palette
    dark_reds = ibm.red(no_of_colors=5, start_from=40)  # List of 3 Red 
    colors from IBM palettes starting from grade 40
 
Random Colors

    ibm.random()  # Random color from IBM Palette
    ibm.random(grade=60)  # Random color from grade 60
    ibm.random(no_of_colors=10)  # 10 Random colors
    ibm.random(no_of_colors=10, grade=30)  # Random colors with grade

Gradients between colors

    ibm.gradient_between(ibm.red(), ibm.blue(), no_of_colors=5)
    # Gradient between your own custom colors
    ibm.gradient_between("#b73752", "#2d74da", no_of_colors=5)

Palette output in other color-spaces

    ibm.change_color_mode("rgb")
    ibm.red()  # (0.90, 0.13, 0.14)

General Conversion Functions

    from SecretColors.palette import hex_to_rgb, hex_to_hsv, rgb_to_hex
    hex_to_rgb("#b73752")  # (0.71, 0.21, 0.32)
    hex_to_hsv("#b73752")  # (0.96, 0.69, 183.0)
    rgb_to_hex((0.71, 0.21, 0.32))  # #b53551

Text contrast on background color

    from SecretColors.palette import text_color
    text_color("#e62325")  # Returns #ffffff. This suggest white color text will
    # have good contrast on given color
    text_color("#eabbbc")  # Returns #000000. Suggesting black color text will have
    #  good contrast on given color

Simple Usage with `matplotlib`

    import matplotlib.pylab as plt
    import numpy as np
    
    data = np.random.randint(10, 50, 5)
    plt.bar(range(len(data)), data, color=ibm.blue(no_of_colors=len(data), start_from=30))
    plt.show()

Few sample plots and inspiration behind this library can be found in 
[WeirdData blog](https://weirddata.github.io/2018/09/10/secret-colors.html). 


### TODO

- [x] IBM Color Palette
- [x] Color gradients
- [x] Google Material Design Palette
- [x] Text contrast detection
- [x] Matplotlib `cmap` helper functions
- [ ] ColorBrewer Palette
- [ ] VMware Palette

### Acknowledgments
Colors used in this library are partly taken from [IBM Design Language](https://www.ibm.com/design/language/resources/color-library/) and [Google 
Material Design](https://material.io/design/color/the-color-system.html)  