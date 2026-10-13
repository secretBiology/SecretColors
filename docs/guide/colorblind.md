# Colorblind friendly

:::{seealso}
{doc}`distinct-colors` picks and checks colorblind-safe colors for you.
:::

```{image} ../images/colorblind-light.png
:class: only-light
:alt: Colorblind simulation
```
```{image} ../images/colorblind-dark.png
:class: only-dark
:alt: Colorblind simulation
```

About 1 in 12 men see red and green as similar, muddy tones. Colors that
look perfectly distinct to you might be indistinguishable to your readers.

## Colorblind safe schemes

SecretColors includes the Okabe-Ito palette[^okabe] and Paul Tol's
schemes[^tol], designed to stay distinct for all common types of
colorblindness.

```{colormap-swatches} colorblind
```

```python
from SecretColors import cmaps

cmaps.colors("cud")             # Okabe-Ito (Color Universal Design)
cmaps.colors("tol_bright")      # qualitative
cmaps.cmap("tol_sunset")        # diverging
cmaps.cmap("tol_yl_or_br")      # sequential
```

## Simulate colorblindness

Check how your own colors look to people with protanopia (red blindness) or
deuteranopia (green blindness).

```python
from SecretColors.utils import (hex_to_rgb, rgb_to_hex,
                                simulate_red_blindness,
                                simulate_green_blindness)

def deuteranopia(color):
    return rgb_to_hex(*simulate_green_blindness(*hex_to_rgb(color)))

deuteranopia("#fa4d56")         # how red looks without green cones
```

Combine it with {func}`~SecretColors.utils.delta_e` to check if two colors
stay distinguishable.

```python
from SecretColors.utils import delta_e

delta_e(deuteranopia("#fa4d56"), deuteranopia("#24a148"))
# a small value means the two colors look alike
```

:::{note}
Simulations are approximations of how dichromats see color. They are useful
for spotting problems, not as a medical tool.
:::

[^okabe]: Okabe M. and Ito K., [Color Universal Design](https://jfly.uni-koeln.de/color/).
[^tol]: Paul Tol, [Colour Schemes](https://personal.sron.nl/~pault/).
