# Choosing distinguishable colors

```{image} ../images/distinct-light.png
:class: only-light
:alt: Distinct colors under colorblindness
```
```{image} ../images/distinct-dark.png
:class: only-dark
:alt: Distinct colors under colorblindness
```

Picking colors for categories by hand is surprisingly hard. Colors that look
different to you might be indistinguishable for colorblind readers, too
light on a white page, or invisible on a dark slide.

## Pick distinct colors

{func}`~SecretColors.distinct_colors` picks colors from a palette which are
as far apart as possible, for normal vision **and** red or green
colorblindness, and have enough contrast with the background.

```python
from SecretColors import distinct_colors

distinct_colors(5)
# ['#8a3ffc', '#b3901f', '#9f1853', '#009d9a', '#993a1d']
distinct_colors(5, background="#161616")
# ['#8a3ffc', '#c6a21a', '#ff7eb6', '#d12771', '#007d79']
distinct_colors(8, palette="material")
distinct_colors(3, palette=["#fa4d56", "#ff832b", "#24a148", "#0f62fe"])
```

Use them as the default colors of your plots.

```python
import matplotlib.pyplot as plt
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=distinct_colors(6))
```

:::{tip}
The first `k` colors of `distinct_colors(n)` are always the same as
`distinct_colors(k)`. Adding a new category never repaints the existing ones.
`Palette().cycle()` gives the same colors one by one, without a limit.
:::

| Argument | Default | Meaning |
|---|---|---|
| `palette` | `"ibm"` | Palette name, `Palette` or your own list of colors |
| `colorblind_safe` | `True` | Include simulated protanopia and deuteranopia |
| `min_delta_e` | `10` | Minimum requested separation |
| `on_failure` | `"warn"` | `"warn"`, `"raise"`, or `"ignore"` when separation falls short |
| `background` | `"#ffffff"` | Skip colors with too little contrast. `None` disables it |
| `min_contrast` | `3.0` | Minimum WCAG contrast with the background |
| `shade_range` | `(40, 70)` | Shades to choose from |
| `include_grays` | `False` | Allow grays |

The selected prefix is preserved even when separation falls short. The default
emits `DistinctnessWarning`; use `on_failure="raise"` to reject that result.
These checks cover normal vision, protanopia and deuteranopia, not every form
or severity of color vision deficiency. Alpha is composited onto the opaque
background before checking contrast and separation.

### How it works

Colors are chosen one at a time. Each time, the color farthest from the ones
already chosen is taken, measured with CIEDE2000 Delta E. With
`colorblind_safe`, the distance is the smallest one among normal vision,
protanopia and deuteranopia. New hues are preferred over a second shade of a
hue which is already used.

## Check your colors

{func}`~SecretColors.check_colors` reports separation under normal vision, protanopia and deuteranopia.

```python
from SecretColors import check_colors

report = check_colors(["#fa4d56", "#24a148", "#0f62fe"])
print(report)
# ColorReport (3 colors): needs attention
#   [ok ] normal vision  min Delta E   44.4  #fa4d56 vs #0f62fe
#   [ok ] protanopia     min Delta E   17.9  #fa4d56 vs #24a148
#   [LOW] deuteranopia   min Delta E    5.5  #fa4d56 vs #24a148

report.ok                   # False
report.colorblind_safe      # False
report.closest_pair_deuteranopia    # ('#fa4d56', '#24a148')
report.low_contrast         # colors with too little contrast
```

By default a pair needs a Delta E of at least 10 (`min_delta_e`), which is
clearly different at a glance.

## Contrast and readability

The [WCAG](https://www.w3.org/TR/WCAG21/#contrast-minimum) guidelines define
how much contrast text needs to be readable.

```python
from SecretColors.utils import contrast_ratio, is_readable

contrast_ratio("#0f62fe", "#ffffff")                    # 5.0
is_readable("#8d8d8d", "#ffffff")                       # False
is_readable("#8d8d8d", "#ffffff", large_text=True)      # True
is_readable("#0f62fe", "#ffffff", level="AAA")          # False
```

| Level | Normal text | Large text |
|---|---|---|
| AA | 4.5 | 3.0 |
| AAA | 7.0 | 4.5 |

A ratio of 3.0 is also the WCAG minimum for graphics such as plot lines and
markers, which is why `distinct_colors` uses it by default.

See also {doc}`colorblind` for ready made colorblind-safe schemes and
colorblindness simulation.
