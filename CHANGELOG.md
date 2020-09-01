# Changelog
# v1.2.0
This is one of the major updates since the conception of this project. Many
 changes are essential for robust functionality and proper code maintenance
 . This
 has introduced the following important changes
 * Probably the most important change in this version is return values. Any
  color you generate with this library will return `ColorString` or
   `ColorTuple` (depending on `color_mode`) which are subclasses of `str` and
    `tuple` respectively. This will NOT change anything in your workflow. Check the full documentation for its
      use cases.
 * `SecretColors.palettes` is now `SecretColors.models.palettes.Palette
 `. However, if
  you have used `from SecretColors import palette`, your code will NOT be
   impacted. We recommend importing this way.
 * `ColorMap` is now `SecretColors.cmaps.ColorMap`. You should import it as
  `from SecretColors.cmaps import ColorMap`
 * `Palette.color_between` is now deprecated. Use `utils.color_in_between
 ` instead. Using this function will raise `AttributeError`.
 * Using shade value less than 0 or greater than 100 will throw a `ValueError`.
 * `allow_gray_shades` argument from `Palette` is deprecated and will be
  ignored.
 * `ignore_gray` and `force_gray` arguments from `Palette.random()` are
  deprecated and will be ignored.
 * `starting_shade` and `ending_shade` values (if not provided by user) will
  be set to minimum and maximum shades available in that palette instead 0
   and 100.
 
 ### What's New?
 * New return class `ColorString` and `ColorTuple`
 * New `ColorWheel` for more scientific use
 * New color palette: Tableau
 * Rewritten `ColorMap` class with new usage and easy colormap access to
  famous color palettes.
 * New `Palette.get()` function which supports all X11 and W3 standard names.
 * Many new RGB space conversions (including *XYZ, adobe, srgb, lab* etc)
 * Many new utility methods (check documentation for details)
 * And of course, fixed many bugs!
  
 ### Known Issues
 #### Pycharm type-hinting not working for 'color methods'

We have shifted to custom decorators for dynamically creating
 documentation of many class methods. However, due to this change
 , Pycharm will not show typehint for 'color methods' It is known [bug
 ](https://youtrack.jetbrains.com/issue/PY-30190) in PyCharm regarding type hinting.
 
 #### Converted RGB/CMYK values are not exact
 
 This issue arises when one performs multiple conversion (specially the one
  involving floating points). For example, take a look at following code,
  
 ```python
from SecretColors.utils import rgb_to_hex, hex_to_rgb

r, g, b = 0.3, 0.5, 0.7
hex_color = rgb_to_hex(r, g, b)  # hex_color: #4c80b2
hex_to_rgb(hex_color) # Retuns (0.2980392156862745, 0.5019607843137255, 0.6980392156862745)
```

In the above code, conversion from RGB to HEX and then from HEX to RGB does 
not give us the same output. This issue is very typical of any programming
 language where we are dealing with float calculations. So you should use
   some rounding logic if you want to compare it with original color

In case of conversion to HEX, we usually round the floats to nearest
 integers with default `round` function. 
 
However, our benchmarks and testing suggest that these values are accurate 
with an error of '0.001'. We also check this during our testings. This much 
precision should be good enough for most of the cases. In case, you want even 
better precision, we kindly ask you to implement the method by yourself 
instead of a depending method provided by `SecretColors`. In future, 
we plan to take a look at this in more details. But for now, 
the workaround is to make some rounding function like following
 


 ```python
# Use precision for rounding according to your need
def rounded_rgb(*args):
    return tuple(round(x,2) for x in args)

rounded_rgb(hex_to_rgb(hex_color)) # returns (0.3, 0.5, 0.7)
```

Note: All CIE-XYZ conversion and colorblind simulation functions are still in
 beta-testing. Do not use them in your production code