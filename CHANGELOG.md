# Changelog

## v2.2.0
* Correct alpha-first parsing, immutable color value representations, and transparent contrast checks.
* Add `with_alpha()`, canonical hex serialization and alpha-aware, validated notebook swatches.
* Fix RGB/RGBA colormap inputs and isolate shared source datasets from caller mutations.
* Honor Lab/LCh interpolation for palette shades while preserving default RGB outputs.
* Add distinctness thresholds and warn/raise/ignore policies; preserve selection ordering.
* Cache candidate snapshots and incrementally extend selections; respect customized palettes.
* Add `Palette.color()`, `sample()`, `resolve()`, palette-only lookup and source provenance.
* Add `cmaps.from_colors()`, colormap metadata and gradient/grayscale/gamut diagnostics.
* Standardize numeric validation and public argument names; old names and colormap classes
  emit DeprecationWarning and will be removed in the next major release.
* Ship typing metadata; exercise dependency-free installs, minimum dependencies and built wheels in CI.
* See the upgrade guide for behavior changes, including immutable channels and alpha quantization.

## v2.1.1
* Updated PyPI project description to match the current README.

## v2.1.0
* Requires Python 3.11+ (Python 3.10 support dropped). Python 3.10 users
  will continue to get v2.0.x from pip.
* Optional `image` extra now requires `pillow>=13.0` to pick up security
  fixes (CVE-2026-112395, CVE-2026-112397, CVE-2026-112400, CVE-2026-112404,
  CVE-2026-112895, CVE-2026-112896, CVE-2026-112897, CVE-2026-112899).
* Development lockfile: `certifi` 2026.10.19 and `uv` 0.13.4 (security fixes).

## v2.0.0
### New palettes and features
* New palettes: Adobe Spectrum (`Palette("spectrum")`) and Flexport Latitude
  (`Palette("latitude")`).
* `SecretColors.image.extract_palette()` generates a color palette from an
  image (needs `pip install "SecretColors[image]"`).
* CIE-L\*a\*b\* support: `xyz_to_lab`, `lab_to_xyz`, `rgb_to_lab`,
  `lab_to_rgb`, `hex_to_lab`, `lab_to_hex`, `lab_to_lch`, `lch_to_lab`.
* `delta_e()` measures perceptual color difference (CIEDE2000 or CIE76).
* `rgb_to_xyz` / `xyz_to_rgb` accept `space=` for all 16 supported RGB
  colorspaces (e.g. `pro_photo`, `wide_gamut`, `apple`). `rgb_spaces()`
  lists them. Unknown colorspace or white reference raises `ValueError`
  (earlier `AttributeError`).
* `distinct_colors(n)` picks colors which stay distinct for normal vision,
  protanopia and deuteranopia and have enough contrast with the background.
  `check_colors()` reports how distinct any set of colors is.
* `Palette.cycle()` yields colorblind-safe distinct colors in the same order
  as `distinct_colors()`, so it can be used directly in loops. Earlier
  sequence had red next to green and low contrast yellow. New `background`
  and `colorblind_safe` arguments.
* WCAG accessibility: `contrast_ratio()` and `is_readable()`.
  `relative_luminance()` accepts RGB tuples as well.
* Perceptual mixing: `mix()`, and `space="lab"` / `"lch"` option in
  `color_in_between()`, `ColorString.blend()`, `cmaps.colors()` and
  `cmaps.cmap()` for smoother gradients. `blend()` accepts `ratio`.
* Colors, lists of colors, palettes and `ColorWheel` show swatches in Jupyter
  notebooks. Functions returning several colors return `ColorList`, a
  regular `list` subclass. `ColorWheel.color` returns `ColorString`.
### New colormap API
* `SecretColors.cmaps.register()` registers every colormap (and its
  reversed `_r` version) in matplotlib with `sc.` prefix. Use them by name
  anywhere matplotlib colormap names are accepted, e.g.
  `plt.imshow(data, cmap="sc.greens")`.
* `SecretColors.cmaps.cmap(name, ...)` returns matplotlib colormap object
  directly. matplotlib is imported automatically, no need to pass it.
* `SecretColors.cmaps.colors(name, ...)` returns plain hex colors which can
  be used with any library (plotly, bokeh, altair, seaborn, CSS). It does not
  need matplotlib.
* `SecretColors.cmaps.available()` lists all colormap names.
* Colorblind safe colormaps (Okabe-Ito `cud` and Paul Tol's schemes) are
  now accessible.
* Diverging and sequential colormaps can be interpolated to any number of
  colors and cropped with `start` / `end`.
* `ColorMap`, `BrewerMap` and `TableauMap` work as before. Passing
  `matplotlib` to them is optional now.
### Bug fixes
* Fixed invalid color in Paul Tol's `tol_bu_rd` colormap.
* `hexa` / `ahex` color modes now encode alpha on the 0-255 scale. Earlier,
  fully opaque colors were written as `64` (~39% opacity) instead of `ff`.
* `Palette.random()` no longer crashes when more colors are requested than
  the number of standard shades available.
* Iterating over a `Palette` (`for c in Palette()`) works.
* `Palette.random_gradient()` no longer randomly raises `IndexError`.
* `shade=0` is respected instead of being treated as "not provided".
* Fixed sRGB gamma transform (`apply_gamma_transform`).
* `hsv_to_rgb` accepts hue value of 1.
* `cmy_to_cmyk(1, 1, 1)` returns pure black instead of raising
  `ZeroDivisionError`.
* `relative_luminance` / `text_color` accept 8-character hex codes.
* `xyz_to_rgb` / `xyz_to_adobe_rgb` accept XYZ values greater than 1, and
  `rgb_to_xyz` / `adobe_rgb_to_xyz` no longer clip XYZ values at 1.
* `simulate_red_blindness` / `simulate_green_blindness` now follow the
  published formula.
* `ColorWheel.rotate_saturation` / `rotate_lightness` clamp between 0-100%
  instead of wrapping (e.g. white no longer turns black).
* `ColorMap.random_divergent()` respects `is_qualitative` and `is_reversed`.
* `BrewerMap` and `TableauMap` accept `log` and `seed` arguments like
  `ColorMap`.
### Behaviour changes
* Unknown palette names raise `ValueError` instead of silently falling back
  to IBM palette.
* `ColorString` / `ColorTuple` no longer override `+`. Normal string / tuple
  concatenation works again. Use `ColorString.blend(other)` to mix colors.
* Looking up colors from other palettes or named colors (e.g. `Palette.get
  ("amber")`) no longer adds them to `Palette.colors`, `get_color_list` or
  the pool used by `Palette.random()`.
* `seed` in `Palette` and `ColorMap` uses a private random generator; global
  `random` state is not modified anymore.
* Logging uses the `SecretColors` logger, attaches handlers only once and no
  longer changes global `warnings` filters.
* ColorMap errors raise `ValueError` instead of bare `Exception`.
* `rgb_to_srgb` / `srgb_to_rgb` are deprecated in favour of correctly named
  `srgb_to_linear` / `linear_to_srgb`.
* `Palette.get_color_dict` / `Palette.get_color_list` are deprecated in
  favour of `Palette.color_dict` / `Palette.color_list`.
* Removed `Palette.color_between` (deprecated since v1.2.0, use
  `SecretColors.utils.color_in_between`) and `Palette.cmap_from` (deprecated
  since v1.2.0, use `ColorMap.from_list`).
### Packaging
* Moved to `pyproject.toml` (hatchling) and [uv](https://docs.astral.sh/uv/).
  `setup.py` and `requirements*.txt` are removed.
* Requires Python 3.10+. Tested on Python 3.10 - 3.14.
* Optional extras: `pip install "SecretColors[matplotlib]"` (colormap
  objects), `"SecretColors[image]"` (palettes from images) or
  `"SecretColors[all]"` (everything). The core library has no dependencies.
* `SecretColors.__version__` is available.
* New documentation with user guide, palette and colormap galleries, upgrade
  guide and light / dark theme: https://secretcolors.readthedocs.io
## v1.2.6
Removed dependency on `numpy` (Thanks to [ri0t](https://github.com/ri0t))
## v1.2.5
New Color Palette `material-accent` which supports accent colors of Google 
Material Design Color Palette.
## v1.2.3
Added new method to `Palette` class. `Palette.cycle()` will return a 
generator to produce infinite color cycle. Read documentation for 
further 
details. 
## v1.2.2
Fixed bug where `Palette.random()` raising error if `no_of_colors` 
parameter is greater than one.
## v1.2.1
Removed the restrictions from `numpy` version [ see [Issue](https://github.com/secretBiology/SecretColors/issues/4) ]
## v1.2.0
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