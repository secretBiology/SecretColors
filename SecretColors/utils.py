"""
Utility functions used in this module
"""


def int_to_hex(num: int):
    """
    Converts integer to hex. Automatically rounds of the float
    :param num: Integer to be converted
    :return: Hex string
    """
    return hex(int(num)).rstrip("L").lstrip("0x").lstrip("-0x")


def rgb_to_hex(rgb_tuple):
    """
    Converts RGB tuple to hex. Ignores alpha channel
    :param rgb_tuple: RGB tuple .
    :return: Hex color
    """
    if sum(rgb_tuple) > 3:
        return "#" + int_to_hex(rgb_tuple[0]) + int_to_hex(
            rgb_tuple[1]) + \
               int_to_hex(rgb_tuple[2])
    else:
        return "#" + int_to_hex(rgb_tuple[0] * 255) + int_to_hex(
            rgb_tuple[1] * 255) + \
               int_to_hex(rgb_tuple[2] * 255)


def rgb_to_hsv(rgb_tuple):
    import numpy as np
    """
    Code from https://github.com/matplotlib/
    matplotlib/blob/master/lib/matplotlib/_color_data.py
    """
    # make sure it is an ndarray
    rgb_tuple = np.asarray(rgb_tuple)

    # check length of the last dimension, should be _some_ sort of rgb
    if rgb_tuple.shape[-1] != 3:
        raise ValueError("Last dimension of input array must be 3; "
                         "shape {} was found.".format(rgb_tuple.shape))

    in_ndim = rgb_tuple.ndim
    if rgb_tuple.ndim == 1:
        rgb_tuple = np.array(rgb_tuple, ndmin=2)

    # make sure we don't have an int image
    rgb_tuple = rgb_tuple.astype(np.promote_types(rgb_tuple.dtype, np.float32))

    out = np.zeros_like(rgb_tuple)
    arr_max = rgb_tuple.max(-1)
    ipos = arr_max > 0
    delta = rgb_tuple.ptp(-1)
    s = np.zeros_like(delta)
    s[ipos] = delta[ipos] / arr_max[ipos]
    ipos = delta > 0
    # red is max
    idx = (rgb_tuple[..., 0] == arr_max) & ipos
    out[idx, 0] = (rgb_tuple[idx, 1] - rgb_tuple[idx, 2]) / delta[idx]
    # green is max
    idx = (rgb_tuple[..., 1] == arr_max) & ipos
    out[idx, 0] = 2. + (rgb_tuple[idx, 2] - rgb_tuple[idx, 0]) / delta[idx]
    # blue is max
    idx = (rgb_tuple[..., 2] == arr_max) & ipos
    out[idx, 0] = 4. + (rgb_tuple[idx, 0] - rgb_tuple[idx, 1]) / delta[idx]

    out[..., 0] = (out[..., 0] / 6.0) % 1.0
    out[..., 1] = s
    out[..., 2] = arr_max

    if in_ndim == 1:
        out.shape = (3,)

    return out[0], out[1], out[2]


def hex_to_rgb(hex_color: str):
    """
    Converts hex color to RGB
    :param hex_color: Color in Hex
    :return: RGB tuple
    """
    if len(hex_color.replace("#", "")) == 8:
        r, g, b, a = [hex_color.replace("#", "")[i:i + 2] for i in
                      range(0, 8, 2)]

        return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255, int(a)
    elif len(hex_color.replace("#", "")) == 6:
        r, g, b = [hex_color.replace("#", "")[i:i + 2] for i in
                   range(0, 6, 2)]

        return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255
    elif len(hex_color.replace("#", "")) == 3:
        r, g, b = [x for x in hex_color.replace("#", "")]
        return int(r + r, 16) / 255, int(g + g, 16) / 255, int(b + b, 16) / 255

    else:
        raise Exception("Invalid Hex Code")


def color_in_between(c1, c2, steps=2) -> list:
    """
    Creates color between two colors
    :param c1: Hex of first color
    :param c2: Hex of second color
    :param steps: How many divisions in between? (Default :2)
    :return: List of Colors between provided colors in RGB space
    """
    all_colors = []
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    rdelta, gdelta, bdelta = (r2 - r1) / steps, (g2 - g1) / steps, (
            b2 - b1) / steps
    for step in range(steps - 1):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        all_colors.append(rgb_to_hex((r1, g1, b1)))
    return all_colors


def hex_to_hsv(hex_color: str):
    """
    Converts hex to HSV value
    :param hex_color: Hex color
    :return: HSV tuple
    """
    return rgb_to_hsv(hex_to_rgb(hex_color))


def get_complementary(hex_color: str):
    """
    Returns complementary color
    :param hex_color: Hex color
    :return: Complementary Hex color
    """

    def flip_value(val):
        if val < 255 / 2:
            return 255 - val
        else:
            return val - 255

    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex((flip_value(r), flip_value(g), flip_value(b)))


def text_color(hex_color: str):
    """
    Provides black or white color which can be used for text on given hex
    color background

    Taken from:
    https://stackoverflow.com/questions/3942878
    /how-to-decide-font-color-in-white-or-black-depending-on-background-color

    :param hex_color: background color
    :return: proper text color
    """
    r, g, b = hex_to_rgb(hex_color)
    score = (r * 0.299 + g * 0.587 + b * 0.114)
    return "#000000" if score > 186 else "#ffffff"
