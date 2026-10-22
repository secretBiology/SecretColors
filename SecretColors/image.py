#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Color palette extraction from images

"""
Generate a color palette from an image.

.. code-block:: python

    from SecretColors.image import extract_palette

    extract_palette("sunset.jpg")              # 5 dominant colors
    extract_palette("sunset.jpg", n=8, sort="lightness")

Requires `Pillow <https://python-pillow.org>`_ ::

    pip install "SecretColors[image]"
"""

from SecretColors._validation import count

import os
import random
from collections import Counter
from typing import List, Union

from SecretColors.models.objects import ColorList, ColorString
from SecretColors.utils import lab_to_hex, lab_to_lch, rgb_to_lab

__all__ = ["extract_palette"]

_SORTS = ("frequency", "lightness", "hue")
_INSTALL_HINT = ("Install it with: pip install 'SecretColors[image]' or "
                 "uv add 'SecretColors[image]'")


def _load(image, max_size: int):
    try:
        from PIL import Image
    except ImportError as err:
        raise ImportError(f"Pillow is required to read images. "
                          f"{_INSTALL_HINT}") from err
    if isinstance(image, Image.Image):
        img = image.copy()
    elif isinstance(image, (str, os.PathLike)) or hasattr(image, "read"):
        with Image.open(image) as opened:
            img = opened.copy()
    else:
        raise TypeError(f"'image' should be a file path, file object or "
                        f"PIL Image, not {type(image)}")
    img = img.convert("RGBA")
    img.thumbnail((max_size, max_size))
    return img


def _buckets(img, min_alpha: int):
    data = img.get_flattened_data() if hasattr(
        img, "get_flattened_data") else img.getdata()
    sums, counts = {}, Counter()
    for r, g, b, a in data:
        if a < min_alpha:
            continue
        key = (r >> 3, g >> 3, b >> 3)
        s = sums.setdefault(key, [0, 0, 0])
        s[0] += r
        s[1] += g
        s[2] += b
        counts[key] += 1
    points, weights = [], []
    for key, count in counts.items():
        r, g, b = (v / count / 255 for v in sums[key])
        points.append(rgb_to_lab(r, g, b))
        weights.append(count)
    return points, weights


def _distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def _kmeans(points, weights, k, rng, iterations=40):
    centers = [points[rng.choices(range(len(points)), weights)[0]]]
    while len(centers) < k:
        d = [w * min(_distance(p, c) for c in centers)
             for p, w in zip(points, weights)]
        if sum(d) == 0:
            break
        centers.append(points[rng.choices(range(len(points)), d)[0]])

    labels = None
    for _ in range(iterations):
        new = [min(range(len(centers)),
                   key=lambda i: _distance(p, centers[i])) for p in points]
        if new == labels:
            break
        labels = new
        totals = [[0.0, 0.0, 0.0, 0.0] for _ in centers]
        for p, w, i in zip(points, weights, labels):
            t = totals[i]
            t[0] += p[0] * w
            t[1] += p[1] * w
            t[2] += p[2] * w
            t[3] += w
        centers = [(t[0] / t[3], t[1] / t[3], t[2] / t[3]) if t[3] else c
                   for t, c in zip(totals, centers)]

    sizes = Counter()
    for w, i in zip(weights, labels):
        sizes[i] += w
    return [(centers[i], sizes[i]) for i in range(len(centers)) if sizes[i]]


def extract_palette(image, n: int = 5, *, sort: str = "frequency",
                    seed: Union[int, None] = 0, max_size: int = 128,
                    min_alpha: int = 128) -> List[ColorString]:
    """
    Extracts dominant colors from an image. Colors are clustered in the
    perceptually uniform CIE-L*a*b* space (k-means), so the palette matches
    what we see rather than raw pixel values.

    >>> extract_palette("photo.jpg")                    # 5 dominant colors
    >>> extract_palette("photo.png", n=8, sort="hue")   # 8 colors, by hue
    >>> extract_palette(pil_image, n=3)                 # PIL Image works too

    Use the result like any other list of colors

    .. code-block:: python

        colors = extract_palette("photo.jpg", n=6, sort="lightness")
        ColorMap().from_list(colors)                    # matplotlib colormap

    :param image: File path, file object or PIL Image
    :param n: Number of colors (default: 5). Fewer colors are returned if
        image does not have enough distinct colors.
    :param sort: 'frequency' (most common first, default), 'lightness'
        (light to dark) or 'hue'
    :param seed: Seed for the random initialisation, so results are
        reproducible. Use None for a different result every time.
    :param max_size: Image is resized (keeping aspect ratio) to fit in this
        many pixels before clustering. Larger is slower but more detailed.
    :param min_alpha: Pixels with alpha below this (0-255) are ignored
    :return: List of hex colors
    """
    n = count(n)
    min_alpha = count(min_alpha, "min_alpha", minimum=0)
    if min_alpha > 255:
        raise ValueError("min_alpha should be at most 255")
    sort = sort.strip().lower()
    if sort not in _SORTS:
        raise ValueError(f"'sort' should be one of {_SORTS}")
    if isinstance(max_size, bool) or not isinstance(max_size, int) or \
            max_size < 1:
        raise ValueError("'max_size' should be a positive int")

    points, weights = _buckets(_load(image, max_size), min_alpha)
    if not points:
        raise ValueError("Image does not have any visible pixels")

    clusters = _kmeans(points, weights, min(n, len(points)),
                       random.Random(seed))
    if sort == "frequency":
        clusters.sort(key=lambda c: -c[1])
    elif sort == "lightness":
        clusters.sort(key=lambda c: -c[0][0])
    else:
        clusters.sort(key=lambda c: (lab_to_lch(*c[0])[1] < 5,
                                     lab_to_lch(*c[0])[2]))

    result, seen = ColorList(), set()
    for center, _ in clusters:
        color = lab_to_hex(*center)
        if color not in seen:
            seen.add(color)
            result.append(ColorString(color))
    return result
