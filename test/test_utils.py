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
        #  RGB to XYZ
        x_xyz = rgb_to_xyz(r, g, b)
        x_rgb = xyz_to_rgb(*x_xyz)
        x2_xyz = rgb_to_xyz(*x_rgb)
        assert x2_xyz == pytest.approx(x_xyz, abs=0.01)
        assert x_rgb == pytest.approx((r, g, b), abs=0.01)
