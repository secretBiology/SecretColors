## SecretColors

[![PyPI version](https://badge.fury.io/py/SecretColors.svg)](https://badge.fury.io/py/SecretColors) [![Documentation Status](https://readthedocs.org/projects/secretcolors/badge/?version=latest)](https://secretcolors.readthedocs.io/en/latest/?badge=latest) 



Library generated for making plots with better color palette. It uses  famous color palettes and adds few helpful functions.   

Currently it supports following Color Palettes

- IBM Color Palette (`ibm`)
- Google Material Design Color Palette (`material`)
- Google Material Design Accent Color Palette (`material-accent`)
- ColorBrewer2 Color Palette (`brewer`)
- VMWare Clarity Color Palette  (`clarity`)
- Tableau Color Palette (`tableau`)

You can get output of colors in variety of color formats including `hex` , `rgb`, `rgba` etc. 

See [changelog](/CHANGELOG.md) to know what's new!

Few sample plots and inspiration behind this library can be found in [WeirdData blog](https://weirddata.github.io/2019/06/11/secret-colors-2.html). 



|<img src="https://user-images.githubusercontent.com/8757115/69130240-72840d00-0ab0-11ea-8ce5-8b715ebef4f6.png" width="60%">|
|:--:|
| Default base colors in matplotlib and SecretColors palettes. |


|<img src="https://user-images.githubusercontent.com/8757115/69130544-fa6a1700-0ab0-11ea-80f4-aaff9e58f804.png" width="60%">|
|:--:|
| Simple bar plot with default colors. |


|<img src="https://user-images.githubusercontent.com/8757115/69130672-31402d00-0ab1-11ea-835d-b161caf4c24a.png" width="60%">|
|:--:|
| Histogram comparison with Magenta and Cyan. You can dramatically change colors by just passing single parameter. |

### Installation 


    pip install SecretColors


### Documentation

Full documentation and API reference can be accessed via [ReadTheDocs](https://secretcolors.readthedocs.io) 

**SecretColors** is a very flexible library. You can easily select different color palettes.

    from SecretColors import Palette
    
    p = Palette()  # Generates Default color palette i.e. IBM Color Palette
    ibm = Palette("ibm")  # Generates IBM Palette
    ibm.red()  # Returns '#fb4b53'
    material = Palette("material")  # Generates Material Palette
    material.red()  # Returns '#f44336'


Select different types of color modes


    p1 = Palette() # Default Color mode (hex)
    p1.green() # '#24a148'
    p2 = Palette(color_mode="hexa")
    p2.green() # '#24a148ff'
    p3 = Palette(color_mode="ahex")
    p3.green() # '#ff24a148'
    p4 = Palette(color_mode="rgb")
    p4.green() # (0.141, 0.631, 0.282)
    p5 = Palette(color_mode="rgba")
    p5.green() # '(0.141, 0.282, 0.631, 1)'


Note: `matplotlib` can accepts *hex*, *rgb* or *hexa* 

Get random colors

    p = Palette()
    p.random() # '#90dbe9'
    p.random(no_of_colors=3) # ['#8fca39', '#64a0fe', '#7430b6']
    p.random(no_of_colors=2, shade=20) # ['#b3e6ff', '#c2dbf4']


Unlimited color manipulations


    p = Palette()
    p.blue()  # normal blue [#408bfc]
    p.blue(shade=20)  # lighter shade of blue [#c9deff]
    p.blue(shade=70)  # darker shade of blue [#054ada]
    p.blue(shade=16.10)  # arbitrary shade of blue (between 0 to 100) [#dbe9ff]
    p.blue(no_of_colors=3)  # Three blue shades ['#b8d4ff', '#408bfc', '#0546d4']
    p.blue(no_of_colors=3, starting_shade=30)  # Three blue shades with lightest one is 30 ['#64a0fe', '#005ef9', '#052ea8']
    p.blue(no_of_colors=3, ending_shade=40)  # Three blue shades with darkest one is 40 ['#edf4ff', '#c9deff', '#97c1ff']
    p.blue(no_of_colors=3, starting_shade=30, ending_shade=40) # Three blue shades with lightest 30 and darkest 60 ['#8cbaff', '#8cbaff', '#8cbaff']
    p.blue(no_of_colors=3, gradient=False) # Three blue shades in random order ['#8cbaff', '#b8d4ff', '#64a0fe']
    p.color_mode = "rgba"
    p.blue(alpha=0.3) # Blue with alpha (0.251, 0.988, 0.545, 0.3) Only works in color mode which outputs alpha values



Flexible functions


    get_complementary("#24a148") # Get complementary color [#a0237c]
    hex_to_rgb("#a0237c") # (0.627, 0.137, 0.486)
    hex_to_hsl("#a0237c") # (0.881, 0.641, 0.382)
    hex_to_hex_a("#a0237c", alpha=0.7) # Get hex with transparency at end [#a0237cb2]
    hex_to_ahex("#a0237c", alpha=0.7) # Get hex with transparency at start [#b2a0237c]
    color_in_between("#24a148","#a0237c") # Color between two ['#616161']
    color_in_between("#24a148","#a0237c", steps=4) # 3 colors between two ['#428154', '#616161', '#80426e'] such that color space is divided into 4 parts
    rgb_to_hex(0.181, 0.241, 0.382) # '#2e3d61'
    rgb_to_hsl(0.181, 0.241, 0.382) # (0.617, 0.357, 0.281)
    hsl_to_hex(0.181, 0.241, 0.382) # '#747849'



Custom and flexible colormaps which can be directly used in `matplotlib` workflow 


    import matplotlib
    import matplotlib.pylab as plt
    import numpy as np
    from SecretColors.cmaps import ColorMap
    from SecretColors import Palette
    p = Palette()
    c = ColorMap(matplotlib, p)
    data = np.random.rand(100, 100)
    plt.pcolor(data, cmap=c.greens())
    plt.show()


Create your own colormaps or make it *qualitative* colormap


    color_list = [p.red(), p.blue()]
    plt.pcolor(data, cmap=c.from_list(color_list, is_qualitative=True))
    plt.show()


Reverse the direction 


    plt.pcolor(data, cmap=c.greens(is_reversed=True))


### TODO
 - [ ] CIE XYZ to CIE Lab conversions
 - [ ] Color Palettes - Latitude, Polaris, Adobe Spectrum
 - [ ] Direct support for more RGB to XYZ conversions
 - [ ] Generate Color Palette from image
 - [x] Color blind safe palette
 - [ ] ~~Out of the box `LinearSegmentedColormap` object~~ 
 
 We can not implement 'out of the box' colormaps for matplotlib because `matplotlib` checks its
  `type` before its use. Hence we can not make new class which can be directly
   act as a substitute.


Note: All CIE-XYZ conversion and colorblind simulation functions are still in
 beta-testing. Do not use them in your production code

### Contribution and Feedback

Feel free to provide feedback and criticism through GitHub or you can email me [rohitsuratekar@gmail.com ](mailto:rohitsuratekar@gmail.com). If you want to contribute, please send pull request to this repository. 

### Acknowledgments

Colors used in this library are partly taken from [IBM Design Language](https://www.ibm.com/design/language/resources/color-library/) , [Google 
Material Design](https://material.io/design/color/the-color-system.html
) , [ColorBrewer](http://colorbrewer2.org/), [VMWare Clarity ](https://vmware.github.io/clarity/documentation/v0.13/color) and 
[Tableau](https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm#Version_9.x_(legacy)_color_palette_hex_values) .

Color name data is taken from [X11](https://gitlab.freedesktop.org/xorg/app/rgb/raw/master/rgb.txt) 
and [W3]( https://www.w3.org/TR/css-color-3/#svg-color). 

RGB colorspace matrices were taken from [Here](http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html) .

Any other specific code or resource used in this library is attributed in
 respective function or method where it is used. It can be accessible
  from our online documentation as well.


### License 

This library and its code is released under MIT License . Read full statement [here](https://github.com/secretBiology/SecretColors/blob/master/LICENSE). 

