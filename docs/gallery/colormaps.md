# Colormap gallery

All 83 colormaps. Use them by name after `cmaps.register()`, or get them
with `cmaps.cmap(name)` and `cmaps.colors(name)`. Every colormap also has a
reversed version with `_r` suffix.

```python
from SecretColors import cmaps
cmaps.register()
plt.imshow(data, cmap="sc.Spectral")
```

## Standard

Generated from the selected palette (IBM by default). Any palette color name
such as `teal` or `magenta` also works with `cmap()` and `colors()`.

```{colormap-swatches} standard
```

## ColorBrewer

From [ColorBrewer](https://colorbrewer2.org/) by Cynthia Brewer.

```{colormap-swatches} brewer
```

## Tableau

From [Tableau](https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm).

```{colormap-swatches} tableau
```

## Colorblind safe

Okabe-Ito (`cud`) and [Paul Tol](https://personal.sron.nl/~pault/) schemes.

```{colormap-swatches} colorblind
```
