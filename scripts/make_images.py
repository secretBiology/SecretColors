#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Generates images used in README.md and documentation
#
#  uv run python scripts/make_images.py

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from SecretColors import ColorWheel, Palette, cmaps
from SecretColors.utils import (hex_to_hsl, hex_to_rgb, rgb_to_hex,
                                simulate_green_blindness,
                                simulate_red_blindness)

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "images"
STATIC = ROOT / "docs" / "_static"

THEMES = {
    "light": dict(bg="#ffffff", ink="#161616", muted="#6f6f6f",
                  grid="#e8e8e8"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", muted="#8b949e",
                 grid="#21262d"),
}

P = Palette()
# Series orders below pass colorblind, lightness and contrast checks on
# their respective surfaces
SERIES = {
    "light": [P.blue(shade=60), P.red(), P.teal(), P.purple(shade=60),
              P.orange()],
    "dark": [P.blue(), P.red(), P.teal(), P.purple(), P.orange(shade=60)],
}

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.linewidth": 0.8,
    "svg.fonttype": "none",
})
MONO = ["Menlo", "DejaVu Sans Mono"]


def _save(fig, name, theme=None, transparent=False):
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = f"-{theme}" if theme else ""
    path = OUT / f"{name}{suffix}.png"
    face = "none" if transparent else THEMES[theme]["bg"]
    fig.savefig(path, dpi=200, facecolor=face, transparent=transparent,
                bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"saved {path.relative_to(OUT.parent.parent)}")


def _chip(ax, x, y, w, h, color, radius=0.12, edge=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor=edge or "none", linewidth=0.6))


def _canvas(width, height, theme=None):
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    if theme:
        fig.patch.set_facecolor(THEMES[theme]["bg"])
    return fig, ax


def _hue_order(names, palette):
    def key(name):
        h, s, _ = hex_to_hsl(palette.get(name))
        return (s < 0.15, (h + 0.04) % 1)

    return sorted((n for n in names if n not in ("white", "black")), key=key)


def banner():
    p = Palette("material")
    hues = _hue_order(p.colors, p)
    hues = [h for h in hues if "gray" not in h and h != "brown"]
    shades = [15, 30, 45, 60, 75]
    fig, ax = _canvas(12, 12 * len(shades) / len(hues) * 0.92)
    for i, name in enumerate(hues):
        for j, shade in enumerate(shades):
            _chip(ax, i, len(shades) - j - 1, 0.86, 0.86,
                  p.get(name, shade=shade), radius=0.16)
    ax.set_xlim(-0.05, len(hues) - 0.1)
    ax.set_ylim(-0.05, len(shades) - 0.1)
    _save(fig, "banner", transparent=True)


def _mosaic(ax, size, gap):
    p = Palette()
    grid = [["red", "magenta", "purple"], ["orange", "cyan", "blue"],
            ["yellow", "green", "teal"]][:size]
    for r, row in enumerate(grid):
        for c, name in enumerate(row[:size]):
            _chip(ax, c, size - r - 1, 1 - gap, 1 - gap, p.get(name),
                  radius=0.22)


def logo():
    for theme, t in THEMES.items():
        fig, ax = _canvas(3.4, 0.62)
        fig.patch.set_alpha(0)
        _mosaic(ax, 3, 0.16)
        ax.text(3.35, 1.42, "SecretColors", color=t["ink"], fontsize=21,
                fontweight="bold", va="center")
        ax.set_xlim(0, 15.5)
        ax.set_ylim(-0.05, 2.95)
        STATIC.mkdir(parents=True, exist_ok=True)
        fig.savefig(STATIC / f"logo-{theme}.png", dpi=200, transparent=True)
        plt.close(fig)
    fig, ax = _canvas(0.64, 0.64)
    fig.patch.set_alpha(0)
    _mosaic(ax, 3, 0.14)
    ax.set_xlim(0, 2.9)
    ax.set_ylim(0, 2.9)
    fig.savefig(STATIC / "favicon.png", dpi=100, transparent=True)
    plt.close(fig)
    print("saved docs/_static/logo-*.png, favicon.png")


def palettes(theme):
    t = THEMES[theme]
    names = ["ibm", "material", "material-accent", "spectrum", "clarity",
             "latitude", "brewer", "tableau"]
    rows = []
    for name in names:
        p = Palette(name)
        rows.append((name, [p.get(c) for c in _hue_order(p.colors, p)]))
    width = max(len(c) for _, c in rows)
    fig, ax = _canvas(10, 0.5 * len(rows), theme)
    for r, (name, colors) in enumerate(rows):
        y = len(rows) - r - 1
        ax.text(-0.4, y + 0.42, f'Palette("{name}")', ha="right",
                va="center", color=t["ink"], fontsize=9, family=MONO)
        for i, c in enumerate(colors):
            _chip(ax, i, y, 0.82, 0.82, c, radius=0.14)
    ax.set_xlim(-6.2, width)
    ax.set_ylim(-0.1, len(rows))
    _save(fig, "palettes", theme)


def shades(theme):
    t = THEMES[theme]
    p = Palette()
    names = ["red", "magenta", "purple", "blue", "cyan", "teal", "green",
             "yellow"]
    fig, ax = _canvas(10, 0.42 * len(names) + 0.5, theme)
    steps = np.linspace(0, 100, 201)
    for r, name in enumerate(names):
        y = len(names) - r - 1
        strip = np.array([[hex_to_rgb(p.get(name, shade=s))[:3]
                           for s in steps]])
        ax.imshow(strip, extent=(0, 100, y + 0.12, y + 0.82),
                  aspect="auto", interpolation="bicubic", zorder=1)
        ax.text(-2, y + 0.47, f"p.{name}()", ha="right", va="center",
                color=t["ink"], fontsize=9, family=MONO)
    for s in (0, 25, 50, 75, 100):
        ax.text(s, -0.25, f"shade={s}", ha="center", va="top",
                color=t["muted"], fontsize=7.5, family=MONO)
    ax.set_xlim(-17, 101)
    ax.set_ylim(-0.6, len(names))
    _save(fig, "shades", theme)


def colormaps(theme):
    t = THEMES[theme]
    groups = [
        ("Sequential", ["greens", "blues", "purples", "YlGnBu",
                        "tol_yl_or_br", "AquaBrown"]),
        ("Diverging", ["Spectral", "RdBu", "tol_sunset", "PRGn",
                       "OrangeBlue", "RedWhiteGreen"]),
        ("Qualitative & colorblind safe", ["cud", "tol_bright",
                                           "tol_vibrant", "Set2",
                                           "Tableau", "Paired"]),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    fig.patch.set_facecolor(t["bg"])
    fig.subplots_adjust(left=0.01, right=0.99, wspace=0.12, top=0.86,
                        bottom=0.02)
    for ax, (title, names) in zip(axes, groups):
        ax.set_axis_off()
        ax.set_title(title, loc="left", color=t["ink"], fontsize=10.5,
                     fontweight="bold", pad=8)
        for r, name in enumerate(names):
            y = len(names) - r - 1
            ax.text(0, y + 0.66, f'"sc.{name}"', color=t["muted"],
                    fontsize=7.5, family=MONO, va="bottom")
            colors = cmaps.colors(name)
            if title.startswith("Qualitative"):
                n = len(colors)
                for i, c in enumerate(colors):
                    _chip(ax, i / n, y + 0.06, 1 / n - 0.008, 0.52, c,
                          radius=0)
            else:
                cm = cmaps.cmap(name)
                ax.imshow(np.linspace(0, 1, 256)[None, :], cmap=cm,
                          extent=(0, 1, y + 0.06, y + 0.58), aspect="auto")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, len(names) - 0.15)
    _save(fig, "colormaps", theme)


def _style(ax, t, title):
    ax.set_facecolor(t["bg"])
    ax.set_title(title, loc="left", color=t["ink"], fontsize=10,
                 fontweight="bold", pad=8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["grid"])
    ax.tick_params(colors=t["muted"], labelsize=7.5, length=0)
    ax.grid(color=t["grid"], linewidth=0.6)
    ax.set_axisbelow(True)


def _legend(ax, t, **kwargs):
    leg = ax.legend(frameon=False, fontsize=7.5, labelcolor=t["ink"],
                    handlelength=1.2, **kwargs)
    return leg


def examples(theme):
    t = THEMES[theme]
    series = SERIES[theme]
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.6))
    fig.patch.set_facecolor(t["bg"])
    fig.subplots_adjust(hspace=0.42, wspace=0.22, left=0.06, right=0.98,
                        top=0.93, bottom=0.07)

    ax = axes[0, 0]
    _style(ax, t, "Line chart")
    x = np.arange(36)
    for i, color in enumerate(series[:4]):
        y = np.cumsum(rng.normal(0.4 + 0.15 * i, 1.2, len(x))) + 10 * i
        ax.plot(x, y, color=color, linewidth=2, solid_capstyle="round",
                label=f"Group {'ABCD'[i]}")
        ax.scatter(x[-1:], y[-1:], s=28, color=color, edgecolor=t["bg"],
                   linewidth=1.5, zorder=3)
    _legend(ax, t, loc="upper left", ncols=2)

    ax = axes[0, 1]
    _style(ax, t, "Heatmap")
    ax.grid(False)
    gx, gy = np.meshgrid(np.linspace(-3, 3, 480), np.linspace(-2, 2, 320))
    z = np.sin(gx * 1.3) * np.cos(gy * 1.6) + 0.25 * gx
    image = ax.imshow(z, cmap=cmaps.cmap("RdBu", reverse=True),
                      vmin=-1.6, vmax=1.6, aspect="auto",
                      extent=(-3, 3, -2, 2))
    cbar = fig.colorbar(image, ax=ax, fraction=0.04, pad=0.02)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=t["muted"], labelsize=7, length=0)

    ax = axes[1, 0]
    _style(ax, t, "Histogram")
    p = Palette()
    a = rng.normal(0, 1, 4000)
    b = rng.normal(1.6, 0.8, 4000)
    bins = np.linspace(-4, 5, 46)
    ax.hist(a, bins=bins, color=p.magenta(), alpha=0.75, label="p.magenta()",
            edgecolor=t["bg"], linewidth=0.6)
    ax.hist(b, bins=bins, color=p.cyan(), alpha=0.75, label="p.cyan()",
            edgecolor=t["bg"], linewidth=0.6)
    _legend(ax, t, loc="upper left", prop={"family": MONO, "size": 7.5})

    ax = axes[1, 1]
    _style(ax, t, "Scatter")
    centers = [(-3, 2), (-1.5, -3), (2.5, 3), (3.5, -1.5)]
    for i, (color, center) in enumerate(zip(series, centers)):
        pts = rng.normal(center, 0.9, (70, 2))
        ax.scatter(pts[:, 0], pts[:, 1], s=26, color=color,
                   edgecolor=t["bg"], linewidth=1.2, alpha=0.95,
                   label=f"Cluster {i + 1}")
    _legend(ax, t, loc="best", ncols=2, markerscale=1.1)
    _save(fig, "examples", theme)


def harmonies(theme):
    t = THEMES[theme]
    base = Palette("material").indigo()
    rows = [
        ("complementary()", ColorWheel(base).complementary()),
        ("triadic()", ColorWheel(base).triadic()),
        ("tetradic()", ColorWheel(base).tetradic()),
        ("analogous()", ColorWheel(base).analogous()),
    ]
    lighter = []
    for i in range(5):
        cw = ColorWheel(base)
        cw.make_lighter(i * 18)
        lighter.append(cw.color)
    rows.append(("make_lighter()", lighter))
    fig, ax = _canvas(9, 0.62 * len(rows), theme)
    for r, (label, colors) in enumerate(rows):
        y = len(rows) - r - 1
        ax.text(-0.3, y + 0.42, label, ha="right", va="center",
                color=t["ink"], fontsize=9, family=MONO)
        for i, c in enumerate(colors):
            _chip(ax, i * 1.5, y + 0.08, 1.35, 0.7, c, radius=0.12)
            ax.text(i * 1.5 + 0.675, y + 0.43, c, ha="center", va="center",
                    color=ColorWheel(c).text_color(), fontsize=7,
                    family=MONO)
    ax.set_xlim(-2.4, 7.5)
    ax.set_ylim(0, len(rows))
    _save(fig, "harmonies", theme)


def _scene():
    from PIL import Image, ImageDraw, ImageFilter

    width, height = 900, 560
    sky = [Palette("material").get(c, shade=s) for c, s in
           (("deep-purple", 70), ("pink", 40), ("deep-orange", 30),
            ("amber", 20))]
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    stops = [hex_to_rgb(c)[:3] for c in sky]
    for y in range(height):
        t = y / (height * 0.62) * (len(stops) - 1)
        i = min(int(t), len(stops) - 2)
        f = min(1.0, t - i)
        rgb = [a + (b - a) * f for a, b in zip(stops[i], stops[i + 1])]
        draw.line([(0, y), (width, y)],
                  fill=tuple(int(v * 255) for v in rgb))
    draw.ellipse((560, 230, 720, 390), fill=Palette("material").get(
        "amber", shade=10))
    hills = [("deep-purple", 80, 0.62, 0.0), ("indigo", 90, 0.72, 1.7),
             ("blue-gray", 90, 0.84, 3.1)]
    for name, shade, base, phase in hills:
        color = Palette("material").get(name, shade=shade)
        pts = [(x, height * base + 28 * np.sin(x / 95 + phase)
                + 14 * np.sin(x / 37 + phase * 2)) for x in range(0, width + 1,
                                                                 6)]
        draw.polygon(pts + [(width, height), (0, height)], fill=color)
    return img.filter(ImageFilter.GaussianBlur(1.2))


def image_palette(theme):
    from SecretColors.image import extract_palette

    t = THEMES[theme]
    scene = _scene()
    colors = extract_palette(scene, n=6, sort="lightness")
    fig = plt.figure(figsize=(10, 3.3))
    fig.patch.set_facecolor(t["bg"])
    ax = fig.add_axes([0.0, 0.0, 0.5, 1.0])
    ax.imshow(np.asarray(scene))
    ax.set_axis_off()
    ax = fig.add_axes([0.53, 0.0, 0.47, 1.0])
    ax.set_axis_off()
    ax.text(0, 5.6, "extract_palette(image, n=6)", color=t["ink"],
            fontsize=9.5, family=MONO, va="center")
    for i, c in enumerate(colors):
        y = 4.55 - i * 0.92
        _chip(ax, 0, y, 0.55, 0.72, c, radius=0.08)
        ax.text(0.64, y + 0.36, c, color=t["muted"], fontsize=8.5,
                family=MONO, va="center")
    ax.set_xlim(0, 1.6)
    ax.set_ylim(-0.1, 6.1)
    _save(fig, "image-palette", theme)


def colorblind(theme):
    t = THEMES[theme]
    palettes_ = [
        ('cmaps.colors("cud")', cmaps.colors("cud")[1:]),
        ("p.red() / p.green()", [P.red(), P.green(), P.red(shade=70),
                         P.green(shade=30)]),
    ]
    views = [
        ("Normal vision", lambda c: c),
        ("Protanopia", lambda c: rgb_to_hex(
            *simulate_red_blindness(*hex_to_rgb(c)[:3]))),
        ("Deuteranopia", lambda c: rgb_to_hex(
            *simulate_green_blindness(*hex_to_rgb(c)[:3]))),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(10, 1.9),
                             gridspec_kw={"width_ratios": [7, 4]})
    fig.patch.set_facecolor(t["bg"])
    fig.subplots_adjust(left=0.13, right=0.99, wspace=0.08, top=0.8,
                        bottom=0.02)
    for k, (ax, (title, colors)) in enumerate(zip(axes, palettes_)):
        ax.set_axis_off()
        ax.set_title(title, loc="left", color=t["ink"], fontsize=9,
                     family=MONO, pad=6)
        for r, (label, view) in enumerate(views):
            y = len(views) - r - 1
            if k == 0:
                ax.text(-0.15, y + 0.4, label, ha="right", va="center",
                        color=t["muted"], fontsize=8)
            for i, c in enumerate(colors):
                _chip(ax, i, y + 0.06, 0.9, 0.7, view(c), radius=0.1)
        ax.set_xlim(-0.05, len(colors))
        ax.set_ylim(0, len(views))
    _save(fig, "colorblind", theme)


if __name__ == "__main__":
    banner()
    logo()
    for mode in THEMES:
        palettes(mode)
        shades(mode)
        colormaps(mode)
        examples(mode)
        harmonies(mode)
        colorblind(mode)
        image_palette(mode)
