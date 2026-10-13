#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Picking and checking colors for categorical data

"""
Pick colors which are easy to tell apart, and check your own colors.

.. code-block:: python

    from SecretColors import distinct_colors, check_colors

    distinct_colors(6)                          # 6 colorblind-safe colors
    check_colors(["#fa4d56", "#24a148"])        # red/green - fails
"""

from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Optional, Sequence, Tuple, Union

from SecretColors.models.objects import ColorList, ColorString
from SecretColors.models.palette import Palette
from SecretColors.utils import (_as_rgb, _ciede2000, contrast_ratio,
                                lab_to_lch, rgb_to_hex, rgb_to_lab,
                                simulate_green_blindness,
                                simulate_red_blindness)

__all__ = ["distinct_colors", "check_colors", "ColorReport"]

_VISIONS = ("normal", "protanopia", "deuteranopia")
# Delta E added to colors of a not yet used hue, so hues are varied unless a
# repeated hue is clearly more distinct
_NEW_HUE_BONUS = 5


def _labs(color) -> Tuple[tuple, tuple, tuple]:
    rgb = _as_rgb(color)
    return (rgb_to_lab(*rgb),
            rgb_to_lab(*simulate_red_blindness(*rgb)),
            rgb_to_lab(*simulate_green_blindness(*rgb)))


def _candidates(palette, shade_range, include_grays) -> List[tuple]:
    if isinstance(palette, (list, tuple)):
        hexes = dict.fromkeys(rgb_to_hex(*_as_rgb(c)) for c in palette)
        return [(c, c) for c in hexes]
    if isinstance(palette, str):
        palette = Palette(palette)
    elif not isinstance(palette, Palette):
        raise TypeError(f"'palette' should be a palette name, Palette or a "
                        f"list of colors, not {type(palette)}")
    low, high = sorted(shade_range)
    shades = [s for s in palette._value.get_shades() if low <= s <= high]
    found = {}
    for name, color in palette.colors.items():
        if name in ("white", "black"):
            continue
        for s in shades:
            c = str(color.shade(s))
            _, chroma, hue = lab_to_lch(*rgb_to_lab(*_as_rgb(c)))
            if chroma < 15 and not include_grays:
                continue
            found.setdefault(c, "gray" if chroma < 15 else int(hue // 30))
    return list(found.items())


def distinct_colors(n: int, *, palette: Union[str, Palette, Sequence] = "ibm",
                    colorblind_safe: bool = True,
                    background: Optional[str] = "#ffffff",
                    min_contrast: float = 3.0,
                    shade_range: Tuple[float, float] = (40, 70),
                    include_grays: bool = False) -> ColorList:
    """
    Picks `n` colors from a palette which are as easy as possible to tell
    apart, e.g. for categories in a plot.

    Colors are chosen one by one, each time taking the color which is
    perceptually farthest (CIEDE2000) from the ones already chosen. With
    `colorblind_safe` the distance is the smallest one among normal vision,
    protanopia and deuteranopia. Different hues are preferred over
    different shades of the same hue.

    The first `k` colors of ``distinct_colors(n)`` are the same as
    ``distinct_colors(k)``, so adding a category never repaints the others.

    >>> distinct_colors(5)                          # from IBM palette
    >>> distinct_colors(8, palette="material")
    >>> distinct_colors(4, background="#161616")    # for dark backgrounds
    >>> distinct_colors(3, palette=["#fa4d56", "#ff832b", "#24a148",
    ...                             "#0f62fe"])     # from your own colors

    :param n: Number of colors
    :param palette: Palette name, :class:`~SecretColors.Palette` or a list of
        colors to choose from (default: 'ibm')
    :param colorblind_safe: If True (default), colors are also kept apart
        for people with red or green colorblindness
    :param background: Background color. Colors with contrast lower than
        `min_contrast` against it are skipped. Use None to skip this check.
    :param min_contrast: Minimum WCAG contrast ratio against the background
        (default: 3.0, the WCAG minimum for graphics)
    :param shade_range: Range of shades to choose from (palettes only)
    :param include_grays: If True, grays can be chosen as well
    :return: List of colors, most distinct first
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"'n' should be int, not {type(n)}")
    if n < 1:
        raise ValueError("'n' should be at least 1")

    pool = _candidates(palette, shade_range, include_grays)
    if background is not None:
        pool = [(c, f) for c, f in pool if contrast_ratio(c, background) >=
                min_contrast]
    if len(pool) < n:
        raise ValueError(f"Only {len(pool)} colors are available with these "
                         f"settings. Try lowering 'min_contrast', widening "
                         f"'shade_range' or setting include_grays=True.")

    families = [f for _, f in pool]
    pool = [c for c, _ in pool]
    labs = [_labs(c) for c in pool]
    views = range(3) if colorblind_safe else range(1)

    def distance(i, j):
        return min(_ciede2000(labs[i][v], labs[j][v]) for v in views)

    chroma = [lab_to_lch(*lab[0])[1] for lab in labs]
    chosen = [max(range(len(pool)), key=lambda i: chroma[i])]
    nearest = [distance(i, chosen[0]) for i in range(len(pool))]
    while len(chosen) < n:
        used = {families[i] for i in chosen}
        best = max((i for i in range(len(pool)) if i not in chosen),
                   key=lambda i: nearest[i] + (_NEW_HUE_BONUS if families[i]
                                               not in used else 0))
        chosen.append(best)
        nearest = [min(d, distance(i, best)) for i, d in enumerate(nearest)]
    return ColorList(ColorString(pool[i]) for i in chosen)


@dataclass
class ColorReport:
    """
    Result of :func:`check_colors`
    """
    colors: List[str]
    min_delta_e: float
    closest_pair: Optional[Tuple[str, str]]
    min_delta_e_protanopia: float
    closest_pair_protanopia: Optional[Tuple[str, str]]
    min_delta_e_deuteranopia: float
    closest_pair_deuteranopia: Optional[Tuple[str, str]]
    low_contrast: List[str] = field(default_factory=list)
    threshold: float = 10.0

    @property
    def colorblind_safe(self) -> bool:
        """True if all pairs stay apart for colorblind readers"""
        return min(self.min_delta_e_protanopia,
                   self.min_delta_e_deuteranopia) >= self.threshold

    @property
    def ok(self) -> bool:
        """True if colors are distinct (also for colorblind readers) and
        have enough contrast with the background"""
        return (self.min_delta_e >= self.threshold and self.colorblind_safe
                and not self.low_contrast)

    def __str__(self) -> str:
        def line(label, value, pair):
            mark = "ok " if value >= self.threshold else "LOW"
            pair = f"  {pair[0]} vs {pair[1]}" if pair else ""
            return f"  [{mark}] {label:<14} min Delta E {value:6.1f}{pair}"

        lines = [f"ColorReport ({len(self.colors)} colors): "
                 f"{'OK' if self.ok else 'needs attention'}",
                 line("normal vision", self.min_delta_e, self.closest_pair),
                 line("protanopia", self.min_delta_e_protanopia,
                      self.closest_pair_protanopia),
                 line("deuteranopia", self.min_delta_e_deuteranopia,
                      self.closest_pair_deuteranopia)]
        if self.low_contrast:
            lines.append(f"  [LOW] low contrast with background: "
                         f"{', '.join(self.low_contrast)}")
        return "\n".join(lines)


def check_colors(colors: Sequence, *, background: Optional[str] = "#ffffff",
                 min_delta_e: float = 10.0,
                 min_contrast: float = 3.0) -> ColorReport:
    """
    Checks if colors are easy to tell apart, for everyone.

    It reports the closest pair of colors (CIEDE2000 Delta E) for normal
    vision, protanopia and deuteranopia, and colors with too little contrast
    against the background.

    >>> report = check_colors(["#fa4d56", "#24a148", "#0f62fe"])
    >>> report.ok                   # False - red and green look alike
    >>> print(report)               # readable summary

    :param colors: List of hex colors or RGB tuples (0-1)
    :param background: Background color for the contrast check. Use None to
        skip this check.
    :param min_delta_e: Smallest acceptable Delta E (default: 10, clearly
        different at a glance)
    :param min_contrast: Smallest acceptable WCAG contrast ratio against
        the background (default: 3.0)
    :return: :class:`ColorReport`
    """
    hexes = [rgb_to_hex(*_as_rgb(c)) for c in colors]
    labs = [_labs(c) for c in hexes]
    results = []
    for v in range(len(_VISIONS)):
        best, pair = float("inf"), None
        for i, j in combinations(range(len(hexes)), 2):
            d = _ciede2000(labs[i][v], labs[j][v])
            if d < best:
                best, pair = d, (hexes[i], hexes[j])
        results.extend([best, pair])
    low = [] if background is None else [
        c for c in hexes if contrast_ratio(c, background) < min_contrast]
    return ColorReport(hexes, *results, low_contrast=low,
                       threshold=min_delta_e)
