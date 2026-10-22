# Smooth gradients

```{image} ../images/gradients-light.png
:class: only-light
:alt: Gradients in RGB, Lab and LCh
```
```{image} ../images/gradients-dark.png
:class: only-dark
:alt: Gradients in RGB, Lab and LCh
```

Mixing two colors in RGB is simple, but the middle of the gradient often
looks dull and grayish (look at yellow to blue above). SecretColors can mix
colors in three spaces.

| Space | Result |
|---|---|
| `"rgb"` *(default)* | Simple linear mix of red, green and blue |
| `"lab"` | Perceptually even steps (CIE L\*a\*b\*) |
| `"lch"` | Goes around the color wheel and keeps colors vivid |

```python
from SecretColors.utils import mix, color_in_between

mix("#fa4d56", "#4589ff")                       # '#a06bab'
mix("#fa4d56", "#4589ff", space="lab")          # '#c670a9'
mix("#fa4d56", "#4589ff", space="lch")          # '#df57c0'
mix("#fa4d56", "#4589ff", ratio=0.25)           # closer to the first color

color_in_between("#f1c21b", "#0f62fe", 3)
# ['#b8aa54', '#80928c', '#487ac5']
color_in_between("#f1c21b", "#0f62fe", 3, space="lab")
# ['#daa76b', '#bc8d9f', '#8f76cf']
```

Every color object can be blended the same way.

```python
from SecretColors import Palette

p = Palette()
p.red().blend("#4589ff")                        # halfway, in RGB
p.red().blend("#4589ff", ratio=0.3, space="lch")
```

## Colormaps

`cmaps.colors()` and `cmaps.cmap()` accept `space` as well. It is used when
colors are interpolated, e.g. to get more colors than a colormap defines, and
`cmap()` resamples continuous colormaps smoothly in that space.

```python
from SecretColors import cmaps

cmaps.colors("Spectral", n=20, space="lab")
cmaps.cmap("RdBu", space="lab")
```

## Check visual properties

Perceptual interpolation is not a guarantee of uniform visual appearance.
Clipping to the sRGB gamut can change the intended trajectory.

```python
from SecretColors.diagnostics import check_gradient, check_interpolation

report = check_gradient(cmaps.colors("blues", n=20))
report.monotonic_lightness
report.adjacent_delta_e
report.min_grayscale_delta_l

report = check_interpolation("#f1c21b", "#0f62fe", space="lch")
report.clipped_positions
cmaps.info("RdBu").kind  # 'diverging'
```

Diverging maps normally change lightness direction. Small grayscale differences
are expected between densely sampled gradient colors; interpret the report in
terms of your chart's purpose rather than as a universal pass/fail score.
