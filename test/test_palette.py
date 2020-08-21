#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
import pytest
from SecretColors.models.palette import Palette


def test_basics():
    p = Palette()
    p2 = Palette("material", color_mode="rgb")
    assert p.name == "ibm"
    assert p.color_mode == "hex"
    assert p2.name == "material"
    assert p2.color_mode == "rgb"
