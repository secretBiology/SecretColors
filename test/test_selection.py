import pytest

from SecretColors import Palette, check_colors, distinct_colors
from SecretColors.selection import ColorReport
from SecretColors.utils import contrast_ratio, hex_to_lab, lab_to_lch


@pytest.mark.parametrize("palette", ["ibm", "material", "spectrum"])
@pytest.mark.parametrize("n", [2, 4, 6, 8])
def test_distinct_colors_are_distinct(palette, n):
    colors = distinct_colors(n, palette=palette)
    assert len(colors) == n
    assert len(set(colors)) == n
    report = check_colors(colors)
    assert report.ok, str(report)


def test_prefix_is_stable():
    eight = distinct_colors(8)
    for k in range(1, 8):
        assert distinct_colors(k) == eight[:k]


def test_background_contrast():
    for background in ("#ffffff", "#161616", "#0d1117"):
        colors = distinct_colors(5, background=background)
        assert all(contrast_ratio(c, background) >= 3 for c in colors)
        assert check_colors(colors, background=background).ok


def test_varied_hues():
    hues = {int(lab_to_lch(*hex_to_lab(c))[2] // 30)
            for c in distinct_colors(5)}
    assert len(hues) == 5


def test_options():
    own = ["#fa4d56", "#ff832b", "#24a148", "#0f62fe", "#fa4d56"]
    picked = distinct_colors(3, palette=own)
    assert set(picked) <= set(own)
    assert len(distinct_colors(3, palette=Palette("material"))) == 3
    assert len(distinct_colors(5, colorblind_safe=False)) == 5
    assert len(distinct_colors(5, background=None)) == 5
    grays = distinct_colors(30, include_grays=True, shade_range=(10, 100),
                            background=None)
    assert len(grays) == 30


@pytest.mark.parametrize("kwargs, error", [
    (dict(n=0), ValueError),
    (dict(n=2.0), TypeError),
    (dict(n=200), ValueError),
    (dict(n=3, palette=5), TypeError),
    (dict(n=3, palette="unknown"), ValueError),
])
def test_distinct_colors_errors(kwargs, error):
    with pytest.raises(error):
        distinct_colors(**kwargs)


def test_check_colors_red_green():
    report = check_colors(["#fa4d56", "#24a148", "#0f62fe"])
    assert isinstance(report, ColorReport)
    assert report.min_delta_e > 10
    assert report.min_delta_e_deuteranopia < 10
    assert set(report.closest_pair_deuteranopia) == {"#fa4d56", "#24a148"}
    assert not report.colorblind_safe
    assert not report.ok
    text = str(report)
    assert "needs attention" in text and "deuteranopia" in text


def test_check_colors_contrast():
    report = check_colors(["#0f62fe", "#ffeb3b"])
    assert report.low_contrast == ["#ffeb3b"]
    assert "low contrast" in str(report)
    assert check_colors(["#0f62fe", "#ffeb3b"],
                        background=None).low_contrast == []
    assert check_colors([(0.06, 0.38, 1.0)]).colors == ["#0f61ff"]


def test_check_colors_single():
    report = check_colors(["#0f62fe"])
    assert report.min_delta_e == float("inf")
    assert report.closest_pair is None
    assert report.ok
