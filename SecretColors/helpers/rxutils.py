#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  All special RGB to XYZ conversions

from SecretColors.data.rgb_xyz import RX_DATA


def _get_matrix(name: str, white: str = None):
    name = name.strip().lower().replace("-", "_").replace(" ", "_")
    if name not in RX_DATA.keys():
        raise ValueError(f"'{name}' is not available in our current RGB "
                         f"conversion tables. Available RGB options are "
                         f"{list(RX_DATA.keys())}")
    if white is None:
        white = "D65" if "D65" in RX_DATA[name] else next(iter(RX_DATA[name]))
    white = white.strip().upper()
    if white not in RX_DATA[name].keys():
        raise ValueError(f"White reference '{white}' is currently not "
                         f"available for '{name}' RGB. Currently "
                         f"available references are : "
                         f"{list(RX_DATA[name].keys())}")
    return RX_DATA[name][white]


def _validate(*args):
    for a in args:
        if a > 1:
            raise ValueError(
                "Color Values can not be greater than 1. "
                "please convert them to 0-1 scale")
        if a < 0:
            raise ValueError("Color values can not be negative")


def _validate_xyz(*args):
    for a in args:
        if a < 0:
            raise ValueError("CIE-XYZ values can not be negative")


def _clip_values(value):
    if value < 0:
        return 0
    elif value > 1:
        return 1
    else:
        return value


def _apply(matrix, values, clip, upper=True):
    v = sum(m * val for m, val in zip(matrix, values))
    if not clip:
        return v
    if upper:
        return _clip_values(v)
    return max(0, v)


def _convert_to_xyz(r, g, b, matrix: dict, clip: bool):
    _validate(r, g, b)
    matrix = matrix["xyz"]
    rgb = [r, g, b]
    x = _apply(matrix["x"], rgb, clip, upper=False)
    y = _apply(matrix["y"], rgb, clip, upper=False)
    z = _apply(matrix["z"], rgb, clip, upper=False)
    return x, y, z


def _convert_to_rgb(x, y, z, matrix: dict, clip: bool):
    _validate_xyz(x, y, z)
    matrix = matrix["rgb"]
    xyz = [x, y, z]
    r = _apply(matrix["r"], xyz, clip)
    g = _apply(matrix["g"], xyz, clip)
    b = _apply(matrix["b"], xyz, clip)
    return r, g, b


def convert_rgb_to_xyz(r, g, b, *, space, reference=None, clip=True):
    """
    Converts given linear RGB (between 0-1) to CIE-XYZ.
    
    Note: For general purpose use, directly use conversion functions like 
    `srgb_to_xyz`, `adobe_rgb_to_xyz` etc. instead using this function.
    
    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :param space: Name of the specific RGB colorspace
    :param reference: White Illumination Reference (e.g. D65)
    :param clip: If True, negative values will be clipped to 0
    :return: CIE-X, CIE-Y, CIE-Z
    """
    return _convert_to_xyz(r, g, b,
                           matrix=_get_matrix(space, reference),
                           clip=clip)


def convert_xyz_to_rgb(x, y, z, *, space, reference=None, clip=True):
    """
    Converts give XYZ values to RGB (0-1).

    Note: For general purpose use, directly use conversion functions like
    `xyz_to_srgb`, `xyz_to_adobe_rgb` etc. instead using this function.

    :param x: X
    :param y: Y
    :param z: Z
    :param space: Name of the specific RGB colorspace
    :param reference: White Illumination Reference (e.g. D65)
    :param clip: If True, values falls outside 0-1 range will be clipped
    :return: RGB values in given colorspace
    """
    return _convert_to_rgb(x, y, z,
                           matrix=_get_matrix(space, reference),
                           clip=clip)
