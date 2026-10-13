#  Copyright (c) SecretBiology  2026.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Sphinx directives which render color swatches directly from the library,
#  so documentation never goes out of sync with the data.
#
#  .. palette-swatches:: ibm
#  .. colormap-swatches:: brewer

import html

from docutils import nodes
from docutils.parsers.rst import Directive

from SecretColors import Palette, cmaps
from SecretColors.cmaps.maps import _QUALITATIVE, _SPECIAL
from SecretColors.utils import hex_to_hsl, text_color

_KIND = {"seq": "sequential", "div": "diverging"}


def _raw(markup: str):
    return [nodes.raw("", markup, format="html")]


def _hue_order(palette: Palette):
    def key(name):
        h, s, _ = hex_to_hsl(palette.get(name))
        return s < 0.15, (h + 0.04) % 1

    return sorted((n for n in palette.colors if n not in ("white", "black")),
                  key=key)


class PaletteSwatches(Directive):
    required_arguments = 1

    def run(self):
        name = self.arguments[0].strip()
        p = Palette(name)
        shades = sorted(p._value.get_shades())
        core = p._value.get_core_shade()
        rows = []
        for color in _hue_order(p):
            chips = []
            for s in shades:
                c = p.get(color, shade=s)
                star = " sc-core" if s == core else ""
                chips.append(
                    f'<span class="sc-chip{star}" style="background:{c};'
                    f'color:{text_color(c)}" title="{html.escape(color)} '
                    f'shade={s:g} · {c}"><span>{c}</span></span>')
            rows.append(f'<div class="sc-row"><code class="sc-name">'
                        f'{html.escape(color)}</code><div class="sc-chips">'
                        f'{"".join(chips)}</div></div>')
        header = "".join(f"<span>{s:g}</span>" for s in shades)
        markup = (f'<div class="sc-swatches" data-palette="{name}">'
                  f'<div class="sc-row sc-header"><span class="sc-name">'
                  f'shade</span><div class="sc-chips">{header}</div></div>'
                  f'{"".join(rows)}</div>')
        return _raw(markup)


class ColormapSwatches(Directive):
    required_arguments = 1

    def run(self):
        source = self.arguments[0].strip()
        rows = []
        for name in cmaps.available(source):
            colors = cmaps.colors(name)
            if source == "standard":
                kind = "sequential"
            else:
                kind = _SPECIAL[name][1].get("type")
                kind = "qualitative" if kind in _QUALITATIVE else \
                    _KIND.get(kind, kind)
            if kind == "qualitative":
                strip = "".join(
                    f'<span style="background:{c}" title="{c}"></span>'
                    for c in colors)
                strip = f'<div class="sc-strip sc-discrete">{strip}</div>'
            else:
                stops = ", ".join(colors)
                strip = (f'<div class="sc-strip" style="background:'
                         f'linear-gradient(to right, {stops})"></div>')
            rows.append(f'<div class="sc-cmap"><div class="sc-cmap-head">'
                        f'<code>"sc.{html.escape(name)}"</code>'
                        f'<span class="sc-badge sc-{kind}">{kind}</span>'
                        f'</div>{strip}</div>')
        return _raw(f'<div class="sc-cmaps">{"".join(rows)}</div>')


def setup(app):
    app.add_directive("palette-swatches", PaletteSwatches)
    app.add_directive("colormap-swatches", ColormapSwatches)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
