# Getting started

## Installation

::::{tab-set}
:::{tab-item} pip
```bash
pip install SecretColors
```
:::
:::{tab-item} uv
```bash
uv add SecretColors
```
:::
::::

SecretColors needs Python 3.10 or newer and has **no dependencies**.
Optional features are available through extras.

| Extra | Installs | Enables |
|---|---|---|
| *(none)* | nothing | Palettes, shades, `ColorWheel`, conversions, `cmaps.colors()` |
| `[matplotlib]` | matplotlib | `cmaps.cmap()`, `cmaps.register()`, `ColorMap` classes |
| `[image]` | Pillow | `extract_palette()` |
| `[all]` | matplotlib, Pillow | Everything |

```bash
pip install "SecretColors[all]"
```

:::{tip}
Using a feature without its extra raises an `ImportError` which tells you
exactly what to install.
:::

## Your first palette

A {class}`~SecretColors.Palette` is a collection of named colors. Every color
has a full range of shades from 0 (white) to 100 (darkest).

```python
from SecretColors import Palette

p = Palette()                   # IBM palette (default)
p.red()                         # '#fa4d56'
p.red(shade=20)                 # '#ffd7d9'
p.red(shade=80)                 # '#750e13'
p.blue(no_of_colors=3, starting_shade=20, ending_shade=60)
# ['#d0e2ff', '#78a9ff', '#0f62fe']
```

Switch to any other palette by its name.

```python
Palette("material").red()       # '#f44336'
Palette("tableau").blue()       # '#3a87b7'
```

Colors are returned as plain strings (or tuples), so they work with every
plotting library. They also carry a few handy extras.

```python
c = p.red()
c.rgb                           # (0.980, 0.302, 0.337)
c.rgb255                        # (250, 77, 86)
c.blend("#ffffff")              # '#fca6ab'
```

## In Jupyter

Colors, lists of colors and palettes show up as color swatches in Jupyter
notebooks. Lists are still regular Python lists.

```python
Palette("spectrum")                 # all colors of the palette
Palette().blue(no_of_colors=6)
```

## Colormaps in one line

```python
import matplotlib.pyplot as plt
from SecretColors import cmaps

cmaps.register()
plt.imshow(data, cmap="sc.greens")
```

## Where next?

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Palettes
:link: guide/palettes
:link-type: doc
Shades, color modes, random colors and more.
:::

:::{grid-item-card} Colormaps
:link: guide/colormaps
:link-type: doc
Every colormap, and how to use it everywhere.
:::

:::{grid-item-card} Gallery
:link: gallery/palettes
:link-type: doc
Every color of every palette.
:::

:::{grid-item-card} Upgrading from 1.x
:link: upgrading
:link-type: doc
What changed in version 2.
:::
::::
