# Colormaps

```{image} ../images/colormaps-light.png
:class: only-light
:alt: Colormaps
```
```{image} ../images/colormaps-dark.png
:class: only-dark
:alt: Colormaps
```

SecretColors ships 83 colormaps. See all of them in the
{doc}`../gallery/colormaps`.

## Use them by name

Register once, and use any colormap by name, exactly like matplotlib's own.
Every colormap also has a reversed `_r` version.

```python
import matplotlib.pyplot as plt
from SecretColors import cmaps

cmaps.register()

plt.imshow(data, cmap="sc.greens")
plt.imshow(data, cmap="sc.Spectral_r")
df.plot.scatter(x="x", y="y", c="z", cmap="sc.tol_sunset")    # pandas
sns.heatmap(data, cmap="sc.RdBu")                            # seaborn
```

{func}`~SecretColors.cmaps.maps.register` accepts a few options.

```python
cmaps.register(palette="material")   # standard maps (sc.greens ...) from Material
cmaps.register("mylib")              # use 'mylib.greens' instead of 'sc.greens'
cmaps.register(force=True)           # replace already registered maps
```

## Create a colormap object

{func}`~SecretColors.cmaps.maps.cmap` returns a matplotlib colormap which
you can pass directly to `cmap=`.

```python
cmaps.cmap("greens")                          # LinearSegmentedColormap
cmaps.cmap("blues", start=20, end=80)         # only part of the range
cmaps.cmap("Spectral", n=9, reverse=True)
cmaps.cmap("Set2", n=4)                       # ListedColormap (discrete)
cmaps.cmap("teal", palette="material")        # any palette color works
```

| Argument | Meaning |
|---|---|
| `n` | Number of colors. Diverging and sequential maps are interpolated when `n` is not available. Qualitative maps return their first `n` colors. |
| `start`, `end` | Crop the map (0-100). For standard maps these are shades. |
| `discrete` | `True` gives a `ListedColormap`. Default is `True` for qualitative maps. |
| `reverse` | Reverse the order of colors. |
| `palette` | Palette used for standard and color-name maps. |

## Plain colors, no matplotlib

{func}`~SecretColors.cmaps.maps.colors` returns a list of hex colors and has
no dependencies, which makes it perfect for other libraries and the web.

```python
cmaps.colors("Spectral", n=5)
# ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba']
cmaps.available()               # all names
cmaps.available("brewer")       # standard, brewer, tableau or colorblind
```

## Names

| Source | Names | Example |
|---|---|---|
| Standard | `greens`, `reds`, `oranges`, `purples`, `grays`, `blues` | `"sc.greens"` |
| Any palette color | `teal`, `magenta`, `amber` ... (with `cmap()` and `colors()`) | `cmap("teal")` |
| ColorBrewer | 35 maps, e.g. `Spectral`, `RdBu`, `Set1` | `"sc.RdBu"` |
| Tableau | 30 maps, e.g. `Tableau`, `OrangeBlue` | `"sc.OrangeBlue"` |
| Colorblind safe | 12 maps, e.g. `cud`, `tol_sunset` | `"sc.tol_sunset"` |

Names are matched exactly first, then as a palette color, and finally
case-insensitively. So `"Greens"` is ColorBrewer's Greens, `"greens"` is the
palette's standard map, and `"spectral"` finds `"Spectral"`.

## Colormap classes

The classes from earlier versions keep working. Passing matplotlib to them
is optional now.

```python
from SecretColors.cmaps import ColorMap, BrewerMap, TableauMap

ColorMap().greens(starting_shade=20, ending_shade=80, no_of_colors=5)
BrewerMap().spectral(no_of_colors=9)
TableauMap().get("OrangeBlue", no_of_colors=13)
ColorMap().from_list(["#fa4d56", "#ffffff", "#4589ff"])
```
