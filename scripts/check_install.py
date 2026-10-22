"""Run with an installed, dependency-free wheel using python -I."""

import importlib.util
from importlib import metadata, resources
from pathlib import Path

import SecretColors
from SecretColors import Palette, cmaps, check_colors, distinct_colors
from SecretColors.image import extract_palette

checkout = Path(__file__).resolve().parents[1]
assert not Path(SecretColors.__file__).resolve().is_relative_to(checkout / "SecretColors")
assert SecretColors.__version__ == metadata.version("SecretColors")
assert resources.files("SecretColors").joinpath("py.typed").is_file()
assert importlib.util.find_spec("matplotlib") is None
assert importlib.util.find_spec("PIL") is None
assert Palette().red() == "#fa4d56"
assert len(Palette().sample("blue", 1)) == 1
assert len(cmaps.colors("Spectral", n=5)) == 5
assert len(distinct_colors(3)) == 3
assert not check_colors(["#00000000"]).ok
assert Palette(color_mode="ahex").red(alpha=.5).rgb255 == (250, 77, 86)
for operation, hint in [(lambda: cmaps.cmap("blues"), "SecretColors[matplotlib]"),
                         (lambda: extract_palette("unused.png"), "SecretColors[image]")]:
    try:
        operation()
    except ImportError as exc:
        assert hint in str(exc)
    else:
        raise AssertionError("Optional dependency unexpectedly available")
print("Installed wheel: core API, typing marker and optional-dependency errors verified")
