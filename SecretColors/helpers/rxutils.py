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


def _get_matrix(name: str, white: str):
    name = name.strip().lower()
    white = white.strip().upper()
    if name not in RX_DATA.keys():
        raise AttributeError(f"'{name}' is not available in our current RGB "
                             f"conversion tables. Available RGB options are "
                             f"{list(RX_DATA.keys())}")
    if white not in RX_DATA[name].keys():
        raise AttributeError(f"White reference '{white}' is currently not "
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


def _clip_values(value):
    if value < 0:
        return 0
    elif value > 1:
        return 1
    else:
        return value


def _apply(matrix, values, clip):
    v = 0
    for m, val in zip(matrix, values):
        v += m * val
    if clip:
        return _clip_values(v)
    else:
        return v


def _convert_to_xyz(r, g, b, matrix: dict, clip: bool):
    _validate(r, g, b)
    matrix = matrix["xyz"]
    rgb = [r, g, b]
    x = _apply(matrix["x"], rgb, clip)
    y = _apply(matrix["y"], rgb, clip)
    z = _apply(matrix["z"], rgb, clip)
    return x, y, z


def _convert_to_rgb(x, y, z, matrix: dict, clip: bool):
    _validate(x, y, z)
    matrix = matrix["rgb"]
    xyz = [x, y, z]
    r = _apply(matrix["r"], xyz, clip)
    g = _apply(matrix["g"], xyz, clip)
    b = _apply(matrix["b"], xyz, clip)
    return r, g, b


def convert_rgb_to_xyz(r, g, b, *, space, reference, clip=True):
    """
    Converts given RGB (between 0-1) to CIE-XYZ (between 0-1).
    
    Note: For general purpose use, directly use conversion functions like 
    `srgb_to_xyz`, `adobe_rgb_to_xyz` etc. instead using this function.
    
    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :param space: Name of the specific RGB colorspace
    :param reference: White Illumination Reference (e.g. D65)
    :param clip: If True, values falls outside 0-1 range will be clipped
    :return: CIE-XYZ (0-1 if clip=True)
    """
    return _convert_to_xyz(r, g, b,
                           matrix=_get_matrix(space, reference),
                           clip=clip)


def convert_xyz_to_rgb(x, y, z, *, space, reference, clip=True):
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
