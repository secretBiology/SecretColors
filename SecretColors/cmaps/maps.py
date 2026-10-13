#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Library-agnostic colormap API

"""
Simple, library-agnostic access to all SecretColors colormaps.

Every colormap has a name (see :func:`available`). Same name can be used to
get plain hex colors (works with any plotting library) or a matplotlib
colormap.

.. code-block:: python

    from SecretColors import cmaps

    cmaps.colors("Spectral", n=5)        # ['#d7191c', '#fdae61', ...]
    cmaps.cmap("greens")                 # matplotlib LinearSegmentedColormap
    cmaps.cmap("tol_bright")             # matplotlib ListedColormap

    cmaps.register()                     # register all maps in matplotlib
    plt.imshow(data, cmap="sc.greens")   # use them by name

Colormap names come from following sources

* **standard** - ``greens``, ``reds``, ``oranges``, ``purples``, ``grays``,
  ``blues`` generated from a :class:`~SecretColors.Palette`. Any other color
  name known to the palette (e.g. ``teal``, ``magenta``) also works.
* **brewer** - ColorBrewer maps (e.g. ``Spectral``, ``RdBu``, ``Set1``)
* **tableau** - Tableau maps (e.g. ``Tableau``, ``OrangeBlue``)
* **colorblind** - Colorblind safe maps (e.g. ``cud``, ``tol_sunset``)
"""

import difflib
import warnings
from functools import lru_cache
from typing import List, Optional, Union

from SecretColors.data.cmaps.brewer import BREWER_DATA
from SecretColors.data.cmaps.colorblind import CB_DATA
from SecretColors.data.cmaps.tableau import TABLEAU_DATA
from SecretColors.data.constants import PALETTE_IBM
from SecretColors.models.objects import ColorString
from SecretColors.models.palette import Palette, _linspace
from SecretColors.utils import hex_to_rgb, rgb_to_hex

__all__ = ["available", "colors", "cmap", "register", "DEFAULT_PREFIX"]

DEFAULT_PREFIX = "sc"
DEFAULT_NO_OF_COLORS = 10

_STANDARD = {
    "greens": "green",
    "reds": "red",
    "oranges": "orange",
    "purples": "purple",
    "grays": "gray",
    "blues": "blue",
}
_STANDARD_ALIASES = {"greys": "grays"}
_SOURCES = {
    "brewer": BREWER_DATA,
    "tableau": TABLEAU_DATA,
    "colorblind": CB_DATA,
}
_SPECIAL = {name: (source, data)
            for source, maps in _SOURCES.items()
            for name, data in maps.items()}
_QUALITATIVE = {"qual", "regular"}
_INSTALL_HINT = ("Install it with: pip install 'SecretColors[matplotlib]' "
                 "or uv add 'SecretColors[matplotlib]'")


def available(source: str = None) -> List[str]:
    """
    Names of all available colormaps

    >>> available()              # All colormaps
    >>> available("brewer")      # Only ColorBrewer colormaps

    :param source: One of 'standard', 'brewer', 'tableau', 'colorblind'.
        If None, all names are returned.
    :return: List of colormap names
    """
    if source is None:
        return list(_STANDARD) + list(_SPECIAL)
    source = source.strip().lower()
    if source == "standard":
        return list(_STANDARD)
    if source not in _SOURCES:
        raise ValueError(f"Unknown source '{source}'. Available sources: "
                         f"{['standard', *_SOURCES]}")
    return list(_SOURCES[source])


def _resolve(name: str):
    if not isinstance(name, str):
        raise TypeError(f"Colormap name should be str, not {type(name)}")
    key = name.strip()
    if key in _SPECIAL:
        return "special", key
    lower = key.lower()
    lower = _STANDARD_ALIASES.get(lower, lower)
    if lower in _STANDARD:
        return "standard", lower
    return "color", lower


def _unknown(name: str, palette: Palette) -> ValueError:
    options = available() + list(palette.colors)
    close = difflib.get_close_matches(name, options, n=3)
    hint = f" Did you mean {close}?" if close else ""
    return ValueError(f"Unknown colormap '{name}'.{hint} Use "
                      f"SecretColors.cmaps.available() to see all names.")


@lru_cache(maxsize=None)
def _named_palette(name: str) -> Palette:
    return Palette(name)


def _get_palette(palette: Union[str, Palette]) -> Palette:
    if isinstance(palette, Palette):
        return palette
    if isinstance(palette, str):
        return _named_palette(palette.strip().lower())
    raise TypeError(f"'palette' should be palette name or Palette object, "
                    f"not {type(palette)}")


def _validate(n, start, end):
    if n is not None:
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"'n' should be int, not {type(n)}")
        if n < 1:
            raise ValueError("'n' should be at least 1")
    for label, value in (("start", start), ("end", end)):
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"'{label}' should be a number, not "
                            f"{type(value)}")
        if not 0 <= value <= 100:
            raise ValueError(f"'{label}' should be between 0 and 100")


def _sample(hex_colors: List[str], n: int, start: float, end: float):
    rgb = [hex_to_rgb(c)[:3] for c in hex_colors]
    if len(rgb) == 1:
        return [hex_colors[0]] * n
    segments = len(rgb) - 1
    positions = [start] if n == 1 else _linspace(start, end, n)
    result = []
    for t in positions:
        x = t * segments
        i = min(int(x), segments - 1)
        f = x - i
        mixed = (a + (b - a) * f for a, b in zip(rgb[i], rgb[i + 1]))
        result.append(rgb_to_hex(*(min(1.0, max(0.0, v)) for v in mixed)))
    return result


def _special_colors(name, data, n, start, end) -> List[str]:
    sizes = sorted(int(k) for k in data if k != "type")
    largest = data[str(sizes[-1])]
    if data.get("type") in _QUALITATIVE:
        if start is not None or end is not None:
            raise ValueError(f"'{name}' is a qualitative colormap. 'start' "
                             f"and 'end' are only supported for sequential "
                             f"and diverging colormaps.")
        if n is None:
            return list(largest)
        if str(n) in data:
            return list(data[str(n)])
        if n <= len(largest):
            return list(largest[:n])
        raise ValueError(f"'{name}' has only {len(largest)} colors. "
                         f"Requested {n}.")
    if start is None and end is None:
        if n is None:
            return list(largest)
        if str(n) in data:
            return list(data[str(n)])
    start = 0 if start is None else start
    end = 100 if end is None else end
    return _sample(largest, n or len(largest), start / 100, end / 100)


def _is_qualitative(kind: str, name: str) -> bool:
    return kind == "special" and _SPECIAL[name][1].get("type") in _QUALITATIVE


def _colors(name, palette, n, start, end):
    _validate(n, start, end)
    kind, key = _resolve(name)
    pal = None if kind == "special" else _get_palette(palette)
    color = None
    if kind != "special":
        color = pal._find(_STANDARD.get(key, key))
    if color is None and kind == "color":
        matches = [k for k in _SPECIAL if k.lower() == key]
        if len(matches) != 1:
            raise _unknown(name, pal)
        kind, key = "special", matches[0]
    if kind == "special":
        result = _special_colors(key, _SPECIAL[key][1], n, start, end)
        return kind, key, result

    shades = color.get_all_shades()
    start = min(shades) if start is None else start
    end = max(shades) if end is None else end
    n = DEFAULT_NO_OF_COLORS if n is None else n
    return kind, key, [color.shade(s) for s in _linspace(start, end, n)]


def colors(name: str, *, palette: Union[str, Palette] = PALETTE_IBM,
           n: int = None, start: float = None, end: float = None,
           reverse: bool = False) -> List[ColorString]:
    """
    Colors of a colormap as hex strings. It does not need matplotlib and
    output can be used with any library.

    >>> colors("Spectral", n=5)                 # ColorBrewer Spectral
    >>> colors("greens", n=4, start=20, end=80)  # IBM greens, shade 20-80
    >>> colors("teal", palette="material")       # Any palette color
    >>> colors("tol_bright")                     # Colorblind safe colors

    Usage with other libraries

    .. code-block:: python

        px.imshow(data, color_continuous_scale=colors("RdBu"))  # plotly
        sns.color_palette(colors("Set2", n=4))                   # seaborn
        figure.line(..., color=colors("Tableau")[0])             # bokeh
        alt.Scale(range=colors("tol_sunset"))                    # altair

    :param name: Name of colormap (see :func:`available`) or any color
        name of the palette
    :param palette: Palette name or :class:`~SecretColors.Palette`. Only
        used for standard and color-name colormaps. (default: ibm)
    :param n: Number of colors. Default: 10 for standard colormaps and the
        largest available set for others. Diverging and sequential
        colormaps are interpolated when `n` is not available. Qualitative
        colormaps return first `n` colors.
    :param start: Start of colormap (0-100). For standard colormaps this is
        the starting shade.
    :param end: End of colormap (0-100). For standard colormaps this is the
        ending shade.
    :param reverse: If True, order of colors will be reversed
    :return: List of hex colors
    """
    _, _, result = _colors(name, palette, n, start, end)
    result = [ColorString(str(c)) for c in result]
    return list(reversed(result)) if reverse else result


def _matplotlib_colors():
    try:
        from matplotlib import colors as mpl_colors
    except ImportError as err:
        raise ImportError(f"matplotlib is required for colormap "
                          f"objects. {_INSTALL_HINT}") from err
    return mpl_colors


def _build(color_list, name: str, discrete: bool, mpl_colors=None):
    mpl_colors = mpl_colors or _matplotlib_colors()
    color_list = [str(c) for c in color_list]
    if discrete:
        return mpl_colors.ListedColormap(color_list, name=name)
    if len(color_list) < 2:
        raise ValueError("At least 2 colors are required for a continuous "
                         "colormap. Use discrete=True for a single color.")
    return mpl_colors.LinearSegmentedColormap.from_list(name, color_list)


def cmap(name: str, *, palette: Union[str, Palette] = PALETTE_IBM,
         n: int = None, start: float = None, end: float = None,
         discrete: Optional[bool] = None, reverse: bool = False):
    """
    Matplotlib colormap which can be directly passed to ``cmap`` argument

    >>> plt.imshow(data, cmap=cmap("greens"))
    >>> plt.imshow(data, cmap=cmap("RdBu", reverse=True))
    >>> plt.scatter(x, y, c=labels, cmap=cmap("Set2", n=4))
    >>> plt.imshow(data, cmap=cmap("blues", palette="material", start=20))

    :param name: Name of colormap (see :func:`available`) or any color
        name of the palette
    :param palette: Palette name or :class:`~SecretColors.Palette`. Only
        used for standard and color-name colormaps. (default: ibm)
    :param n: Number of colors (see :func:`colors`)
    :param start: Start of colormap (0-100)
    :param end: End of colormap (0-100)
    :param discrete: If True, :class:`matplotlib.colors.ListedColormap` is
        returned, else :class:`matplotlib.colors.LinearSegmentedColormap`.
        Default: True for qualitative colormaps, False otherwise.
    :param reverse: If True, colormap will be reversed
    :return: Matplotlib colormap
    """
    kind, key, result = _colors(name, palette, n, start, end)
    if discrete is None:
        discrete = _is_qualitative(kind, key)
    if reverse:
        result = list(reversed(result))
    full_name = f"{DEFAULT_PREFIX}.{key}" + ("_r" if reverse else "")
    return _build(result, full_name, discrete)


def register(prefix: str = DEFAULT_PREFIX, *,
             palette: Union[str, Palette] = PALETTE_IBM,
             force: bool = False) -> List[str]:
    """
    Registers all colormaps (and their reversed '_r' versions) in
    matplotlib, so that they can be used by name everywhere (matplotlib,
    pandas, seaborn etc.)

    >>> register()
    >>> plt.imshow(data, cmap="sc.greens")
    >>> plt.imshow(data, cmap="sc.Spectral_r")
    >>> sns.heatmap(data, cmap="sc.tol_sunset")

    Calling it again is safe. Already registered names are skipped unless
    `force` is True.

    :param prefix: Prefix added to every name (default: 'sc'). It avoids
        clashes with matplotlib's own colormaps (e.g. 'Spectral').
    :param palette: Palette used for standard colormaps (default: ibm)
    :param force: If True, existing colormaps with same names are replaced
    :return: Names of colormaps registered in this call
    """
    if not isinstance(prefix, str) or not prefix.strip():
        raise ValueError("'prefix' should be a non-empty string")
    prefix = prefix.strip()
    try:
        import matplotlib
    except ImportError as err:
        raise ImportError(f"matplotlib is required to register colormaps. "
                          f"{_INSTALL_HINT}") from err
    registry = getattr(matplotlib, "colormaps", None)
    if registry is None:
        raise ImportError("matplotlib>=3.5 is required to register "
                          "colormaps.")

    mpl_colors = _matplotlib_colors()
    registered = []
    for name in available():
        kind, key, result = _colors(name, palette, None, None, None)
        base = _build(result, f"{prefix}.{key}",
                      _is_qualitative(kind, key), mpl_colors)
        for colormap in (base, base.reversed()):
            if colormap.name in registry and not force:
                continue
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="Overwriting the "
                                                          "cmap")
                registry.register(colormap, name=colormap.name, force=force)
            registered.append(colormap.name)
    return registered
