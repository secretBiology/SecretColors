#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# Object testing includes test from model.objects

import pytest

from SecretColors.models.objects import (ColorOutput, ColorString,
                                         ColorTuple, ColorWheel)

test_data = [
    ("#ffffff", False, (1, 1, 1, 1), "#ffffff"),
    ((0, 0, 0), True, (0, 0, 0, 1), "#000000"),
    ("101010", False, (16 / 255, 16 / 255, 16 / 255, 1), "101010"),
    (
        "#f1f1f1f1", False,
        (241 / 255, 241 / 255, 241 / 255, 241 / 255),
        "#f1f1f1"
    ),
    (
        (0.129, 0.576, 0.819), True,
        (33 / 255, 147 / 255, 209 / 255, 1),
        "#2193d1"
    ),
    ((0.39991, 0.7189, 1, 0.1), True, (0.39991, 0.7189, 1, 0.1), "#66b7ff")
]


@pytest.mark.parametrize("color, is_tuple, rgba, hex_color", test_data)
def test_color_object_type(color, is_tuple, rgba, hex_color):
    col = ColorOutput(color)
    assert col.is_tuple == is_tuple
    assert col.rgba == pytest.approx(rgba, rel=1e-2)
    assert col.hex == hex_color


@pytest.mark.parametrize("color", [
    4,
    {"something": "here"},
    True,
    None,
    ColorOutput("#fff"),
    [2, 3],
    [0.1, 0.5, 0.5],
    ("0.3", "0.4", "1")
])
def test_color_type_errors(color):
    # _RawColor type error
    with pytest.raises(TypeError):
        ColorOutput(color)


@pytest.mark.parametrize("color", [
    (),
    "#f",
    (0.2, 0.5),
    (1, 2, 3, 5),
    (-1, 0, 0.4),
    "fffffg",
    "#0000000000",
    (0.2, 0.5, 0.8, 1, 0.5)
])
def test_color_value_errors(color):
    with pytest.raises(ValueError):
        ColorOutput(color)


def test_odd_cases():
    """_RawColor the odd cases
    """
    with pytest.raises(TypeError):
        ColorOutput(1, 0.1, 1)


def test_color_objects():
    """
    _RawColor the characteristics of str and tuple
    """
    col_str = ColorString("#ffffff")
    col_tuple = ColorTuple((0, 1, 0.6))

    assert isinstance(col_str, str)
    assert isinstance(col_tuple, tuple)
    assert col_str.replace("f", "") == "#"
    assert col_tuple[1] == 1
    assert len(col_tuple) == 3




def test_string_and_tuple_semantics():
    c = ColorString("#ff0000")
    assert c + "80" == "#ff000080"
    assert "color: " + c == "color: #ff0000"
    t = ColorTuple((1, 0, 0))
    assert t + (1,) == (1, 0, 0, 1)


def test_blend():
    c = ColorString("#ff0000")
    assert c.blend("#0000ff") == "#800080"
    assert c.blend((0, 0, 1)) == "#800080"
    assert c.blend(ColorString("#0000ff")) == "#800080"
    assert isinstance(c.blend("#0000ff"), ColorString)
    with pytest.raises(TypeError):
        c.blend(5)


def test_color_wheel():
    cw = ColorWheel("#fa4d56")
    cw.rotate_hue(180)
    assert cw.color == "#4dfaf1"
    cw.rotate_hue(-180)
    assert cw.color == "#fa4d56"
    cw.rotate_hue(360 * 3)
    assert cw.color == "#fa4d56"

    white = ColorWheel("#ffffff")
    white.rotate_lightness(0)
    assert white.color == "#ffffff"
    white.rotate_lightness(90)
    assert white.color == "#ffffff"
    white.rotate_lightness(-720)
    assert white.color == "#000000"

    gray = ColorWheel("#808080")
    gray.rotate_saturation(-90)
    assert gray.color == "#808080"
    assert len(ColorWheel("#fa4d56").tetradic()) == 4
