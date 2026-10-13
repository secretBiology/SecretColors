import random

import pytest

matplotlib = pytest.importorskip("matplotlib")

from SecretColors import ColorMap, Palette
from SecretColors.cmaps import BrewerMap, TableauMap

STANDARD = ["greens", "reds", "oranges", "purples", "grays", "blues"]


@pytest.mark.parametrize("method", STANDARD)
@pytest.mark.parametrize("palette", ["ibm", "material", "brewer", "tableau"])
def test_standard_maps(method, palette):
    cm = ColorMap(matplotlib, palette=Palette(palette))
    func = getattr(cm, method)
    assert func().N == 256
    assert func(no_of_colors=5, is_qualitative=True).N == 5
    assert func(starting_shade=20, ending_shade=80, no_of_colors=4,
                is_qualitative=True).N == 4
    assert func(is_reversed=True).N == 256


def test_minimum_colors():
    with pytest.raises(ValueError):
        ColorMap(matplotlib).greens(no_of_colors=1)


def test_from_list():
    cm = ColorMap(matplotlib)
    assert cm.from_list(["#ff0000", "#0000ff"], is_qualitative=True).N == 2


def test_special_maps():
    bm = BrewerMap(matplotlib)
    assert "Spectral" in bm.get_all
    assert len(bm.get_colors("Spectral", 9)) == 9
    assert bm.get("Spectral", no_of_colors=9, is_qualitative=True).N == 9
    with pytest.raises(ValueError):
        bm.get_colors("NoSuchMap", 3)
    with pytest.raises(ValueError):
        bm.get_colors("Spectral", 99)
    with pytest.raises(ValueError):
        bm.get("NoSuchMap")
    tm = TableauMap(matplotlib)
    assert tm.get_all
    with pytest.raises(ValueError):
        ColorMap(matplotlib).get("Spectral")


def test_random_divergent_and_seed():
    random.seed(4)
    expected = random.random()
    random.seed(4)
    a = ColorMap(matplotlib, seed=9).random_divergent(is_qualitative=True)
    b = ColorMap(matplotlib, seed=9).random_divergent(is_qualitative=True)
    assert random.random() == expected
    assert list(a.colors) == list(b.colors)
    assert BrewerMap(matplotlib, seed=1).random_divergent().N == 256
