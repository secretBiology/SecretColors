"""Numerical diagnostics for gradients; these are not accessibility guarantees."""

from dataclasses import dataclass
from itertools import combinations

from SecretColors._validation import count
from SecretColors.utils import (_check_space, _display_rgb, _mix, _ciede2000,
                                rgb_to_lab, contrast_ratio)


@dataclass(frozen=True)
class GradientReport:
    lightness: tuple[float, ...]
    monotonic_lightness: bool
    adjacent_delta_e: tuple[float, ...]
    min_grayscale_delta_l: float
    min_contrast: float | None
    clipped_positions: tuple[float, ...] | None = None


def check_gradient(colors, *, background="#ffffff") -> GradientReport:
    """Measure lightness progression, adjacent Delta E and grayscale separation.

    A diverging map normally has non-monotonic lightness. Small grayscale
    differences are expected for finely sampled gradients. Clipping cannot be
    inferred from finished colors; use :func:`check_interpolation` for that.
    """
    rgb = [_display_rgb(c, background) for c in colors]
    if len(rgb) < 2:
        raise ValueError("At least two colors are required")
    labs = [rgb_to_lab(*c) for c in rgb]
    lightness = tuple(lab[0] for lab in labs)
    steps = [b - a for a, b in zip(lightness, lightness[1:])]
    return GradientReport(
        lightness,
        all(d >= -1e-6 for d in steps) or all(d <= 1e-6 for d in steps),
        tuple(_ciede2000(a, b) for a, b in zip(labs, labs[1:])),
        min(abs(a - b) for a, b in combinations(lightness, 2)),
        min(contrast_ratio(c, background) for c in rgb) if background is not None else None)


def check_interpolation(color1, color2, *, n: int = 256,
                        space: str = "lab", background="#ffffff") -> GradientReport:
    """Sample an interpolation, reporting where it leaves the sRGB gamut.

    Inputs must be opaque. ``background`` is used only for contrast diagnostics.
    """
    n = count(n, minimum=2)
    space = _check_space(space)
    first, last = _display_rgb(color1), _display_rgb(color2)
    samples, clipped = [], []
    for i in range(n):
        t = i / (n - 1)
        try:
            _mix(first, last, t, space, clip=False)
        except ValueError:
            clipped.append(t)
        samples.append(_mix(first, last, t, space))
    report = check_gradient(samples, background=background)
    return GradientReport(report.lightness, report.monotonic_lightness,
                          report.adjacent_delta_e, report.min_grayscale_delta_l,
                          report.min_contrast, tuple(clipped))
