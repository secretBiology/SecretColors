#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# New util functions
#
# Color conversions are borrowed from following article
#
# Ford A and Roberts A, Colour Space Conversions, August 11, 1998(a)
# https://poynton.ca/PDFs/coloureq.pdf
#
# TODO: HSI conversions

import math


def _validate(*args):
    for a in args:
        if a > 1:
            raise Exception(
                "Color Values can not be greater than 1. "
                "please convert them to 0-1 scale")
        if a < 0:
            raise Exception("Color values can not be negative")


def _sanitize_hex(hex_string: str):
    hex_string = hex_string.strip().lower()
    if hex_string.startswith("#"):
        hex_string = hex_string[1:]

    if len(hex_string) == 3:
        hex_string = "{0}{0}{1}{1}{2}{2}".format(*hex_string)

    if len(hex_string) % 2 != 0 or len(hex_string) < 6:
        raise Exception("Invalid Hex code for conversion")

    return hex_string


def rgb_to_cmy(r, g, b) -> tuple:
    _validate(r, g, b)
    return 1 - r, 1 - g, 1 - b


def cmy_to_rgb(c, m, y) -> tuple:
    _validate(c, m, y)
    return 1 - c, 1 - m, 1 - y


def cmy_to_cmyk(c, m, y) -> tuple:
    _validate(c, m, y)
    b = min(c, m, y)
    c2 = (c - b) / (1 - b)
    m2 = (m - b) / (1 - b)
    y2 = (y - b) / (1 - b)
    return c2, m2, y2, b


def cmyk_to_cmy(c, m, y, k):
    _validate(c, m, y, k)
    c2 = min(1, c * (1 - k) + k)
    m2 = min(1, m * (1 - k) + k)
    y2 = min(1, y * (1 - k) + k)
    return c2, m2, y2


def rgb_to_hsv(r, g, b):
    """
    Converts RGB to HSV

    Hue will be normalized and will be on the scale of 0-1 than 0-360
    Conversion is done by Travis Method

    :param r: Red (0 to 1)
    :param g: Green (0 to 1)
    :param b: Blue (0 to 1)
    :return: (Hue, Saturation, Lightness) on the scale of (0 to 1)
    """

    _validate(r, g, b)
    v_min = min(r, g, b)
    v_max = max(r, g, b)

    if v_max == 0:
        return 0, 0, 0

    s = (v_max - v_min) / v_max
    v = v_max

    if s == 0:
        return 0, 0, v

    r2 = (v_max - r) / (v_max - v_min)
    g2 = (v_max - g) / (v_max - v_min)
    b2 = (v_max - b) / (v_max - v_min)

    if v_max == r and v_min == g:
        h = 5 + b2
    elif v_max == r and v_min != g:
        h = 1 - g2
    elif v_max == g and v_min == b:
        h = r2 + 1
    elif v_max == g and v_min != b:
        h = 3 - b2
    elif v_max == r:
        h = 3 + g2
    else:
        h = 5 - r2

    h = h * 60  # H in 0-360 range
    h = h / 360  # H in 0-1 range

    return h, s, v


def hsv_to_rgb(h, s, v) -> tuple:
    _validate(h, s, v)
    h = h * 360  # Convert to angle
    h = h / 60
    primary = math.floor(h)
    secondary = h - primary
    a = (1 - s) * v
    b = (1 - (s * secondary)) * v
    c = (1 - (s * (1 - secondary))) * v
    if primary == 0:
        return v, c, a
    elif primary == 1:
        return b, v, a
    elif primary == 2:
        return a, v, c
    elif primary == 3:
        return a, b, v
    elif primary == 4:
        return c, a, v
    elif primary == 5:
        return v, a, b
    else:
        raise Exception("Something went wrong in conversion")


def rgb_to_hsl(r, g, b) -> tuple:
    """
    Converts RGB tuple into HSL tuple
    Calculations are taken from  http://www.easyrgb.com/en/math.php

    :param r: Red (between 0 to 1)
    :param g: Green (between 0 to 1)
    :param b: Blue (between 0 to 1)
    :return: (hue, saturation, lightness) All between 0 to 1
    """

    _validate(r, g, b)

    min_rgb = min(r, g, b)
    max_rgb = max(r, g, b)
    delta_rgb = max_rgb - min_rgb
    l = (max_rgb + min_rgb) / 2
    if delta_rgb == 0:
        h = 0
        s = 0
    else:
        if l < 0.5:
            s = delta_rgb / (max_rgb + min_rgb)
        else:
            s = delta_rgb / (2 - max_rgb - min_rgb)

        delta_r = (((max_rgb - r) / 6) + (delta_rgb / 2)) / delta_rgb
        delta_g = (((max_rgb - g) / 6) + (delta_rgb / 2)) / delta_rgb
        delta_b = (((max_rgb - b) / 6) + (delta_rgb / 2)) / delta_rgb

        if r == max_rgb:
            h = delta_b - delta_g
        elif g == max_rgb:
            h = (1 / 3) + delta_r - delta_b
        else:
            h = (2 / 3) + delta_g - delta_r

        if h < 0:
            h += 1
        if h > 1:
            h -= 1

    return h, s, l


def hsl_to_rgb(h, s, l) -> tuple:
    """
    Converts HSL values to RGB tuple.
    Calculations are taken from http://www.easyrgb.com/en/math.php

    :param h: Hue (between 0 to 1)
    :param s: Saturation (between 0 to 1)
    :param l: Lightness (between 0 to 1)
    :return: (Red, Green, Blue) between 0 to 1
    """

    _validate(h, s, l)

    def __hue_to_rgb(v1, v2, vh):
        """
        Calculation from http://www.easyrgb.com/en/math.php
        """
        if vh < 0:
            vh += 1
        if vh > 1:
            vh -= 1
        if 6 * vh < 1:
            return v1 + ((v2 - v1) * 6 * vh)
        elif 2 * vh < 1:
            return v2
        elif 3 * vh < 2:
            return v1 + ((v2 - v1) * ((2 / 3) - vh) * 6)
        else:
            return v1

    if s == 0:
        r = l
        g = l
        b = l
    else:
        if l < 0.5:
            var2 = l * (1 + s)
        else:
            var2 = (l + s) - (s * l)

        var1 = (2 * l) - var2

        r = __hue_to_rgb(var1, var2, h + (1 / 3))
        g = __hue_to_rgb(var1, var2, h)
        b = __hue_to_rgb(var1, var2, h - (1 / 3))

    return r, g, b


def rgb_to_hex(r, g, b):
    _validate(r, g, b)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex_string: str):
    hex_string = _sanitize_hex(hex_string)
    c = []
    for x in range(0, len(hex_string), 2):
        c.append(int(hex_string[x: x + 2], 16) / 255)

    return tuple(c)


def rgb_to_hsb(r, g, b):
    return rgb_to_hsv(r, g, b)


def hsb_to_rgb(h, s, b):
    return hsv_to_rgb(h, s, b)


def rgb_to_xyz(r, g, b):
    """
    Convert RGB to XYZ

    X, Y and Z output refer to a D65/2° standard illuminant.
    Taken from
    https://www.easyrgb.com/en/math.php

    :param r: Red (0 to 1)
    :param g: Green (0 to 1)
    :param b: Blue (0 to 1)
    :return: X, Y, Z (on the scale of 0 to 1)
    """
    _validate(r, g, b)

    def _adjust(color):
        if color > 0.04045:
            return pow(((color + 0.055) / 1.055), 2.4)
        else:
            return color / 12.92

    r = _adjust(r)
    g = _adjust(g)
    b = _adjust(b)

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return _adjust_excess(x, y, z)


def _get_raw_rgb(x, y, z):
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570
    return r, g, b


def _adjust_excess(x, y, z):
    if x > 1:
        x = 1
    if y > 1:
        y = 1
    if z > 1:
        z = 1
    return x, y, z


def xyz_to_rgb(x, y, z):
    """
    Convert XYZ into RGB

    X, Y and Z output refer to a D65/2° standard illuminant.
    Taken from
    https://www.easyrgb.com/en/math.php

    :param x: X (0 to 1)
    :param y: Y (0 to 1)
    :param z: Z (0 to 1)
    :return: (Red, Green, Blue) on the scale of 0 to 1
    """
    _validate(x, y, z)

    def _adjust(color):
        if color > 0.0031308:
            return 1.055 * (pow(color, (1 / 2.4))) - 0.055

    r, g, b, = _get_raw_rgb(x, y, z)
    r = _adjust(r)
    g = _adjust(g)
    b = _adjust(b)

    return _adjust_excess(r, g, b)


def xyz_to_adobe_rgb(x, y, z):
    """
    Converts XYZ to Adobe RGB (RGB Adobe 1998)

    X, Y and Z output refer to a D65/2° standard illuminant.

    Taken from
    https://www.easyrgb.com/en/math.php

    :param x:
    :param y:
    :param z:
    :return:
    """
    _validate(x, y, z)
    r, g, b = _get_raw_rgb(x, y, z)
    r = pow(r, 1 / 2.19921875)
    g = pow(g, 1 / 2.19921875)
    b = pow(b, 1 / 2.19921875)
    return _adjust_excess(r, g, b)


def adobe_rgb_to_xyz(r, g, b):
    _validate(r, g, b)

    r = pow(r, 2.19921875)
    g = pow(g, 2.19921875)
    b = pow(b, 2.19921875)

    x = r * 0.57667 + g * 0.18555 + b * 0.18819
    y = r * 0.29738 + g * 0.62735 + b * 0.07527
    z = r * 0.02703 + g * 0.07069 + b * 0.99110

    return _adjust_excess(x, y, z)


def rgb_to_adobe_rgb(r, g, b):
    _validate(r, g, b)
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_adobe_rgb(x, y, z)


def adobe_rgb_to_rgb(r, g, b):
    _validate(r, g, b)
    x, y, z = adobe_rgb_to_xyz(r, g, b)
    return xyz_to_rgb(x, y, z)


def relative_luminance(hex_color: str):
    """
    Relative luminance according to WCAG 2.0 standard
    https://www.w3.org/WAI/GL/wiki/Relative_luminance
    :param hex_color:
    :return:
    """

    def _conv(v):
        if v <= 0.03928:
            return v / 12.92
        else:
            return pow((v + 0.055) / 1.055, 2.4)

    r, g, b = hex_to_rgb(hex_color)

    r = _conv(r)
    g = _conv(g)
    b = _conv(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def text_color(hex_color: str):
    """
    Provides black or white color which can be used for text on given hex
    color background

    According to WCA 2.0 standards
    https://www.w3.org/WAI/GL/wiki/Relative_luminance
    and
    https://medium.muz.li/the-science-of-color-contrast-an-expert-designers-guide-33e84c41d156

    >>> text_color("#ffffff") # '#000000'

    :param hex_color: background color
    :return: proper text color
    """
    rw = relative_luminance("#ffffff")
    rl = relative_luminance(hex_color)
    rb = relative_luminance("#000000")
    white_ratio = (rw + 0.05) / (rl + 0.05)
    black_ratio = (rl + 0.05) / (rb + 0.05)
    if white_ratio > black_ratio:
        return "#ffffff"
    else:
        return "#000000"


def color_in_between(c1, c2, no_of_colors=1) -> list:
    """
    Creates color between two colors in RGB ColorSpace

    >>> color_in_between("#fb4b53", "#408bfc") # ['#9d6aa7']
    >>> color_in_between("#fb4b53", "#408bfc", 3) # ['#cc5a7d', '#9d6aa7', '#6e7ad1']


    :param c1: Hex of first color
    :param c2: Hex of second color
    :param no_of_colors: How many colors in between? [Default :1]
    :return: List of Colors between provided colors in RGB space
    """
    steps = no_of_colors + 1
    all_colors = []
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    rdelta, gdelta, bdelta = (r2 - r1) / steps, (g2 - g1) / steps, (
            b2 - b1) / steps
    for step in range(steps - 1):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        all_colors.append(rgb_to_hex(r1, g1, b1))
    return all_colors


def hex_to_hsl(hex_string):
    return rgb_to_hsl(*hex_to_rgb(hex_string))


def hsl_to_hex(h, s, l):
    return rgb_to_hex(*hsl_to_rgb(h, s, l))


def run():
    a = rgb_to_adobe_rgb(1, 0.5, 0.34)
    print(adobe_rgb_to_rgb(*a))
