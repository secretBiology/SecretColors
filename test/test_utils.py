#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Tests the utility classes

from SecretColors.utils import *
import random

import pytest


def test_rgb_conversions():
    """
    Tests all RGB related conversion functions
    """
    for _ in range(1000):
        r = random.random()
        g = random.random()
        b = random.random()
        # RGB to Hex conversion
        r_hex = rgb_to_hex(r, g, b)
        r_rgb = hex_to_rgb(r_hex)
        r2_hex = rgb_to_hex(*r_rgb)
        assert r_hex == r2_hex
        assert r_rgb == pytest.approx((r, g, b), abs=0.01)
        # RGB to HSV
        m_hsv = rgb_to_hsv(r, g, b)
        m_rgb = hsv_to_rgb(*m_hsv)
        m2_hsv = rgb_to_hsv(*m_rgb)
        assert m_hsv == pytest.approx(m2_hsv, abs=0.01)
        assert m_rgb == pytest.approx((r, g, b), abs=0.01)
        # RGB to RGB255
        rgb255 = rgb_to_rgb255(r, g, b)
        assert (r, g, b) == pytest.approx(rgb255_to_rgb(*rgb255), abs=0.01)
        # RGB to HSL
        n_hsl = rgb_to_hsl(r, g, b)
        n_rgb = hsl_to_rgb(*n_hsl)
        n2_hsl = rgb_to_hsl(*n_rgb)
        assert n_hsl == pytest.approx(n2_hsl, abs=0.01)
        assert n_rgb == pytest.approx((r, g, b), abs=0.01)

        # RGB to XYZ
        for to_xyz, to_rgb in [(rgb_to_xyz, xyz_to_rgb),
                               (adobe_rgb_to_xyz, xyz_to_adobe_rgb)]:
            x_xyz = to_xyz(r, g, b)
            x_rgb = to_rgb(*x_xyz)
            assert x_rgb == pytest.approx((r, g, b), abs=1e-5)
        # sRGB to linear
        assert linear_to_srgb(*srgb_to_linear(r, g, b)) == pytest.approx(
            (r, g, b), abs=1e-9)


def test_white_xyz():
    xyz = rgb_to_xyz(1, 1, 1)
    assert xyz == pytest.approx((0.95047, 1, 1.08883), abs=1e-4)
    assert xyz_to_rgb(*xyz) == pytest.approx((1, 1, 1), abs=1e-5)


def test_negative_xyz():
    with pytest.raises(ValueError):
        xyz_to_rgb(-0.1, 0.5, 0.5)


@pytest.mark.parametrize("value, expected", [
    (0, 0), (1, 1), (0.5, 0.21404114), (0.02, 0.02 / 12.92)])
def test_gamma_transforms(value, expected):
    assert apply_linear_transform(value) == pytest.approx(expected)
    assert apply_gamma_transform(expected) == pytest.approx(value)


def test_deprecated_srgb_aliases():
    with pytest.warns(DeprecationWarning):
        assert rgb_to_srgb(0.5, 0.5, 0.5) == srgb_to_linear(0.5, 0.5, 0.5)
    with pytest.warns(DeprecationWarning):
        assert srgb_to_rgb(0.2, 0.2, 0.2) == linear_to_srgb(0.2, 0.2, 0.2)


@pytest.mark.parametrize("h", [0, 1 / 3, 2 / 3, 1])
def test_hsv_hue_bounds(h):
    assert hsv_to_rgb(h, 1, 1) == hsv_to_rgb(h % 1, 1, 1)


def test_cmyk():
    assert cmy_to_cmyk(1, 1, 1) == (0, 0, 0, 1)
    assert cmy_to_cmyk(0, 0, 0) == (0, 0, 0, 0)
    assert cmyk_to_cmy(*cmy_to_cmyk(0.2, 0.5, 0.7)) == pytest.approx(
        (0.2, 0.5, 0.7))


def test_luminance_and_text_color():
    assert relative_luminance("#ffffff") == pytest.approx(1)
    assert relative_luminance("#000000") == pytest.approx(0)
    assert relative_luminance("#ff0000ff") == relative_luminance("#ff0000")
    assert text_color("#ffffff") == "#000000"
    assert text_color("#000000") == "#ffffff"
    assert text_color("#00000080") == "#ffffff"


@pytest.mark.parametrize("func", [simulate_red_blindness,
                                  simulate_green_blindness])
def test_color_blindness(func):
    for _ in range(500):
        c = (random.random(), random.random(), random.random())
        r, g, b = func(*c)
        assert r == g
        assert all(0 <= x <= 1 for x in (r, g, b))
    assert func(1, 1, 1) == pytest.approx((1, 1, 1), abs=0.02)
    gray = func(0.5, 0.5, 0.5)
    assert gray == pytest.approx((0.5, 0.5, 0.5), abs=0.02)
    assert func(1, 0, 0)[2] < 0.2


def test_color_in_between():
    assert color_in_between("#000000", "#ffffff", 3) == [
        "#404040", "#808080", "#bfbfbf"]
