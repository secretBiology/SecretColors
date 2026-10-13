import io
import sys

import pytest

from SecretColors.image import extract_palette
from SecretColors.utils import delta_e

Image = pytest.importorskip("PIL.Image")
ImageDraw = pytest.importorskip("PIL.ImageDraw")

BLOCKS = ["#fa4d56", "#4589ff", "#24a148", "#f1c21b"]


def _blocks(mode="RGB", size=(200, 200)):
    img = Image.new(mode, size)
    draw = ImageDraw.Draw(img)
    w, h = size
    boxes = [(0, 0, w // 2, h // 2), (w // 2, 0, w, h // 2),
             (0, h // 2, w // 2, h), (w // 2, h // 2, w, h)]
    for box, color in zip(boxes, BLOCKS):
        draw.rectangle(box, fill=color)
    return img


def _matches(found, expected, tolerance=3):
    return all(min(delta_e(f, e) for e in expected) < tolerance
               for f in found)


def test_dominant_colors():
    colors = extract_palette(_blocks(), n=4)
    assert len(colors) == 4
    assert _matches(colors, BLOCKS)
    assert _matches(BLOCKS, colors)


def test_inputs(tmp_path):
    img = _blocks()
    path = tmp_path / "blocks.png"
    img.save(path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    expected = extract_palette(img, n=4)
    assert extract_palette(path, n=4) == expected
    assert extract_palette(str(path), n=4) == expected
    assert extract_palette(buffer, n=4) == expected
    assert img.size == (200, 200)
    with pytest.raises(TypeError):
        extract_palette(42)


def test_frequency_order():
    img = Image.new("RGB", (100, 100), "#4589ff")
    ImageDraw.Draw(img).rectangle((0, 0, 100, 20), fill="#fa4d56")
    colors = extract_palette(img, n=2)
    assert delta_e(colors[0], "#4589ff") < 3
    assert delta_e(colors[1], "#fa4d56") < 3


def test_sorting():
    lightness = extract_palette(_blocks(), n=4, sort="lightness")
    assert delta_e(lightness[0], "#f1c21b") < 3
    hue = extract_palette(_blocks(), n=4, sort="hue")
    assert delta_e(hue[0], "#fa4d56") < 3
    assert delta_e(hue[-1], "#4589ff") < 3
    with pytest.raises(ValueError):
        extract_palette(_blocks(), sort="random")


def test_fewer_colors_than_requested():
    colors = extract_palette(Image.new("RGB", (50, 50), "#24a148"), n=5)
    assert colors == ["#24a148"]


def test_transparency():
    img = _blocks("RGBA")
    ImageDraw.Draw(img).rectangle((0, 0, 200, 100), fill=(0, 0, 0, 0))
    colors = extract_palette(img, n=2)
    assert _matches(colors, BLOCKS[2:])
    with pytest.raises(ValueError):
        extract_palette(Image.new("RGBA", (10, 10), (0, 0, 0, 0)))


def test_reproducible():
    img = _blocks()
    assert extract_palette(img, n=3, seed=1) == extract_palette(img, n=3,
                                                                seed=1)


@pytest.mark.parametrize("kwargs, error", [
    (dict(n=0), ValueError),
    (dict(n=2.5), TypeError),
    (dict(n=True), TypeError),
    (dict(max_size=0), ValueError),
])
def test_invalid_arguments(kwargs, error):
    with pytest.raises(error):
        extract_palette(_blocks(), **kwargs)


def test_without_pillow(monkeypatch):
    monkeypatch.setitem(sys.modules, "PIL", None)
    with pytest.raises(ImportError, match="SecretColors\\[image\\]"):
        extract_palette("image.png")
