"""Validated HTML swatches; independent of palette and color science code."""

import html
from SecretColors._color import ColorValue


def _swatch_html(colors: list, labels: list) -> str:
    chips = []
    for color, label in zip(colors, labels):
        value = ColorValue.parse(color)
        css = value.hex(alpha=value.rgba[3] < 1)
        label = html.escape(str(label), quote=True)
        chips.append(
            '<div style="display:inline-block;margin:0 6px 6px 0;'
            'text-align:center;font:11px monospace">'
            f'<div role="img" aria-label="{label}" title="{label}" '
            'style="width:56px;height:36px;border-radius:6px;overflow:hidden;'
            'background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) '
            '0 0/12px 12px;box-shadow:inset 0 0 0 1px #888">'
            f'<div style="width:100%;height:100%;background:{css}"></div></div>'
            f'{css}</div>')
    return f'<div>{"".join(chips)}</div>'

