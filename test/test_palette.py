#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
import random

import pytest
from SecretColors.models.palette import Palette


def test_basics():
    p = Palette()
    p2 = Palette("material", color_mode="rgb")
    assert p.name == "ibm"
    assert p.color_mode == "hex"
    assert p2.name == "material"
    assert p2.color_mode == "rgb"


ALL_NAMES = ["ibm", "material", "material-accent", "brewer", "clarity",
             "tableau", "spectrum", "latitude"]


def test_unknown_palette():
    with pytest.raises(ValueError):
        Palette("materia")


def test_unknown_color_mode():
    with pytest.raises(ValueError):
        Palette(color_mode="cmyk")


@pytest.mark.parametrize("mode, alpha, expected", [
    ("hexa", None, "#24a148ff"),
    ("ahex", None, "#ff24a148"),
    ("hexa", 0.5, "#24a14880"),
    ("ahex", 0, "#0024a148"),
])
def test_alpha_modes(mode, alpha, expected):
    assert Palette(color_mode=mode).green(alpha=alpha) == expected


def test_rgba_mode():
    c = Palette(color_mode="rgba").green(alpha=0.3)
    assert len(c) == 4
    assert c[3] == 0.3


@pytest.mark.parametrize("name", ALL_NAMES)
@pytest.mark.parametrize("n", [1, 5, 12, 40])
def test_random(name, n):
    p = Palette(name, seed=7)
    colors = p.random(n, force_list=True)
    assert len(colors) == n
    assert len(p.random(n, starting_shade=15, ending_shade=85,
                        force_list=True)) == n
    assert len(p.random(n, gradient=False, force_list=True)) == n
    assert len(p.random(n, reverse=True, force_list=True)) == n


def test_random_single_and_shade():
    p = Palette(seed=1)
    assert isinstance(p.random(), str)
    assert p.random(shade=0) == "#ffffff"
    assert p.random(3, shade=0) == ["#ffffff"] * 3


def test_random_invalid():
    p = Palette()
    with pytest.raises(ValueError):
        p.random(0)
    with pytest.raises(ValueError):
        p.random(avoid=list(p.colors.keys()))


def test_seed_is_local():
    assert Palette(seed=3).random(10) == Palette(seed=3).random(10)
    random.seed(11)
    expected = random.random()
    random.seed(11)
    Palette(seed=5).random(5)
    assert random.random() == expected


def test_seed_zero():
    p = Palette(seed=0)
    assert p.seed == 0
    assert p.random(5) == Palette(seed=0).random(5)


def test_iteration():
    p = Palette()
    assert list(p) == p.color_list
    assert list(p) == list(p)


@pytest.mark.parametrize("name", ALL_NAMES)
def test_random_gradient(name):
    p = Palette(name, seed=0)
    for _ in range(300):
        assert len(p.random_gradient()) == 3
        assert len(p.random_gradient(complementary=False)) == 3
    assert len(p.random_gradient(no_of_colors=7)) == 7
    assert len(p.random_gradient(no_of_colors=2)) == 2


def test_shade_zero():
    p = Palette()
    assert p.red(shade=0) == "#ffffff"
    assert p.red(shade=100) == "#2d0709"
    assert p.get("red", shade=0) == "#ffffff"


def test_multiple_colors():
    p = Palette(seed=2)
    assert len(p.red(no_of_colors=5)) == 5
    assert p.red(no_of_colors=3, starting_shade=0, ending_shade=100)[0] == \
        "#ffffff"
    assert len(p.red(no_of_colors=4, gradient=False)) == 4
    with pytest.raises(ValueError):
        p.red(no_of_colors=0)


def test_lookup_does_not_mutate_palette():
    p = Palette()
    before = list(p.colors)
    assert p.get("amber") == Palette("material").amber()
    assert p.amber() == p.get("amber")
    p.get("aquamarine")
    p.get("GhostWhite", naming="x11", strict_search=True)
    assert list(p.colors) == before
    assert len(p.color_list) == len(before)


def test_synonyms_and_named_colors():
    p = Palette()
    assert p.get("grey") == p.gray()
    assert p.get("k") == p.black()
    assert p.get("aquamarine") == "#7fffd4"
    assert p.get("gray", strict_search=True) == "#808080"
    assert p.get("gray", naming="x11", strict_search=True) == "#bebebe"
    assert p.get("GhostWhite", shade=80) == "#636366"
    with pytest.raises(KeyError):
        p.get("no-such-color")
    with pytest.raises(ValueError):
        p.get("red", naming="css4")


def test_named_color_in_rgb_mode():
    c = Palette(color_mode="rgb").get("aquamarine")
    assert c == pytest.approx((127 / 255, 1, 212 / 255))


def test_cycle():
    cycle = Palette().cycle()
    colors = [next(cycle) for _ in range(60)]
    assert len(set(colors[:18])) == 18


def test_color_collections():
    p = Palette()
    assert p.color_list == list(p.color_dict.values())
    assert list(p.color_dict) == list(p.colors)
    with pytest.warns(DeprecationWarning):
        assert p.get_color_list == p.color_list
    with pytest.warns(DeprecationWarning):
        assert p.get_color_dict == p.color_dict


def test_removed_methods():
    assert not hasattr(Palette, "color_between")
    assert not hasattr(Palette, "cmap_from")


@pytest.mark.parametrize("name, red, blue", [
    ("spectrum", "#d73220", "#3b63fb"),
    ("latitude", "#d92736", "#6294be"),
])
def test_new_palettes(name, red, blue):
    p = Palette(name)
    assert p.red() == red
    assert p.blue() == blue
    assert p.red(shade=0) == "#ffffff"
    assert len(p.blue(no_of_colors=5)) == 5
