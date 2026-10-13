import re
import sys

import pytest

from SecretColors import Palette, cmaps
from SecretColors.cmaps.maps import _SPECIAL, _QUALITATIVE
from SecretColors.data.names.w3 import W3_DATA
from SecretColors.data.names.x11 import X11_DATA
from SecretColors.data.palettes import (ClarityPalette, ColorBrewer,
                                        IBMPalette, LatitudePalette,
                                        MaterialAccentPalette,
                                        MaterialPalette, SpectrumPalette,
                                        TableauPalette)

HEX = re.compile(r"^#[0-9a-f]{6}$")


def test_all_data_is_valid():
    for name, (_, data) in _SPECIAL.items():
        for key, values in data.items():
            if key == "type":
                continue
            assert len(values) == int(key), name
            assert all(HEX.match(c.lower()) for c in values), name
    for palette in (IBMPalette, MaterialPalette, MaterialAccentPalette,
                    ClarityPalette, ColorBrewer, TableauPalette,
                    SpectrumPalette, LatitudePalette):
        p = palette()
        for name, values in p.get_all_colors().items():
            assert len(values) == len(p.get_shades()), name
            assert all(HEX.match(c.lower()) for c in values), name
    for data in (W3_DATA, X11_DATA):
        assert all(HEX.match(c.lower()) for c in data.values())


def test_available():
    names = cmaps.available()
    assert len(names) == len(set(names))
    assert cmaps.available("standard") == ["greens", "reds", "oranges",
                                           "purples", "grays", "blues"]
    for source in ("brewer", "tableau", "colorblind"):
        assert set(cmaps.available(source)) <= set(names)
    assert "Spectral" in cmaps.available("brewer")
    assert "tol_sunset" in cmaps.available("colorblind")
    with pytest.raises(ValueError):
        cmaps.available("unknown")


@pytest.mark.parametrize("name", cmaps.available())
def test_every_map(name):
    result = cmaps.colors(name)
    assert len(result) >= 2
    assert all(HEX.match(c) for c in result)
    assert cmaps.colors(name, reverse=True) == list(reversed(result))


def test_special_maps():
    assert cmaps.colors("Spectral", n=5) == [
        "#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]
    assert cmaps.colors("spectral", n=5) == cmaps.colors("Spectral", n=5)
    assert len(cmaps.colors("Spectral")) == 11
    interpolated = cmaps.colors("Spectral", n=21)
    assert len(interpolated) == 21
    assert interpolated[0] == "#9e0142"
    assert interpolated[-1] == "#5e4fa2"
    assert cmaps.colors("RdBu", start=10, end=90, n=3) == [
        "#b2182b", "#f7f7f7", "#2166ac"]
    assert cmaps.colors("tol_bu_rd")[-1] == "#b2182b"


def test_qualitative_maps():
    assert cmaps.colors("Set1", n=3) == ["#e41a1c", "#377eb8", "#4daf4a"]
    assert len(cmaps.colors("Tableau", n=4)) == 4
    assert len(cmaps.colors("cud")) == 8
    with pytest.raises(ValueError):
        cmaps.colors("Set1", n=50)
    with pytest.raises(ValueError):
        cmaps.colors("Set1", start=10)


def test_standard_maps():
    greens = cmaps.colors("greens", n=3)
    assert greens == [str(c) for c in Palette().green(
        no_of_colors=3, starting_shade=10, ending_shade=100)]
    assert cmaps.colors("greys") == cmaps.colors("grays")
    assert cmaps.colors("green") == cmaps.colors("greens")
    assert len(cmaps.colors("teal", palette="material", n=4)) == 4
    rgb = Palette("material", color_mode="rgb")
    assert cmaps.colors("blues", palette=rgb, n=3) == cmaps.colors(
        "blues", palette="material", n=3)
    assert cmaps.colors("reds", start=0, end=0, n=2) == ["#ffffff"] * 2


@pytest.mark.parametrize("kwargs, error", [
    (dict(name="Spectrall"), ValueError),
    (dict(name=5), TypeError),
    (dict(name="greens", n=0), ValueError),
    (dict(name="greens", n=2.5), TypeError),
    (dict(name="greens", n=True), TypeError),
    (dict(name="greens", start=-1), ValueError),
    (dict(name="greens", end=101), ValueError),
    (dict(name="greens", start="10"), TypeError),
    (dict(name="greens", palette=3), TypeError),
    (dict(name="greens", palette="unknown"), ValueError),
])
def test_invalid_inputs(kwargs, error):
    name = kwargs.pop("name")
    with pytest.raises(error):
        cmaps.colors(name, **kwargs)


def test_suggestions():
    with pytest.raises(ValueError, match="Spectral"):
        cmaps.colors("Spectrall")


def test_without_matplotlib(monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib", None)
    monkeypatch.setitem(sys.modules, "matplotlib.colors", None)
    assert len(cmaps.colors("greens")) == 10
    with pytest.raises(ImportError, match="SecretColors\\[matplotlib\\]"):
        cmaps.cmap("greens")
    with pytest.raises(ImportError, match="SecretColors\\[matplotlib\\]"):
        cmaps.register()
    with pytest.raises(ImportError):
        cmaps.ColorMap().greens()


class TestMatplotlib:
    matplotlib = pytest.importorskip("matplotlib")

    def test_cmap_types(self):
        colors = self.matplotlib.colors
        greens = cmaps.cmap("greens")
        assert isinstance(greens, colors.LinearSegmentedColormap)
        assert greens.name == "sc.greens"
        assert isinstance(cmaps.cmap("Set2"), colors.ListedColormap)
        assert isinstance(cmaps.cmap("Set2", discrete=False),
                          colors.LinearSegmentedColormap)
        assert cmaps.cmap("greens", n=5, discrete=True).N == 5
        assert cmaps.cmap("RdBu", reverse=True).name == "sc.RdBu_r"

    def test_cmap_colors(self):
        to_hex = self.matplotlib.colors.to_hex
        m = cmaps.cmap("Spectral", n=5)
        assert to_hex(m(0.0)) == "#d7191c"
        assert to_hex(m(1.0)) == "#2b83ba"
        r = cmaps.cmap("Spectral", n=5, reverse=True)
        assert to_hex(r(0.0)) == "#2b83ba"
        listed = cmaps.cmap("Set1", n=3)
        assert [to_hex(c) for c in listed.colors] == cmaps.colors("Set1",
                                                                   n=3)

    def test_single_color(self):
        assert cmaps.cmap("Set1", n=1).N == 1
        with pytest.raises(ValueError):
            cmaps.cmap("Set1", n=1, discrete=False)

    def test_register(self):
        registry = self.matplotlib.colormaps
        prefix = "sc_test"
        try:
            names = cmaps.register(prefix)
            assert len(names) == 2 * len(cmaps.available())
            assert f"{prefix}.greens" in registry
            assert f"{prefix}.Spectral_r" in registry
            assert isinstance(registry[f"{prefix}.Set1"],
                              self.matplotlib.colors.ListedColormap)
            assert cmaps.register(prefix) == []
            assert len(cmaps.register(prefix, force=True)) == len(names)
            to_hex = self.matplotlib.colors.to_hex
            assert to_hex(registry[f"{prefix}.Spectral"](0.0)) == "#9e0142"
            assert to_hex(registry[f"{prefix}.Spectral_r"](0.0)) == "#5e4fa2"
        finally:
            for name in list(registry):
                if name.startswith(f"{prefix}."):
                    registry.unregister(name)

    def test_register_with_palette(self):
        registry = self.matplotlib.colormaps
        prefix = "sc_material"
        try:
            cmaps.register(prefix, palette="material")
            to_hex = self.matplotlib.colors.to_hex
            assert to_hex(registry[f"{prefix}.greens"](1.0)) == cmaps.colors(
                "greens", palette="material")[-1]
        finally:
            for name in list(registry):
                if name.startswith(f"{prefix}."):
                    registry.unregister(name)

    @pytest.mark.parametrize("prefix", ["", "  ", None, 5])
    def test_register_invalid_prefix(self, prefix):
        with pytest.raises(ValueError):
            cmaps.register(prefix)

    def test_used_by_name(self):
        plt = pytest.importorskip("matplotlib.pyplot")
        registry = self.matplotlib.colormaps
        try:
            cmaps.register("sc_plot")
            fig, ax = plt.subplots()
            image = ax.imshow([[0, 1], [2, 3]], cmap="sc_plot.greens")
            assert image.get_cmap().name == "sc_plot.greens"
            plt.close(fig)
        finally:
            for name in list(registry):
                if name.startswith("sc_plot."):
                    registry.unregister(name)


def test_qualitative_types_cover_data():
    types = {data.get("type") for _, data in _SPECIAL.values()}
    assert types <= _QUALITATIVE | {"seq", "div"}


def test_name_resolution_order():
    assert cmaps.colors("Green") != cmaps.colors("green")
    assert len(cmaps.colors("Green")) == 7
    assert cmaps.colors("orange", n=3) == cmaps.colors("oranges", n=3)
    assert cmaps.colors("aquared") == cmaps.colors("AquaRed")
    assert cmaps.colors("TOL_SUNSET") == cmaps.colors("tol_sunset")


def test_interpolation_space():
    assert cmaps.colors("Spectral", n=5, space="lab") == \
        cmaps.colors("Spectral", n=5)
    assert cmaps.colors("Spectral", n=20, space="lab") != \
        cmaps.colors("Spectral", n=20)
    assert len(cmaps.colors("RdBu", n=7, space="lch")) == 7
    with pytest.raises(ValueError):
        cmaps.colors("RdBu", space="hsv")


def test_cmap_space():
    matplotlib = pytest.importorskip("matplotlib")
    to_hex = matplotlib.colors.to_hex
    m = cmaps.cmap("RdBu", space="lab")
    assert m.N == 256
    assert to_hex(m(0.0)) == cmaps.colors("RdBu")[0]
    assert to_hex(m(1.0)) == cmaps.colors("RdBu")[-1]
