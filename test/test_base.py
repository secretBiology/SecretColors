#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# tests objects from models.base

import pytest

from SecretColors.models.base import _RawColor, Color


def test_raw_colors():
    rc1 = _RawColor("#ffffff", 20)
    rc2 = _RawColor("#ffff3f", 25)
    rc3 = _RawColor("#ffff4f", 10)
    rc4 = _RawColor("#ffff5f", 10)

    assert not rc1 < rc1
    assert rc1 < rc2
    assert rc1 <= rc2
    assert rc2 > rc1
    assert rc2 >= rc1
    assert rc3 == rc4
    assert rc1 != rc4
    assert rc4 < 12
    assert rc4 <= 12
    assert rc4 > 2.33
    assert rc4 >= 2.33
    assert rc4 == 10


raw_error_data = [
    ("sample", [20, 20]),
    (["some", "something"], 2),
    ("some", [2, 2]),
    ([], []),
    (["a", "b"], [-1, 22]),
    (["a", "b"], [1, 122]),
]


@pytest.mark.parametrize("value, shades", raw_error_data)
def test_raw_errors(value, shades):
    with pytest.raises(ValueError):
        Color("test", value, shades)


def test_shades():
    white = "#ffffff"
    black = "#000000"
    c = Color("test", [white, black], [0, 100])
    c2 = Color("test", [black, white], [100, 0])
    assert c.name == "test"
    assert c.shade(0) == white
    assert isinstance(c.shade(0), str)
    assert c.shade(100) == black
    assert c.values[0] == c2.values[0]
    assert c.shade(50) == c2.shade(50)
    assert c.shade(50) == "#808080"
    assert c.shade(49.9999) == c.shade(50.001)
