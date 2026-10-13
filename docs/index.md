---
hide-toc: true
---

```{image} images/banner.png
:class: sc-banner
:alt: SecretColors
```

# SecretColors

{.sc-tagline}
Beautiful, ready-to-use color palettes and colormaps for Python.
IBM, Material, Adobe Spectrum, ColorBrewer, Tableau and colorblind-safe
schemes - one simple API.

::::{div} sc-buttons
:::{button-ref} getting-started
:color: primary
:shadow:
Get started
:::
:::{button-ref} gallery/palettes
:color: secondary
:outline:
Browse colors
:::
:::{button-link} https://github.com/secretBiology/SecretColors
:color: secondary
:outline:
GitHub
:::
::::

## Install

::::{tab-set}
:::{tab-item} pip
```bash
pip install SecretColors
pip install "SecretColors[all]"   # with matplotlib and Pillow
```
:::
:::{tab-item} uv
```bash
uv add SecretColors
uv add "SecretColors[all]"        # with matplotlib and Pillow
```
:::
:::{tab-item} From GitHub
```bash
pip install "SecretColors[all] @ git+https://github.com/secretBiology/SecretColors"
```
:::
::::

## Thirty seconds tour

```python
from SecretColors import Palette

p = Palette()                   # IBM palette (default)
p.red()                         # '#fa4d56'
p.red(shade=20)                 # '#ffd7d9'  lighter
p.blue(no_of_colors=5)          # ['#edf5ff', '#9bc0ff', '#2a75fe', '#0032a9', '#001141']

from SecretColors import cmaps
cmaps.register()
plt.imshow(data, cmap="sc.Spectral")
```

## Explore

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} {bdg-primary}`8` Palettes
:link: guide/palettes
:link-type: doc

IBM, Material, Spectrum, Clarity, Latitude, ColorBrewer and Tableau, each
with a full range of shades.
:::

:::{grid-item-card} {bdg-success}`83` Colormaps
:link: guide/colormaps
:link-type: doc

Register once and use `cmap="sc.greens"` in matplotlib, pandas or seaborn.
:::

:::{grid-item-card} Plotting
:link: guide/plotting
:link-type: doc

Make SecretColors the default look of your plots, in one line.
:::

:::{grid-item-card} Colorblind friendly
:link: guide/colorblind
:link-type: doc

Okabe-Ito and Paul Tol schemes, plus colorblindness simulation.
:::

:::{grid-item-card} Palette from an image
:link: guide/image-palettes
:link-type: doc

Pull the dominant colors out of any photo.
:::

:::{grid-item-card} Color science
:link: guide/color-science
:link-type: doc

CIE L\*a\*b\*, LCh, Delta E (CIEDE2000) and 16 RGB colorspaces.
:::
::::

```{toctree}
:hidden:
:caption: Get started

getting-started
upgrading
```

```{toctree}
:hidden:
:caption: User guide

guide/palettes
guide/plotting
guide/colormaps
guide/colorblind
guide/image-palettes
guide/harmonies
guide/color-science
```

```{toctree}
:hidden:
:caption: Gallery

gallery/palettes
gallery/colormaps
```

```{toctree}
:hidden:
:caption: API reference

api/palette
api/colormaps
api/colorwheel
api/utils
api/image
```

```{toctree}
:hidden:
:caption: Project

changelog
GitHub <https://github.com/secretBiology/SecretColors>
PyPI <https://pypi.org/project/SecretColors/>
```
