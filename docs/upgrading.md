# Upgrading

## Upgrading to 2.2: compatibility and correctness

Default opaque palette colors, curated colormap samples, seeded random
sequences and the existing distinct-color ordering are preserved. Corrections
to alpha handling and explicitly requested Lab/LCh interpolation can change
results. Existing default-output fingerprints are tested against the previous
implementation.

### Deprecated aliases

Every alias below emits `DeprecationWarning` and **will be removed in the next
major release**. Enable these warnings with `python -Wd` during migration.
Supplying both spellings of one argument raises `TypeError`.

| Deprecated | Replacement |
|---|---|
| `no_of_colors=` | `n=` |
| `starting_shade=` / `ending_shade=` | `start=` / `end=` |
| `is_qualitative=` | `discrete=` |
| `is_reversed=` | `reverse=` |
| `ColorWheel.triadic(is_reserved=...)` | `ColorWheel.triadic(reverse=...)` |
| `ColorMap`, `BrewerMap`, `TableauMap` | `cmaps.cmap`, `cmaps.colors`, `cmaps.from_colors` |
| Colormap instance `.no_of_colors` | `.n` (while migrating off the class API) |
| `Palette.get_color_list` / `get_color_dict` | `color_list` / `color_dict` |
| `utils.rgb_to_srgb` / `srgb_to_rgb` | `srgb_to_linear` / `linear_to_srgb` |

Legacy colormap classes retain their historical count validation and defaults;
the functional API can interpolate unsupported sizes and infers qualitative
maps automatically. Choose `discrete=` explicitly when matching a legacy map.

### Color value corrections

Color objects are immutable. Replace `c.alpha = 0.5` with
`c = c.with_alpha(0.5)`. Construct a new color to change RGB channels.
`ColorString` still inherits `str`; `ColorTuple` still inherits `tuple`.
Their native payload and conversion properties now agree. String output
normalizes whitespace, case, shorthand and missing `#`. `.hex` always returns
`#rrggbb`; `.hexa` returns `#rrggbbaa`; `.ahex` returns `#aarrggbb`.
Eight-bit alpha is quantized: the `80` channel corresponds to `128/255`, not
exactly `0.5`. RGBA tuples preserve floating-point alpha.

`ColorString(value, alpha_first=True)` explicitly parses alpha-first hex.
`Palette(color_mode="ahex")` sets this automatically. Converting that object
to a plain string loses its encoding metadata; do not pass a plain alpha-first
string to CSS or Matplotlib, which expect alpha last.

Colormap data is read-only. `get_colors()` and `cmaps.colors()` return independent
lists. Editing a returned list no longer changes future calls.

### Accessibility and interpolation

`contrast_ratio(foreground, background)` composites foreground alpha onto an
opaque background. It is symmetric only when both colors are opaque.
Transparent backgrounds require an explicit canvas: composite them first with
`utils.composite()`. `text_color(color, background=canvas)` supports this directly.
`check_colors()` compares displayed colors and rejects transparent inputs when
`background=None`. `relative_luminance()` remains a raw RGB-channel calculation
and explicitly ignores alpha. `mix()`, `blend()` and `color_in_between()`
interpolate alpha separately and return alpha-last hex for transparent results;
use `composite()` for source-over compositing.

`distinct_colors()` optimizes separation; it does not guarantee accessibility
for every viewer. It evaluates normal vision, protanopia and deuteranopia.
`min_delta_e=10` and `on_failure="warn"` are the defaults. Use `"raise"` for an
enforced threshold or `"ignore"` for deliberate best-effort selection. Ordering
never changes silently to satisfy a threshold. `Palette.cycle()` repeats a
finite candidate pool; later colors need not remain distinguishable.

`space="lab"` and `space="lch"` now apply to palette-derived interpolation,
including `Palette.sample()` and `Palette.red(shade=..., space=...)`. RGB remains
the default, including its historical shade quantization. Perceptual
interpolation can leave the sRGB gamut; see `diagnostics.check_interpolation()`.

### Predictable lookups and return types

```python
from SecretColors import Palette

p = Palette()
p.color("red")                  # exactly one color
p.sample("red", 1)              # always a ColorList
p.color("red", fallback=False)  # restrict lookup to this palette
p.resolve("amber").source       # 'material'
```

`get()` and named helpers retain their historical scalar/list return behavior.
`strict_search=True` still means CSS/X11-only; it is not palette-only lookup.
Customized `Palette` instances are respected by selection and cache keys.
Counts reject booleans, non-integers and invalid ranges. Numeric color inputs
reject NaN and infinity. Empty color reports and empty colormaps raise errors.

---

## Upgrading from 1.x

Version 2.0 fixes many long standing bugs and modernises the library. Most
code keeps working. This page lists everything that may need a change.

## Requirements

- Python **3.11** or newer.
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
| `Palette.cycle()` started with red, blue, yellow, green ... (red/green clash for colorblind readers) | Yields colorblind-safe distinct colors, same order as `distinct_colors()` | Nothing, or pass `background=` for dark themes |
| Several colors were returned as `list` | Returned as `ColorList`, a `list` subclass which shows swatches in Jupyter | Nothing |

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
