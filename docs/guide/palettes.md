# Palettes

```{image} ../images/palettes-light.png
:class: only-light
:alt: Available palettes
```
```{image} ../images/palettes-dark.png
:class: only-dark
:alt: Available palettes
```

## Available palettes

| Name | Source | Colors | Shades | License |
|---|---|---|---|---|
| `ibm` *(default)* | [IBM Design Language](https://www.ibm.com/design/language/color/) | 20 | 10 | |
| `material` | [Google Material Design](https://m2.material.io/design/color/the-color-system.html) | 19 | 10 | |
| `material-accent` | Material Design accent colors | 16 | 4 | |
| `spectrum` | [Adobe Spectrum](https://spectrum.adobe.com/page/color-palette/) | 18 | 16 | Apache-2.0 |
| `clarity` | [VMware Clarity](https://clarity.design/) | 14 | 10 | |
| `latitude` | [Flexport Latitude](https://github.com/auxdesigner/latitude) | 7 | 6 | MIT |
| `brewer` | [ColorBrewer](https://colorbrewer2.org/) | 6 | 9 | |
| `tableau` | [Tableau](https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm) | 5 | 7 | |

See every color of every palette in the {doc}`../gallery/palettes`.

```python
from SecretColors import Palette

p = Palette("spectrum")
p.name                          # 'spectrum'
p.creator_url                   # 'https://spectrum.adobe.com/page/color-palette/'
p.color_list                    # all colors at their default shade
p.color_dict                    # {'red': '#d73220', ...}
for color in p:                 # iterate over all colors
    ...
```

## Getting a color

Every common color has its own method.

```python
p = Palette()
p.red(), p.blue(), p.green(), p.purple(), p.magenta(), p.teal(), p.gray()
```

```{dropdown} All color methods
`amber`, `aqua`, `black`, `blue`, `blue_light`, `brown`, `cerulean`, `cyan`,
`gold`, `gray`, `gray_blue`, `gray_cool`, `gray_neutral`, `gray_warm`,
`green`, `green_light`, `indigo`, `lime`, `magenta`, `orange`,
`orange_deep`, `peach`, `pink`, `purple`, `purple_deep`, `red`,
`red_orange`, `teal`, `ultramarine`, `violet`, `white`, `yellow`
```

Use {meth}`~SecretColors.Palette.get` for any color by name. If a color is
not part of the current palette, SecretColors looks for it in the following
order.

1. The current palette
2. Other palettes (e.g. `amber` is not in IBM, so Material's amber is used)
3. Common spellings and matplotlib's one letter names (`grey`, `k`, `r` ...)
4. [CSS](https://www.w3.org/TR/css-color-3/#svg-color) and
   [X11](https://gitlab.freedesktop.org/xorg/app/rgb/raw/master/rgb.txt) color names

```python
p = Palette()
p.get("amber")                  # '#ffc107'
p.get("grey"), p.get("k")       # ('#8d8d8d', '#000000')
p.get("aquamarine")             # '#7fffd4'
p.get("gray", strict_search=True)                   # '#808080'  CSS gray only
p.get("gray", naming="x11", strict_search=True)     # '#bebebe'  X11 gray only
```

## Shades

```{image} ../images/shades-light.png
:class: only-light
:alt: Shades
```
```{image} ../images/shades-dark.png
:class: only-dark
:alt: Shades
```

Every color is a smooth gradient. `shade` can be any number between 0 and
100, not just the shades defined by the palette.

```python
p.blue(shade=20)                # '#d0e2ff'
p.blue(shade=37.5)              # any value works
p.blue(n=5)          # 5 evenly spaced shades
p.blue(n=3, start=20, end=60)
# ['#d0e2ff', '#78a9ff', '#0f62fe']
p.blue(n=4, gradient=False)    # random shades
```

## Color modes and transparency

Choose the output format with `color_mode`.

| Mode | Example | Alpha |
|---|---|---|
| `hex` *(default)* | `'#24a148'` | |
| `hexa` | `'#24a14880'` | yes |
| `ahex` | `'#8024a148'` | yes |
| `rgb` | `(0.141, 0.631, 0.282)` | |
| `rgba` | `(0.141, 0.631, 0.282, 0.5)` | yes |

```python
Palette(color_mode="rgba").green(alpha=0.5)
# (0.141, 0.631, 0.282, 0.5)
```

## Random colors

```python
p = Palette(seed=42)            # reproducible results
p.random()                      # one random color
p.random(n=3, shade=30)     # ['#a6c8ff', '#ffb3b8', '#c6c6c6']
p.random(n=5, avoid=["gray"])
p.random_gradient(n=5)      # between two complementary colors
```

:::{note}
`seed` only affects that palette. The global `random` module is never
touched.
:::

## Infinite color cycle

{meth}`~SecretColors.Palette.cycle` keeps producing distinct colors, which is
handy when you do not know in advance how many series you will plot.

```python
for color, (name, data) in zip(Palette().cycle(), groups.items()):
    plt.plot(data, color=color, label=name)

from itertools import islice
list(islice(Palette().cycle(), 5))
# ['#8a3ffc', '#b3901f', '#9f1853', '#009d9a', '#993a1d']
```

Colors come in the same order as {func}`~SecretColors.distinct_colors`: every
next color is the most distinct one from the colors before it, also for
colorblind readers, with enough contrast against the background. When all
colors of the palette are used, the cycle starts again.

```python
Palette().cycle(background="#161616")   # for dark themes
Palette("material").cycle()             # any palette
Palette().cycle(skip_first=2)           # start from the third color
```

:::{tip}
Readers can reliably tell apart about 8 categorical colors. With more
categories, consider grouping the smallest ones into "Other" or using small
multiples. Small palettes such as `tableau` and `clarity` have fewer distinct
colors to offer.
:::
