"""Deprecation messages must explain how to migrate, with a removal deadline."""

import pytest

from SecretColors import ColorWheel, Palette
from SecretColors.cmaps import BrewerMap, ColorMap, TableauMap
from SecretColors.utils import rgb_to_srgb, srgb_to_rgb, srgb_to_linear, linear_to_srgb


@pytest.mark.parametrize("old,new,value", [
    ("no_of_colors", "n", 3),
    ("starting_shade", "start", 20),
    ("ending_shade", "end", 80),
])
def test_keyword_migration_guidance(old, new, value):
    palette = Palette()
    with pytest.warns(DeprecationWarning) as caught:
        actual = palette.blue(**{old: value})
    assert actual == palette.blue(**{new: value})
    message = str(caught[0].message)
    assert f"Palette.blue(..., {new}=...)" in message
    assert "removed in the next major release" in message


@pytest.mark.parametrize("old", ["is_reserved", "is_reversed"])
def test_wheel_alias_migration_guidance(old):
    wheel = ColorWheel("#123456")
    with pytest.warns(DeprecationWarning) as caught:
        assert wheel.triadic(**{old: True}) == wheel.triadic(reverse=True)
    assert "ColorWheel.triadic(..., reverse=...)" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)


@pytest.mark.parametrize("old,new", [
    ("get_color_dict", "color_dict"),
    ("get_color_list", "color_list"),
])
def test_property_migration_guidance(old, new):
    palette = Palette()
    with pytest.warns(DeprecationWarning) as caught:
        assert getattr(palette, old) == getattr(palette, new)
    assert f"palette.{new}" in str(caught[0].message)
    assert "without parentheses" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)


@pytest.mark.parametrize("call,option", [
    (lambda **kw: Palette(**kw).color_list, "allow_gray_shades"),
    (lambda **kw: Palette(seed=42).random(**kw), "ignore_gray"),
    (lambda **kw: Palette(seed=42).random(**kw), "force_gray"),
    (lambda **kw: Palette(seed=42).random_gradient(**kw), "ignore_gray"),
])
def test_ignored_option_migration_preserves_behavior(call, option):
    with pytest.warns(DeprecationWarning) as caught:
        actual = call(**{option: True})
    assert actual == call()
    assert f"Remove '{option}' from the call" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)


def test_cycle_migration_guidance_preserves_skip():
    with pytest.warns(DeprecationWarning) as caught:
        actual = next(Palette().cycle(1, 2))
    assert actual == next(Palette().cycle(skip_first=2))
    assert "palette.cycle(skip_first=2)" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)


@pytest.mark.parametrize("cls", [ColorMap, BrewerMap, TableauMap])
def test_colormap_migration_guidance(cls):
    with pytest.warns(DeprecationWarning) as caught:
        cls()
    message = str(caught[0].message)
    assert "from SecretColors import cmaps" in message
    assert "cmaps.cmap(name, n=..., discrete=False)" in message
    assert "cmaps.from_colors(color_list)" in message
    assert "cmaps.colors(name, n=...)" in message
    assert "removed in the next major release" in message


def test_colormap_count_property_migration_guidance():
    with pytest.warns(DeprecationWarning):
        colormap = ColorMap()
    with pytest.warns(DeprecationWarning) as caught:
        colormap.no_of_colors = 4
    assert "colormap.n = value" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)
    with pytest.warns(DeprecationWarning) as caught:
        assert colormap.no_of_colors == colormap.n == 4
    assert "Read 'colormap.n'" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)


@pytest.mark.parametrize("old,new,args", [
    (rgb_to_srgb, srgb_to_linear, "r, g, b"),
    (srgb_to_rgb, linear_to_srgb, "sr, sg, sb"),
])
def test_conversion_migration_guidance(old, new, args):
    with pytest.warns(DeprecationWarning) as caught:
        assert old(0.2, 0.4, 0.6) == new(0.2, 0.4, 0.6)
    assert f"SecretColors.utils.{new.__name__}({args})" in str(caught[0].message)
    assert "removed in the next major release" in str(caught[0].message)
