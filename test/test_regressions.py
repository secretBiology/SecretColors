"""Cross-feature contracts and output compatibility captured before the refactor."""

import copy
import hashlib
import json
import pickle
import warnings
from pathlib import Path

import pytest

from SecretColors import Palette, ColorMap, ColorWheel, cmaps, distinct_colors, check_colors
from SecretColors.cmaps import BrewerMap
from SecretColors.data.constants import ALL_PALETTES
from SecretColors.models.objects import ColorString, ColorTuple, ColorList
from SecretColors.utils import contrast_ratio, is_readable, mix, composite
from SecretColors.selection import DistinctnessWarning


def test_default_color_compatibility():
    expected = json.loads((Path(__file__).parent / "data/compatibility.json").read_text())

    def compare(key, value):
        digest = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
        assert digest == expected[key], key

    for name in ALL_PALETTES:
        p = Palette(name, seed=42)
        compare("palette/" + name, [
            (c, [p.get(c, shade=s) for s in [0, 10, 25, 37.5, 50, 80, 100]],
             p.get(c, n=5)) for c in p.colors])
        compare("random/" + name, [p.random(10), p.random(4, gradient=False),
                                    p.random_gradient(7)])
    for name in cmaps.available():
        compare("map/" + name, cmaps.colors(name))
    for name in ("ibm", "material", "spectrum"):
        compare("distinct/" + name, distinct_colors(8, palette=name))


@pytest.mark.parametrize("mode", ["hex", "hexa", "ahex", "rgb", "rgba"])
def test_representation_invariants(mode):
    c = Palette(color_mode=mode).red(alpha=0.5)
    assert c.rgb255 == (250, 77, 86)
    assert c.hex == "#fa4d56"
    if mode == "rgba":
        assert tuple(c) == c.rgba
    if mode == "rgb":
        assert tuple(c) == c.rgb
    if mode in ("hexa", "ahex"):
        assert c.alpha == 128 / 255
    assert mix(c, c)[:7] == "#fa4d56"


def test_normalized_constructors_and_immutability():
    assert ColorString((1, 0, 0)) == "#ff0000"
    assert ColorTuple("#ff0000") == (1, 0, 0)
    assert ColorString("  #F00 ").hex == "#ff0000"
    assert ColorString("#f008").alpha == 136 / 255
    c = Palette(color_mode="rgba").red(alpha=.5)
    for attr in ("r", "g", "b", "alpha", "_value"):
        with pytest.raises(AttributeError, match="immutable"):
            setattr(c, attr, .2)
    changed = c.with_alpha(.2)
    assert changed[3] == changed.alpha == .2
    assert c[3] == c.alpha == .5


@pytest.mark.parametrize("value", [ColorString("#ff0000ff"),
                                  ColorString("#80fa4d56", alpha_first=True),
                                  ColorTuple((1, 0, 0, .5))])
def test_copy_and_pickle(value):
    for result in (copy.copy(value), copy.deepcopy(value), pickle.loads(pickle.dumps(value))):
        assert result == value
        assert result.rgba == value.rgba


def test_transparent_accessibility():
    assert composite("#00000000", "#ffffff") == (1, 1, 1, 1)
    assert contrast_ratio("#00000000", "#ffffff") == 1
    assert not is_readable("#00000000", "#ffffff")
    assert not check_colors(["#00000000"]).ok
    report = check_colors(["#00000000", "#ffffff"])
    assert report.min_delta_e == 0
    with pytest.raises(ValueError, match="opaque"):
        contrast_ratio("#000000", "#ffffff80")
    with pytest.raises(ValueError, match="background"):
        check_colors(["#00000080"], background=None)
    ahex = Palette(color_mode="ahex").red(alpha=.5)
    assert contrast_ratio(ahex, "#ffffff") == contrast_ratio(ahex.rgba, "#ffffff")


def test_distinctness_policy():
    with pytest.warns(DistinctnessWarning, match="min_delta_e"):
        warned = distinct_colors(10)
    assert warned == distinct_colors(10, on_failure="ignore")
    with pytest.raises(ValueError, match="min_delta_e"):
        distinct_colors(10, on_failure="raise")
    with pytest.raises(ValueError, match="min_delta_e"):
        distinct_colors(2, palette=["#000000", "#010101"], on_failure="raise")
    assert distinct_colors(8, on_failure="raise") == warned[:8]
    with pytest.raises(ValueError):
        distinct_colors(1, on_failure="unknown")


def test_selection_respects_instance_and_cached_prefix():
    from SecretColors.selection import _order_state
    _order_state.cache_clear()
    first = distinct_colors(1)
    assert _order_state.cache_info().misses == 1
    assert distinct_colors(8)[:1] == first
    assert _order_state.cache_info().hits == 1
    p = Palette()
    p.colors.clear()
    with pytest.raises(ValueError, match="Only 0"):
        distinct_colors(1, palette=p)


def test_selecting_one_does_not_compute_all_pairs(monkeypatch):
    import SecretColors.selection as selection
    selection._order_state.cache_clear()
    def unexpected(*args):
        raise AssertionError("Single-color selection needs no pair distances")
    monkeypatch.setattr(selection, "_ciede2000", unexpected)
    assert len(distinct_colors(1, palette=["#123456", "#654321"], background=None)) == 1


def test_colormap_tuples_and_immutable_datasets():
    mpl = pytest.importorskip("matplotlib")
    with pytest.warns(DeprecationWarning):
        legacy = ColorMap(palette=Palette(color_mode="rgba"))
    m = legacy.blues()
    assert m(0.0)[:3] == pytest.approx(Palette().blue(shade=10).rgb)
    assert cmaps.from_colors([(1, 0, 0), (0, 0, 1)])(0.0) == (1, 0, 0, 1)
    assert cmaps.from_colors([(1, 0, 0, .2)], discrete=True)(0)[3] == .2
    with pytest.warns(DeprecationWarning):
        bm = BrewerMap()
    original = cmaps.colors("Spectral", n=3)
    bm.get_colors("Spectral", 3)[0] = "#000000"
    assert cmaps.colors("Spectral", n=3) == original
    with pytest.raises(TypeError):
        bm.data["Spectral"]["3"][0] = "#000000"


def test_perceptual_palette_sampling():
    p = Palette()
    expected = mix(p.yellow(shade=10), p.yellow(shade=20), space="lab")
    assert expected == "#ffdf6d"
    assert cmaps.colors("yellow", n=3, start=10, end=20, space="lab")[1] == expected
    assert p.sample("yellow", 3, start=10, end=20, space="lab")[1] == expected
    assert p.yellow(shade=15, space="lab") == expected


def test_notebook_html():
    html = Palette(color_mode="ahex").red(alpha=.1)._repr_html_()
    assert "background:#fa4d561a" in html
    assert "checkerboard" in html or "conic-gradient" in html
    assert "aria-label" in html
    with pytest.raises(ValueError):
        ColorList(['red;" data-probe="injected'])._repr_html_()


@pytest.mark.parametrize("invalid,error", [(True, TypeError), (2.9, TypeError),
                                         (0, ValueError), (-1, ValueError)])
def test_consistent_counts(invalid, error):
    p = Palette()
    for func in (p.random, p.random_gradient, lambda n: p.red(n=n),
                 lambda n: p.sample("red", n), lambda n: cmaps.colors("blues", n=n)):
        with pytest.raises(error):
            func(invalid)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_finite_inputs(value):
    for func in (lambda: Palette().red(shade=value),
                 lambda: Palette(color_mode="rgba").red(alpha=value),
                 lambda: distinct_colors(1, min_delta_e=value),
                 lambda: ColorTuple((value, 0, 0))):
        with pytest.raises(ValueError):
            func()


def test_alias_warnings_and_conflicts():
    p = Palette()
    with pytest.warns(DeprecationWarning, match="removed in the next major release"):
        assert p.blue(no_of_colors=3) == p.blue(n=3)
    with pytest.warns(DeprecationWarning, match="next major release"):
        assert p.get_color_list == p.color_list
    with pytest.raises(TypeError, match="not both"):
        p.blue(n=2, no_of_colors=3)
    with pytest.raises(TypeError):
        p.random(2, no_of_colors=3)
    cw = ColorWheel("#123456")
    for old in ("is_reserved", "is_reversed"):
        with pytest.warns(DeprecationWarning, match="next major release"):
            assert cw.triadic(**{old: True}) == cw.triadic(reverse=True)
    with pytest.raises(TypeError):
        cw.triadic(is_reserved=True, is_reversed=False)
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        p.sample("blue", 3)
        p.blue(n=3, start=20, end=80)
        cw.triadic(reverse=True)


def test_predictable_return_types_and_provenance():
    p = Palette()
    assert isinstance(p.color("red"), ColorString)
    assert isinstance(p.sample("red", 1), ColorList)
    assert len(p.sample("red", 1)) == 1
    assert p.resolve("red").source == "ibm"
    assert p.resolve("amber").source == "material"
    assert p.resolve("aquamarine").source == "w3"
    with pytest.raises(KeyError):
        p.color("amber", fallback=False)
    assert p.color("grey", fallback=False) == p.gray()
    assert cmaps.info("Set1").kind == "qualitative"
    assert cmaps.info("RdBu").kind == "diverging"
    assert cmaps.info("blues").kind == "sequential"


def test_gradient_diagnostics():
    from SecretColors.diagnostics import check_gradient, check_interpolation
    assert check_gradient(["#000000", "#777777", "#ffffff"]).monotonic_lightness
    report = check_gradient(["#000000", "#ffffff", "#000000"])
    assert not report.monotonic_lightness
    assert report.min_grayscale_delta_l == 0
    assert report.clipped_positions is None
    assert check_interpolation("#f1c21b", "#0f62fe", n=20, space="lch").clipped_positions
    assert not check_interpolation("#000000", "#ffffff", n=20).clipped_positions


def test_alpha_interpolation_and_space_normalization():
    from SecretColors.utils import color_in_between
    assert mix("#ff000000", "#0000ff80") == "#80008040"
    assert color_in_between("#ff000000", "#0000ff80", n=1) == ["#80008040"]
    assert ColorString("#ff000000").blend("#0000ff80") == "#80008040"
    pytest.importorskip("matplotlib")
    assert cmaps.cmap("RdBu", space=" LAB ")(.5) == cmaps.cmap("RdBu", space="lab")(.5)


@pytest.mark.parametrize("mode", ["hex", "hexa", "ahex", "rgb", "rgba"])
def test_deprecated_classes_preserve_palette_output_modes(mode):
    pytest.importorskip("matplotlib")
    p = Palette(color_mode=mode)
    with pytest.warns(DeprecationWarning):
        cm = ColorMap(palette=p)
    assert cm.blues()(0.0)[:3] == pytest.approx(p.blue(shade=10).rgb)


def test_legacy_default_count_alias():
    with pytest.warns(DeprecationWarning):
        cm = ColorMap()
    with pytest.warns(DeprecationWarning, match="next major release"):
        cm.no_of_colors = 4
    assert cm.n == 4
    with pytest.warns(DeprecationWarning, match="next major release"):
        assert cm.no_of_colors == 4


def test_reject_invalid_image_alpha():
    from SecretColors.image import extract_palette
    for value in (-1, 256, 1.5, True, float("nan")):
        with pytest.raises((TypeError, ValueError)):
            extract_palette("unused.png", min_alpha=value)
