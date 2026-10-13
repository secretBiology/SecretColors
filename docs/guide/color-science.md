# Color science

SecretColors includes the conversions you need for perceptual work.
Everything lives in {mod}`SecretColors.utils`.

## CIE L\*a\*b\* and LCh

L\*a\*b\* is designed so that equal distances look equally different.
`L*` is lightness (0-100), `a*` goes from green to red and `b*` from blue to
yellow. LCh is the same space in polar form (lightness, chroma, hue).

```python
from SecretColors.utils import *

hex_to_lab("#ff0000")                   # (53.24, 80.09, 67.20)
lab_to_hex(53.24, 80.09, 67.20)         # '#ff0000'
lab_to_lch(*hex_to_lab("#ff0000"))      # (53.24, 104.55, 40.0)
lab_to_rgb(50, 200, 0)                  # out of gamut colors are clipped
lab_to_rgb(50, 200, 0, clip=False)      # ...or raise ValueError
```

## Delta E

{func}`~SecretColors.utils.delta_e` measures how different two colors look.
It uses CIEDE2000[^sharma] by default.

```python
delta_e("#fa4d56", "#fa4d57")           # 0.27
delta_e("#fa4d56", "#4589ff")           # 44.47
delta_e((50, 2.5, 0), (73, 25, -18))    # L*a*b* tuples work too
delta_e("#000000", "#ffffff", method="cie76")
```

A rough guide to reading the result

| Delta E | Perception |
|---|---|
| < 1 | Not perceptible |
| 1 - 2 | Perceptible on close observation |
| 2 - 10 | Perceptible at a glance |
| 11 - 49 | Colors are more similar than opposite |
| 100 | Opposite colors |

## RGB colorspaces

{func}`~SecretColors.utils.rgb_to_xyz` and
{func}`~SecretColors.utils.xyz_to_rgb` support 16 RGB colorspaces. They
expect *linear* RGB, so convert gamma encoded sRGB first.

```python
rgb_spaces()["pro_photo"]               # ['D50']
xyz = rgb_to_xyz(*srgb_to_linear(1, 0, 0))          # sRGB red to XYZ
rgb_to_xyz(0.2, 0.5, 0.1, space="pro_photo")
xyz_to_rgb(*xyz, space="adobe")
```

| Colorspace | White references | Colorspace | White references |
|---|---|---|---|
| `srgb` | D65, D50 | `don4` | D50 |
| `adobe` | D65, D50 | `eci` | D50 |
| `apple` | D65, D50 | `ekta_space_ps5` | D50 |
| `best` | D50 | `ntsc` | C, D50 |
| `beta` | D50 | `pal_secam` | D65, D50 |
| `bruce` | D65, D50 | `pro_photo` | D50 |
| `cie` | E, D50 | `smptec` | D65, D50 |
| `color_match` | D50 | `wide_gamut` | D50 |

L\*a\*b\* conversions accept the white references A, B, C, D50, D55, D65,
D75, E, F2, F7 and F11.

## Other conversions

| From \ To | Functions |
|---|---|
| Hex | `hex_to_rgb`, `hex_to_hsl`, `hex_to_lab` |
| RGB (0-1) | `rgb_to_hex`, `rgb_to_hsl`, `rgb_to_hsv`, `rgb_to_hsb`, `rgb_to_cmy`, `rgb_to_rgb255`, `rgb_to_lab` |
| RGB (0-255) | `rgb255_to_rgb`, `rgb255_to_hex`, `rgb255_to_hsl`, `rgb255_to_hsv` |
| Others | `hsl_to_rgb`, `hsl_to_hex`, `hsv_to_rgb`, `cmy_to_rgb`, `cmy_to_cmyk`, `cmyk_to_cmy`, `lch_to_lab` |
| Helpers | `color_in_between`, `get_complementary`, `text_color`, `relative_luminance` |

[^sharma]: Sharma G., Wu W. and Dalal E. N., [The CIEDE2000 color-difference formula](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/), Color Research & Application, 2005.
