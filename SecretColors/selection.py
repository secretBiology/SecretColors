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

import warnings
from threading import RLock
from dataclasses import dataclass, field

from SecretColors._color import ColorValue
from SecretColors._validation import count, number
from functools import lru_cache
from itertools import combinations
from typing import List, Optional, Sequence, Tuple, Union

from SecretColors.models.objects import ColorList, ColorString
from SecretColors.models.palette import Palette
from SecretColors.utils import (_display_rgb, _as_rgb, _ciede2000, contrast_ratio,
                                lab_to_lch, rgb_to_hex, rgb_to_lab,
                                simulate_green_blindness,
                                simulate_red_blindness)

__all__ = ["distinct_colors", "check_colors", "ColorReport", "DistinctnessWarning"]


class DistinctnessWarning(UserWarning):
    """Requested colors do not meet the configured separation threshold."""

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
    if isinstance(palette, Sequence) and not isinstance(palette, str):
        hexes = dict.fromkeys(_color_hex(c) for c in palette)
        return [(c, c) for c in hexes]
    if isinstance(palette, str):
        palette = Palette(palette)
    elif not isinstance(palette, Palette):
        raise TypeError(f"'palette' should be a palette name, Palette or a "
                        f"list of colors, not {type(palette)}")
    low, high = sorted(shade_range)
    found = {}
    for name, color in palette.colors.items():
        if name in ("white", "black"):
            continue
        for s in color.get_all_shades():
            if not low <= s <= high:
                continue
            c = str(color.shade(s))
            _, chroma, hue = lab_to_lch(*rgb_to_lab(*_as_rgb(c)))
            if chroma < 15 and not include_grays:
                continue
            found.setdefault(c, "gray" if chroma < 15 else int(hue // 30))
    return list(found.items())


def _color_hex(color):
    value = ColorValue.parse(color)
    return value.hex(alpha=value.rgba[3] < 1)


@lru_cache(maxsize=64)
def _builtin_candidates(name, shade_range, include_grays):
    return tuple(_candidates(name, shade_range, include_grays))


class _SelectionState:
    """Extend a stable greedy ordering only as far as the caller requests."""

    def __init__(self, pool, colorblind_safe):
        self.pool = pool
        self.labs = [_labs(display) for _, _, display in pool]
        self.views = range(3) if colorblind_safe else range(1)
        self.chosen = []
        self.nearest = [float("inf")] * len(pool)
        self.processed = 0
        self.remaining = set(range(len(pool)))
        self.lock = RLock()

    def distance(self, i, j):
        return min(_ciede2000(self.labs[i][v], self.labs[j][v]) for v in self.views)

    def take(self, n):
        with self.lock:
            if self.pool and not self.chosen:
                first = max(range(len(self.pool)),
                            key=lambda i: lab_to_lch(*self.labs[i][0])[1])
                self.chosen.append(first)
                self.remaining.remove(first)
            while self.remaining and len(self.chosen) < n:
                for previous in self.chosen[self.processed:]:
                    self.nearest = [min(d, self.distance(i, previous))
                                    for i, d in enumerate(self.nearest)]
                self.processed = len(self.chosen)
                used = {self.pool[i][1] for i in self.chosen}
                best = max(sorted(self.remaining),
                           key=lambda i: self.nearest[i] + (
                               _NEW_HUE_BONUS if self.pool[i][1] not in used else 0))
                self.chosen.append(best)
                self.remaining.remove(best)
            return tuple(self.pool[i][0] for i in self.chosen[:n])


@lru_cache(maxsize=64)
def _order_state(pool, colorblind_safe):
    return _SelectionState(pool, colorblind_safe)


def _distinct_order(palette, colorblind_safe: bool,
                    background: Optional[str], min_contrast: float,
                    shade_range: Tuple[float, float], include_grays: bool,
                    n: Optional[int] = None) -> Tuple[str, ...]:
    number(min_contrast, "min_contrast", minimum=1, maximum=21)
    if len(shade_range) != 2:
        raise ValueError("'shade_range' requires two values")
    shade_range = tuple(number(s, "shade", minimum=0, maximum=100) for s in shade_range)
    if background is not None:
        _display_rgb(background)
    candidates = (_builtin_candidates(palette.strip().lower(), shade_range, include_grays)
                  if isinstance(palette, str) else _candidates(palette, shade_range, include_grays))
    pool = []
    for color, family in candidates:
        display = _display_rgb(color, background)
        if background is None or contrast_ratio(color, background) >= min_contrast:
            pool.append((color, family, display))
    state = _order_state(tuple(pool), colorblind_safe)
    return state.take(len(pool) if n is None else n)


def distinct_colors(n: int, *, palette: Union[str, Palette, Sequence] = "ibm",
                    colorblind_safe: bool = True,
                    background: Optional[str] = "#ffffff",
                    min_contrast: float = 3.0,
                    shade_range: Tuple[float, float] = (40, 70),
                    include_grays: bool = False, min_delta_e: float = 10.0,
                    on_failure: str = "warn") -> ColorList:
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
    :meth:`Palette.cycle() <SecretColors.Palette.cycle>` yields the same
    colors one by one, without a limit.

    >>> distinct_colors(5)                          # from IBM palette
    >>> distinct_colors(8, palette="material")
    >>> distinct_colors(4, background="#161616")    # for dark backgrounds
    >>> distinct_colors(3, palette=["#fa4d56", "#ff832b", "#24a148",
    ...                             "#0f62fe"])     # from your own colors

    :param n: Number of colors
    :param palette: Palette name, :class:`~SecretColors.Palette` or a list of
        colors to choose from (default: 'ibm')
    :param colorblind_safe: Include simulated protanopia/deuteranopia in
        distance optimization and threshold checks. This is not a guarantee
        for all forms or severities of color vision deficiency.
    :param background: Background color. Colors with contrast lower than
        `min_contrast` against it are skipped. Use None to skip this check.
    :param min_contrast: Minimum WCAG contrast ratio against the background
        (default: 3.0, the WCAG minimum for graphics)
    :param shade_range: Range of shades to choose from (palettes only)
    :param include_grays: If True, grays can be chosen as well
    :param min_delta_e: Required separation under the selected vision models.
    :param on_failure: 'warn' (default), 'raise' or 'ignore' when the selected
        prefix misses the threshold. Its ordering is never silently changed.
    :return: List of colors, most distinct first
    """
    n = count(n)
    min_delta_e = number(min_delta_e, "min_delta_e", minimum=0)
    if on_failure not in ("warn", "raise", "ignore"):
        raise ValueError("'on_failure' should be 'warn', 'raise' or 'ignore'")
    order = _distinct_order(palette, bool(colorblind_safe), background,
                            min_contrast, tuple(shade_range), bool(include_grays), n)
    if len(order) < n:
        raise ValueError(f"Only {len(order)} colors are available with these settings. "
                         "Try lowering 'min_contrast', widening 'shade_range' or "
                         "setting include_grays=True.")
    result = ColorList(ColorString(c) for c in order)
    if on_failure != "ignore":
        report = check_colors(result, background=background,
                              min_delta_e=min_delta_e, min_contrast=min_contrast)
        separated = report.min_delta_e >= min_delta_e
        if colorblind_safe:
            separated = separated and report.colorblind_safe
        if not separated:
            message = (f"Requested {n} colors do not meet min_delta_e={min_delta_e:g} "
                       "under the selected vision models. Use fewer colors, "
                       "a different palette, or inspect check_colors().")
            if on_failure == "raise":
                raise ValueError(message)
            warnings.warn(message, DistinctnessWarning, stacklevel=2)
    return result


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
        """True if all pairs meet the threshold for simulated protanopia/deuteranopia"""
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
    Checks separation for normal vision, protanopia and deuteranopia.

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
    min_delta_e = number(min_delta_e, "min_delta_e", minimum=0)
    min_contrast = number(min_contrast, "min_contrast", minimum=1, maximum=21)
    if background is not None:
        _display_rgb(background)
    original = list(colors)
    hexes = [_color_hex(c) for c in original]
    if not hexes:
        raise ValueError("At least one color is required")
    labs = [_labs(_display_rgb(c, background)) for c in original]
    results = []
    for v in range(len(_VISIONS)):
        best, pair = float("inf"), None
        for i, j in combinations(range(len(hexes)), 2):
            d = _ciede2000(labs[i][v], labs[j][v])
            if d < best:
                best, pair = d, (hexes[i], hexes[j])
        results.extend([best, pair])
    low = [] if background is None else [
        label for label, c in zip(hexes, original)
        if contrast_ratio(c, background) < min_contrast]
    return ColorReport(hexes, *results, low_contrast=low,
                       threshold=min_delta_e)
