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
from typing import Tuple
from SecretColors.helpers.rxutils import convert_rgb_to_xyz, convert_xyz_to_rgb


def _validate(*args):
    for a in args:
        if a > 1:
            raise ValueError(
                "Color Values can not be greater than 1. "
                "please convert them to 0-1 scale")
        if a < 0:
            raise ValueError("Color values can not be negative")


def _validate255(*args):
    for a in args:
        if not isinstance(a, int):
            raise ValueError(f"Only integers {int} are allowed for conversion "
                             f"between RGB255 and others. Your have provided "
                             f"'{a}' which is {type(a)}")

        if a < 0 or a > 255:
            raise ValueError(f"Value should be between 0 to 255 for "
                             f"conversion from RGB255 to other classes. You "
                             f"have provided '{a}'")


def _sanitize_hex(hex_string: str):
    hex_string = hex_string.strip().lower()
    if hex_string.startswith("#"):
        hex_string = hex_string[1:]

    if len(hex_string) == 3:
        hex_string = "{0}{0}{1}{1}{2}{2}".format(*hex_string)
    if len(hex_string) % 2 != 0 or len(hex_string) < 6:
        raise ValueError(f"Invalid Hex code '{hex_string}' for conversion")

    if len(hex_string) > 8:
        raise ValueError("Hex code can by maximum 8 character long including "
                         "alpha channel")

    return hex_string


def rgb_to_cmy(r, g, b) -> tuple:
    """
    Converts RGB to CMY (both between 0-1)

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Cyan, Magenta, Yellow
    """
    _validate(r, g, b)
    return 1 - r, 1 - g, 1 - b


def cmy_to_rgb(c, m, y) -> tuple:
    """
    Converts CMY to RGB (both between 0-1)

    :param c: Cyan
    :param m: Magenta
    :param y: Yellow
    :return: Red, Green, Blue
    """
    _validate(c, m, y)
    return 1 - c, 1 - m, 1 - y


def cmy_to_cmyk(c, m, y) -> tuple:
    """
    Converts CMY to CMYK (both between 0-1)

    :param c: Cyan
    :param m: Magenta
    :param y: Yellow
    :return: Cyan, Magenta, Yellow, Black
    """
    _validate(c, m, y)
    b = min(c, m, y)
    c2 = (c - b) / (1 - b)
    m2 = (m - b) / (1 - b)
    y2 = (y - b) / (1 - b)
    return c2, m2, y2, b


def cmyk_to_cmy(c, m, y, k):
    """
    Converts CMYK to CMY (both between 0-1)

    :param c: Cyan
    :param m: Magenta
    :param y: Yellow
    :param k: Black
    :return: Cyan, Magenta, Black
    """
    _validate(c, m, y, k)
    c2 = min(1, c * (1 - k) + k)
    m2 = min(1, m * (1 - k) + k)
    y2 = min(1, y * (1 - k) + k)
    return c2, m2, y2


def rgb_to_hsv(r, g, b):
    """
    Converts RGB to HSV

    Hue will be normalized and will be on the scale of 0-1 than 0-360
    Conversion formula is taken from
    https://www.rapidtables.com/convert/color/rgb-to-hsv.html

    :param r: Red (0 to 1)
    :param g: Green (0 to 1)
    :param b: Blue (0 to 1)
    :return: (Hue, Saturation, Lightness) on the scale of (0 to 1)
    """

    _validate(r, g, b)
    v_min = min(r, g, b)
    v_max = max(r, g, b)

    diff = v_max - v_min

    if diff == 0:
        h = 0
    elif v_max == r:
        h = ((g - b) / diff) % 6
    elif v_max == g:
        h = ((b - r) / diff) + 2
    elif v_max == b:
        h = ((r - g) / diff) + 4
    else:
        raise Exception("Something went wrong in converting HSV to RGB")

    h = h * 60  # H in 0-360 range
    h = h / 360  # H in 0-1 range

    if v_max == 0:
        s = 0
    else:
        s = diff / v_max

    v = v_max
    return h, s, v


def hsv_to_rgb(h, s, v) -> tuple:
    """
    Converts HSV to RGB (both between 0-1)

    Conversion calculation from:
    https://www.rapidtables.com/convert/color/hsv-to-rgb.html

    :param h: Hue
    :param s: Saturation
    :param v: Value
    :return: Red, Green, Blue
    """
    _validate(h, s, v)
    h = h * 360  # Convert to angle

    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c

    def __adjust(p, q, r):
        return p + m, q + m, r + m

    if 0 <= h < 60:
        return __adjust(c, x, 0)
    elif 60 <= h < 120:
        return __adjust(x, c, 0)
    elif 120 <= h < 180:
        return __adjust(0, c, x)
    elif 180 <= h < 240:
        return __adjust(0, x, c)
    elif 240 <= h < 300:
        return __adjust(x, 0, c)
    elif 300 <= h < 360:
        return __adjust(c, 0, x)
    else:
        raise Exception("Something went wrong in converting HSV to RGB")


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


def rgb_to_rgb255(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    Converts 0-1 based RGB into 0-255 based RGB

    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :return: Red, Green, Blue (between 0-255)
    """
    _validate(r, g, b)
    # Here rounding is important as `int` will not consider reminder for
    # rounding up to nearest neighbour
    r = int(round(r * 255))
    g = int(round(g * 255))
    b = int(round(b * 255))
    return r, g, b


def rgb255_to_hex(r: int, g: int, b: int) -> str:
    """
    Converts 0-255 based RGB to Hex

    :param r: Red (between 0-255)
    :param g: Green (between 0-255)
    :param b: Blue (between 0-255)
    :return: Hex color code
    """
    _validate255(r, g, b)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rgb_to_hex(r: float, g: float, b: float) -> str:
    _validate(r, g, b)
    return rgb255_to_hex(*rgb_to_rgb255(r, g, b))


def rgb255_to_rgb(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Converts 0-255 based RGB to 0-1 based RGB

    :param r: Red (between 0-255)
    :param g: Green (between 0-255)
    :param b: Blue (between 0-255)
    :return: Red, Green, Blue (between 0-1)
    """
    _validate255(r, g, b)
    return r / 255, g / 255, b / 255


def rgb255_to_hsv(r: int, g: int, b: int):
    """
    Converts 0-255 based RGB to HSV (0-1 based)

    :param r: Red (between 0-255)
    :param g: Green (between 0-255)
    :param b: Blue (between 0-255)
    :return: Hue, Saturation, Value (0-1 based)
    """
    _validate255(r, g, b)
    return rgb_to_hsv(*rgb255_to_rgb(r, g, b))


def rgb255_to_hsl(r: int, g: int, b: int):
    """
    Converts 0-255 based RGB to HSL (0-1 based)

    :param r: Red (between 0-255)
    :param g: Green (between 0-255)
    :param b: Blue (between 0-255)
    :return: Hue, Saturation, Lightness (0-1 based)
    """
    _validate255(r, g, b)
    return rgb_to_hsl(*rgb255_to_rgb(r, g, b))


def hex_to_rgb(hex_string: str):
    """
    Converts Hex to RGB (0-1)

    :param hex_string: Hex string
    :return: Red, Green, Blue (between 0-1)
    """
    hex_string = _sanitize_hex(hex_string)
    c = []
    for x in range(0, len(hex_string), 2):
        try:
            c.append(int(hex_string[x: x + 2], 16) / 255)
        except ValueError:
            raise ValueError(f"{hex_string} is an invalid hex color") from None
    return tuple(c)


def rgb_to_hsb(r, g, b):
    """
    Converts RGB to HSB (both between 1-0)

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Hue, Saturation, Brightness (between 0-1)
    """
    return rgb_to_hsv(r, g, b)


def hsb_to_rgb(h, s, b):
    """
    Converts HSB to RGB (both between 0-1)

    :param h: Hue
    :param s: Saturation
    :param b: Brightness
    :return: Red, Green, Blue (between 0-1)
    """
    return hsv_to_rgb(h, s, b)


def apply_gamma_transform(value):
    """
    Transforms values from linear scale to non-linea by applying gamma
    transform.

    :param value: Values to be transformed
    :return: Transformed values
    """
    if value > 0.0031308:
        return (pow(1.055 * value, (1 / 2.4))) - 0.055
    else:
        return 12.92 * value


def apply_linear_transform(value):
    """
    Transforms value from non-linear scale (with gamma transform) to linear

    :param value: Value to be transform (between 0-1)
    :return: Transformed value (between 0-1)
    """

    if value > 0.04045:
        return pow(((value + 0.055) / 1.055), 2.4)
    else:
        return value / 12.92


def rgb_to_srgb(r, g, b):
    """
    Converts RGB to sRGB

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: sRed, sGreen, sBlue
    """
    _validate(r, g, b)
    return (apply_linear_transform(r),
            apply_linear_transform(g),
            apply_linear_transform(b))


def srgb_to_rgb(sr, sg, sb):
    """
    Converts sRGB to RGB

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param sr: sRed
    :param sg: sGreen
    :param sb: sBlue
    :return: Red, Green, Blue
    """
    return (apply_gamma_transform(sr),
            apply_gamma_transform(sg),
            apply_gamma_transform(sb))


def rgb_to_xyz(r, g, b, *, reference="D65", clip=True):
    """
    Converts Linear-RGB (0-1) to CIE-XYZ

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param r: Red
    :param g: Green
    :param b: Blue
    :param reference: White reference (default: D65)
    :param clip: If True, values below 0 and above 1 will be clipped
    :return: CIE-X, CIE-Y, CIE-Z
    """
    return convert_rgb_to_xyz(r, g, b, space="srgb",
                              reference=reference, clip=clip)


def xyz_to_rgb(x, y, z, *, reference="D65", clip=True):
    """
    Converts CIE-XYZ to Linear-RGB (0-1)

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param x: CIE-X
    :param y: CIE-Y
    :param z: CIE-Z
    :param reference: White reference (default: D65)
    :param clip: If True, values below 0 and above 1 will be clipped
    :return: Red, Green Blue
    """
    return convert_xyz_to_rgb(x, y, z, space="srgb",
                              reference=reference, clip=clip)


def adobe_rgb_to_xyz(r, g, b, *, reference="D65", clip=True):
    """
     Converts adobe-RGB to CIE-XYZ


    Note: This function is still in beta-testing. Do not use in your
    production code.

     :param r: adobe-Red
     :param g: adobe-Green
     :param b: adobe-Blue
     :param reference: White reference (default: D65)
     :param clip: If True, values above 1 and below 0 will be clipped
     :return: CIE-X, CIE-Y, CIE-Z
     """
    return convert_rgb_to_xyz(r, g, b, space="adobe",
                              reference=reference, clip=clip)


def xyz_to_adobe_rgb(x, y, z, *, reference="D65", clip=True):
    """
    Converts CIE-XYZ to adobe-RGB

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param x: CIE-X
    :param y: CIE-Y
    :param z: CIE-Z
    :param reference: White reference (default: D65)
    :param clip: If True, values below 0 and above 1 will be clipped
    :return: adobe-Red, adobe-Green adobe-Blue
    """
    return convert_xyz_to_rgb(x, y, z, space="adobe",
                              reference=reference, clip=clip)


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
    """
    Converts HEX to HSL (0-1)

    :param hex_string: Hex String
    :return: Heu, Saturation, Lightness (between 0-1)
    """
    return rgb_to_hsl(*hex_to_rgb(hex_string))


def hsl_to_hex(h, s, l):
    """
    Converts HSL (between 0-1) into Hex string

    :param h: Hue
    :param s: Saturation
    :param l: Lightness
    :return: Hex String
    """
    return rgb_to_hex(*hsl_to_rgb(h, s, l))


def get_complementary(hex_color: str):
    """
    Returns complementary color

    >>> get_complementary("#fb4b53") # '#4afaf3'

    :param hex_color: Hex color
    :return: Complementary Hex color
    """

    r, g, b = hex_to_rgb(hex_color)
    k = max([r, g, b]) + min([r, g, b])
    t = tuple(k - u for u in (r, g, b))
    return rgb_to_hex(t[0], t[1], t[2])


def simulate_green_blindness(r, g, b):
    """
    Adjust RGB values such that it can 'simulate' Green blindness

    Conversion formula taken from
    https://personal.sron.nl/~pault/#sec:colour_blindness

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Red, Green, Blue (seen by Green-Blind person)
    """
    _validate(r, g, b)

    r2, g2, b2 = rgb_to_rgb255(*rgb_to_srgb(r, g, b))

    r = pow((4211 + pow(g2 * 0.677, 2.2) + pow(r2 * 0.2802, 2.2)), 1 / 2.2)
    g = pow((4211 + pow(g2 * 0.677, 2.2) + pow(r2 * 0.2802, 2.2)), 1 / 2.2)
    b = pow((4211 +
             pow(b2 * 0.95724, 2.2) +
             pow(g2 * 0.02138, 2.2) -
             pow(r2 * 0.02138, 2.2)), 1 / 2.2)

    r2, g2, b2 = rgb255_to_rgb(int(round(r)), int(round(g)), int(round(b)))
    return srgb_to_rgb(r2, g2, b2)


def simulate_red_blindness(r, g, b):
    """
    Adjust RGB values such that it can 'simulate' Red blindness

    Conversion formula taken from
    https://personal.sron.nl/~pault/#sec:colour_blindness

    Note: This function is still in beta-testing. Do not use in your
    production code.

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Red, Green, Blue (seen by Red-Blind person)
    """
    _validate(r, g, b)

    r2, g2, b2 = rgb_to_rgb255(*rgb_to_srgb(r, g, b))
    r = pow((782.7 + pow(g2 * 0.8806, 2.2) + pow(r2 * 0.1115, 2.2)), 1 / 2.2)
    g = pow((782.7 + pow(g2 * 0.8806, 2.2) + pow(r2 * 0.1115, 2.2)), 1 / 2.2)
    b = pow((782.7 +
             pow(b2 * 0.992052, 2.2) -
             pow(g2 * 0.003974, 2.2) +
             pow(r2 * 0.003974, 2.2)), 1 / 2.2)
    r2, g2, b2 = rgb255_to_rgb(int(round(r)), int(round(g)), int(round(b)))
    return srgb_to_rgb(r2, g2, b2)


def run():
    r, g, b = 0.9339861535887517, 0.8860409576833747, 0.9749859185188849
    xyz = rgb_to_xyz(r, g, b)
    print(xyz_to_rgb(*xyz))
