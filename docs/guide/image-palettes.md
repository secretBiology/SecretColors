# Palette from an image

```{image} ../images/image-palette-light.png
:class: only-light
:alt: Palette extracted from an image
```
```{image} ../images/image-palette-dark.png
:class: only-dark
:alt: Palette extracted from an image
```

Pull the dominant colors out of any photo or artwork. Requires Pillow.

```bash
pip install "SecretColors[image]"
```

```python
from SecretColors.image import extract_palette

extract_palette("sunset.jpg")                         # 5 dominant colors
extract_palette("sunset.jpg", n=8, sort="lightness")  # light to dark
extract_palette(pil_image, n=3)                       # PIL Image works too
```

## How it works

1. The image is resized to fit in `max_size` pixels (128 by default).
2. Pixels are grouped and converted to the CIE L\*a\*b\* color space, where
   distances match how different colors *look*.
3. k-means clustering finds the `n` most representative colors.

Results are reproducible thanks to `seed`. Transparent pixels are ignored.

## Options

| Argument | Default | Meaning |
|---|---|---|
| `n` | `5` | Number of colors |
| `sort` | `"frequency"` | `"frequency"` (most common first), `"lightness"` (light to dark) or `"hue"` |
| `seed` | `0` | Random seed. `None` gives a different result every time |
| `max_size` | `128` | Resize limit. Larger is slower but more detailed |
| `min_alpha` | `128` | Pixels more transparent than this are ignored |

## Use the palette

```python
from SecretColors.cmaps import ColorMap

colors = extract_palette("sunset.jpg", n=6, sort="lightness")
plt.imshow(data, cmap=ColorMap().from_list(colors))     # colormap
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)  # color cycle
```
