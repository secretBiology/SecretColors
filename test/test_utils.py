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


def test_rgb_space_matrices():
    from SecretColors.data.rgb_xyz import RX_DATA, WHITE_POINTS
    for space, references in RX_DATA.items():
        for reference, m in references.items():
            white = [sum(m["xyz"][k]) for k in "xyz"]
            assert white == pytest.approx(WHITE_POINTS[reference], abs=1e-4)
            to_rgb = [m["rgb"][k] for k in "rgb"]
            to_xyz = [m["xyz"][k] for k in "xyz"]
            for i in range(3):
                for k in range(3):
                    v = sum(to_rgb[i][j] * to_xyz[j][k] for j in range(3))
                    assert v == pytest.approx(float(i == k), abs=1e-4)


@pytest.mark.parametrize("space", list(rgb_spaces()))
def test_all_rgb_spaces(space):
    for reference in rgb_spaces()[space]:
        for _ in range(50):
            c = (random.random(), random.random(), random.random())
            xyz = rgb_to_xyz(*c, space=space, reference=reference)
            assert xyz_to_rgb(*xyz, space=space, reference=reference) == \
                pytest.approx(c, abs=1e-5)
    assert rgb_to_xyz(1, 1, 1, space=space) == pytest.approx(
        rgb_to_xyz(1, 1, 1, space=space, reference=rgb_spaces()[space][0]))


def test_rgb_space_names():
    assert rgb_to_xyz(0.2, 0.5, 0.1, space="Pro-Photo") == rgb_to_xyz(
        0.2, 0.5, 0.1, space="pro_photo")
    assert rgb_to_xyz(1, 0, 0) == rgb_to_xyz(1, 0, 0, space="srgb",
                                             reference="d65")
    with pytest.raises(ValueError):
        rgb_to_xyz(1, 0, 0, space="unknown")
    with pytest.raises(ValueError):
        rgb_to_xyz(1, 0, 0, space="pro_photo", reference="D65")


@pytest.mark.parametrize("hex_color, lab", [
    ("#ff0000", (53.2408, 80.0925, 67.2032)),
    ("#00ff00", (87.7347, -86.1827, 83.1793)),
    ("#0000ff", (32.2970, 79.1875, -107.8602)),
    ("#ffffff", (100, 0, 0)),
    ("#000000", (0, 0, 0)),
    ("#808080", (53.5850, 0, 0)),
])
def test_lab(hex_color, lab):
    assert hex_to_lab(hex_color) == pytest.approx(lab, abs=1e-3)
    assert lab_to_hex(*lab) == hex_color


def test_lab_round_trip():
    for _ in range(500):
        c = (random.random(), random.random(), random.random())
        assert lab_to_rgb(*rgb_to_lab(*c)) == pytest.approx(c, abs=1e-5)
        xyz = rgb_to_xyz(*c)
        for reference in ("D65", "D50", "A"):
            lab = xyz_to_lab(*xyz, reference=reference)
            assert lab_to_xyz(*lab, reference=reference) == pytest.approx(
                xyz, abs=1e-9)
        lab = rgb_to_lab(*c)
        assert lch_to_lab(*lab_to_lch(*lab)) == pytest.approx(lab, abs=1e-9)


def test_lab_gamut():
    assert lab_to_hex(150, 0, 0) == "#ffffff"
    assert lab_to_hex(50, 200, 0) == lab_to_hex(50, 200, 0)
    with pytest.raises(ValueError):
        lab_to_rgb(50, 200, 0, clip=False)
    with pytest.raises(ValueError):
        xyz_to_lab(0.5, 0.5, 0.5, reference="D99")


@pytest.mark.parametrize("lab1, lab2, expected", [
    ((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425),
    ((50, 3.1571, -77.2803), (50, 0, -82.7485), 2.8615),
    ((50, 2.8361, -74.0200), (50, 0, -82.7485), 3.4412),
    ((50, -1.3802, -84.2814), (50, 0, -82.7485), 1.0000),
    ((50, 0, 0), (50, -1, 2), 2.3669),
    ((50, 2.5, 0), (73, 25, -18), 27.1492),
])
def test_ciede2000(lab1, lab2, expected):
    assert delta_e(lab1, lab2) == pytest.approx(expected, abs=1e-4)
    assert delta_e(lab2, lab1) == pytest.approx(expected, abs=1e-4)


def test_delta_e():
    assert delta_e("#fa4d56", "#fa4d56") == 0
    assert delta_e("#000000", "#ffffff", method="cie76") == pytest.approx(100)
    assert delta_e("#fa4d56", "#fa4d57") < 1
    with pytest.raises(ValueError):
        delta_e("#000000", "#ffffff", method="cie94")
    with pytest.raises(ValueError):
        delta_e((1, 2), "#ffffff")
