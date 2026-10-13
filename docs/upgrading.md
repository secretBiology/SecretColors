# Upgrading from 1.x

Version 2.0 fixes many long standing bugs and modernises the library. Most
code keeps working. This page lists everything that may need a change.

## Requirements

- Python **3.10** or newer.
- matplotlib is optional. Install `SecretColors[matplotlib]` (or `[all]`)
  if you use colormaps.

## Behaviour changes

| 1.x | 2.0 | What to do |
|---|---|---|
| Unknown palette name silently used IBM | Raises `ValueError` | Check the palette name |
| `ColorString + "text"` mixed colors | Normal string concatenation | Use `color.blend(other)` to mix colors |
| `hexa` / `ahex` alpha used 0-100 scale (opaque was `64`) | Uses 0-255 scale (opaque is `ff`) | Nothing, colors are now correct |
| `p.get("amber")` added colors to `p.colors` | Palette is never modified | Nothing |
| `seed=` changed global `random` state | Uses a private generator | Seed `random` yourself if you relied on it |
| `ColorWheel.rotate_lightness()` wrapped around | Clamps between 0-100% | Nothing |
| Unknown RGB colorspace raised `AttributeError` | Raises `ValueError` | Catch `ValueError` |

## Renamed and removed

| 1.x | 2.0 |
|---|---|
| `Palette.get_color_list` | `Palette.color_list` (old name is deprecated) |
| `Palette.get_color_dict` | `Palette.color_dict` (old name is deprecated) |
| `utils.rgb_to_srgb` | `utils.srgb_to_linear` (old name is deprecated) |
| `utils.srgb_to_rgb` | `utils.linear_to_srgb` (old name is deprecated) |
| `Palette.color_between` | Removed, use `utils.color_in_between` |
| `Palette.cmap_from` | Removed, use `ColorMap().from_list` |

## Colormaps

`ColorMap(matplotlib)` still works, but passing matplotlib is no longer
needed. The new functional API is simpler.

```python
# 1.x
import matplotlib
from SecretColors.cmaps import ColorMap
plt.imshow(data, cmap=ColorMap(matplotlib).greens())

# 2.0
from SecretColors import cmaps
plt.imshow(data, cmap=cmaps.cmap("greens"))
# or register once and use names everywhere
cmaps.register()
plt.imshow(data, cmap="sc.greens")
```

See the {doc}`changelog` for the complete list of changes.
