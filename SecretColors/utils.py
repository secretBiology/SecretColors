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
from typing import Sequence, Tuple, Union

from SecretColors.data.rgb_xyz import RX_DATA, WHITE_POINTS
from SecretColors.helpers.decorators import deprecated
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
    if b == 1:
        return 0, 0, 0, 1
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
    h = (h * 360) % 360

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
    else:
        return __adjust(c, 0, x)


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
        return 1.055 * pow(value, 1 / 2.4) - 0.055
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


def srgb_to_linear(r, g, b):
    """
    Converts gamma-encoded sRGB (0-1) to linear RGB (0-1)

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Linear Red, Linear Green, Linear Blue
    """
    _validate(r, g, b)
    return (apply_linear_transform(r),
            apply_linear_transform(g),
            apply_linear_transform(b))


def linear_to_srgb(r, g, b):
    """
    Converts linear RGB (0-1) to gamma-encoded sRGB (0-1)

    :param r: Linear Red
    :param g: Linear Green
    :param b: Linear Blue
    :return: Red, Green, Blue
    """
    _validate(r, g, b)
    return (apply_gamma_transform(r),
            apply_gamma_transform(g),
            apply_gamma_transform(b))


@deprecated("Its name is misleading as it converts sRGB to linear RGB. "
            "Use 'srgb_to_linear' instead.")
def rgb_to_srgb(r, g, b):
    """
    Deprecated alias of :func:`srgb_to_linear`
    """
    return srgb_to_linear(r, g, b)


@deprecated("Its name is misleading as it converts linear RGB to sRGB. "
            "Use 'linear_to_srgb' instead.")
def srgb_to_rgb(sr, sg, sb):
    """
    Deprecated alias of :func:`linear_to_srgb`
    """
    return linear_to_srgb(sr, sg, sb)


def rgb_spaces() -> dict:
    """
    RGB colorspaces available for CIE-XYZ conversions and their white
    references

    >>> rgb_spaces()["pro_photo"] # ['D50']

    :return: Dictionary of colorspace name and list of white references
    """
    return {name: list(refs) for name, refs in RX_DATA.items()}


def rgb_to_xyz(r, g, b, *, space="srgb", reference=None, clip=True):
    """
    Converts linear RGB (0-1) of given RGB colorspace to CIE-XYZ

    >>> rgb_to_xyz(*srgb_to_linear(1, 0, 0))   # sRGB red
    >>> rgb_to_xyz(0.2, 0.5, 0.1, space="pro_photo")

    :param r: Red
    :param g: Green
    :param b: Blue
    :param space: RGB colorspace (see :func:`rgb_spaces`). (default: srgb)
    :param reference: White reference. Default is D65 if available for the
        colorspace, otherwise its native reference.
    :param clip: If True, negative values will be clipped to 0
    :return: CIE-X, CIE-Y, CIE-Z
    """
    return convert_rgb_to_xyz(r, g, b, space=space,
                              reference=reference, clip=clip)



def xyz_to_rgb(x, y, z, *, space="srgb", reference=None, clip=True):
    """
    Converts CIE-XYZ to linear RGB (0-1) of given RGB colorspace

    :param x: CIE-X
    :param y: CIE-Y
    :param z: CIE-Z
    :param space: RGB colorspace (see :func:`rgb_spaces`). (default: srgb)
    :param reference: White reference. Default is D65 if available for the
        colorspace, otherwise its native reference.
    :param clip: If True, values below 0 and above 1 will be clipped
    :return: Red, Green Blue
    """
    return convert_xyz_to_rgb(x, y, z, space=space,
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
     :param clip: If True, negative values will be clipped to 0
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


_LAB_EPSILON = 216 / 24389
_LAB_KAPPA = 24389 / 27


def _white_point(reference: str) -> tuple:
    key = reference.strip().upper()
    if key not in WHITE_POINTS:
        raise ValueError(f"Unknown white reference '{reference}'. Available "
                         f"references: {list(WHITE_POINTS)}")
    return WHITE_POINTS[key]


def xyz_to_lab(x, y, z, *, reference="D65") -> tuple:
    """
    Converts CIE-XYZ to CIE-L*a*b*

    Conversion formula taken from
    http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html

    :param x: CIE-X
    :param y: CIE-Y
    :param z: CIE-Z
    :param reference: White reference (default: D65)
    :return: L* (0-100), a*, b*
    """

    def f(t):
        if t > _LAB_EPSILON:
            return t ** (1 / 3)
        return (_LAB_KAPPA * t + 16) / 116

    xw, yw, zw = _white_point(reference)
    fx, fy, fz = f(x / xw), f(y / yw), f(z / zw)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lab_to_xyz(l, a, b, *, reference="D65") -> tuple:
    """
    Converts CIE-L*a*b* to CIE-XYZ

    Conversion formula taken from
    http://www.brucelindbloom.com/index.html?Eqn_Lab_to_XYZ.html

    :param l: L* (0-100)
    :param a: a*
    :param b: b*
    :param reference: White reference (default: D65)
    :return: CIE-X, CIE-Y, CIE-Z
    """
    xw, yw, zw = _white_point(reference)
    fy = (l + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200
    xr = fx ** 3 if fx ** 3 > _LAB_EPSILON else (116 * fx - 16) / _LAB_KAPPA
    yr = fy ** 3 if l > _LAB_KAPPA * _LAB_EPSILON else l / _LAB_KAPPA
    zr = fz ** 3 if fz ** 3 > _LAB_EPSILON else (116 * fz - 16) / _LAB_KAPPA
    return xr * xw, yr * yw, zr * zw


def rgb_to_lab(r, g, b) -> tuple:
    """
    Converts sRGB (0-1) to CIE-L*a*b* (D65)

    >>> rgb_to_lab(1, 0, 0) # (53.24, 80.09, 67.20)

    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :return: L* (0-100), a*, b*
    """
    return xyz_to_lab(*rgb_to_xyz(*srgb_to_linear(r, g, b), clip=False))


def lab_to_rgb(l, a, b, *, clip=True) -> tuple:
    """
    Converts CIE-L*a*b* (D65) to sRGB (0-1)

    :param l: L* (0-100)
    :param a: a*
    :param b: b*
    :param clip: If True, colors outside sRGB gamut are clipped. Otherwise
        ValueError is raised for such colors.
    :return: Red, Green, Blue (between 0-1)
    """
    x, y, z = lab_to_xyz(l, a, b)
    if clip:
        x, y, z = max(0.0, x), max(0.0, y), max(0.0, z)
    elif min(x, y, z) < 0:
        raise ValueError(f"L*a*b* ({l}, {a}, {b}) is outside sRGB gamut")
    linear = xyz_to_rgb(x, y, z, clip=False)
    if clip:
        linear = tuple(min(1.0, max(0.0, v)) for v in linear)
    elif any(v < -1e-9 or v > 1 + 1e-9 for v in linear):
        raise ValueError(f"L*a*b* ({l}, {a}, {b}) is outside sRGB gamut")
    else:
        linear = tuple(min(1.0, max(0.0, v)) for v in linear)
    return linear_to_srgb(*linear)


def hex_to_lab(hex_color: str) -> tuple:
    """
    Converts Hex to CIE-L*a*b* (D65)

    :param hex_color: Hex color
    :return: L* (0-100), a*, b*
    """
    return rgb_to_lab(*hex_to_rgb(hex_color)[:3])


def lab_to_hex(l, a, b) -> str:
    """
    Converts CIE-L*a*b* (D65) to Hex. Colors outside sRGB gamut are clipped.

    :param l: L* (0-100)
    :param a: a*
    :param b: b*
    :return: Hex color
    """
    return rgb_to_hex(*lab_to_rgb(l, a, b))


def lab_to_lch(l, a, b) -> tuple:
    """
    Converts CIE-L*a*b* to CIE-LCh(ab)

    :param l: L*
    :param a: a*
    :param b: b*
    :return: Lightness, Chroma, Hue (in degrees, 0-360)
    """
    return l, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def lch_to_lab(l, c, h) -> tuple:
    """
    Converts CIE-LCh(ab) to CIE-L*a*b*

    :param l: Lightness
    :param c: Chroma
    :param h: Hue (in degrees)
    :return: L*, a*, b*
    """
    h = math.radians(h)
    return l, c * math.cos(h), c * math.sin(h)


def _as_lab(color) -> tuple:
    if isinstance(color, str):
        return hex_to_lab(color)
    if len(color) != 3:
        raise ValueError(f"Expected hex color or L*a*b* tuple, got {color}")
    return tuple(color)


def _ciede2000(lab1, lab2) -> float:
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c_bar = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(c_bar ** 7 / (c_bar ** 7 + 25 ** 7)))
    a1p, a2p = a1 * (1 + g), a2 * (1 + g)
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if c1p else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if c2p else 0.0

    dl = l2 - l1
    dc = c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    elif abs(h2p - h1p) <= 180:
        dh = h2p - h1p
    elif h2p - h1p > 180:
        dh = h2p - h1p - 360
    else:
        dh = h2p - h1p + 360
    dh_big = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))

    l_bar = (l1 + l2) / 2
    cp_bar = (c1p + c2p) / 2
    if c1p * c2p == 0:
        hp_bar = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hp_bar = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hp_bar = (h1p + h2p + 360) / 2
    else:
        hp_bar = (h1p + h2p - 360) / 2

    t = (1 - 0.17 * math.cos(math.radians(hp_bar - 30))
         + 0.24 * math.cos(math.radians(2 * hp_bar))
         + 0.32 * math.cos(math.radians(3 * hp_bar + 6))
         - 0.20 * math.cos(math.radians(4 * hp_bar - 63)))
    d_theta = 30 * math.exp(-(((hp_bar - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cp_bar ** 7 / (cp_bar ** 7 + 25 ** 7))
    sl = 1 + 0.015 * (l_bar - 50) ** 2 / math.sqrt(20 + (l_bar - 50) ** 2)
    sc = 1 + 0.045 * cp_bar
    sh = 1 + 0.015 * cp_bar * t
    rt = -math.sin(math.radians(2 * d_theta)) * rc
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dh_big / sh) ** 2
                     + rt * (dc / sc) * (dh_big / sh))


def delta_e(color1: Union[str, Sequence[float]],
            color2: Union[str, Sequence[float]], *,
            method: str = "ciede2000") -> float:
    """
    Perceptual difference between two colors. Values below ~2.3 are barely
    noticeable to the human eye.

    >>> delta_e("#fa4d56", "#fa4d57")             # ~0.3
    >>> delta_e("#fa4d56", "#4589ff")             # ~44.5
    >>> delta_e((50, 2.5, 0), (73, 25, -18))      # L*a*b* tuples work too

    :param color1: Hex color or L*a*b* tuple
    :param color2: Hex color or L*a*b* tuple
    :param method: 'ciede2000' (default) or 'cie76'
    :return: Color difference (Delta E)
    """
    lab1, lab2 = _as_lab(color1), _as_lab(color2)
    method = method.strip().lower()
    if method == "cie76":
        return math.dist(lab1, lab2)
    if method == "ciede2000":
        return _ciede2000(lab1, lab2)
    raise ValueError(f"Unknown method '{method}'. Use 'ciede2000' or "
                     f"'cie76'")


def _as_rgb(color) -> tuple:
    if isinstance(color, str):
        return hex_to_rgb(color)[:3]
    if isinstance(color, (tuple, list)) and len(color) in (3, 4):
        _validate(*color[:3])
        return tuple(color[:3])
    raise ValueError(f"Expected hex string or RGB/RGBA tuple (0-1), got "
                     f"{color!r}")


def relative_luminance(color) -> float:
    """
    Relative luminance according to WCAG 2.0 standard
    https://www.w3.org/WAI/GL/wiki/Relative_luminance

    :param color: Hex color or RGB/RGBA tuple (0-1). Alpha is ignored.
    :return: Relative luminance (between 0-1)
    """
    r, g, b = srgb_to_linear(*_as_rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1, color2) -> float:
    """
    WCAG 2.x contrast ratio between two colors. Order of colors does not
    matter.

    https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio

    >>> contrast_ratio("#000000", "#ffffff")   # 21.0 (maximum)
    >>> contrast_ratio("#0f62fe", "#ffffff")   # 5.0

    :param color1: Hex color or RGB/RGBA tuple (0-1)
    :param color2: Hex color or RGB/RGBA tuple (0-1)
    :return: Contrast ratio between 1 and 21
    """
    l1, l2 = sorted((relative_luminance(color1),
                     relative_luminance(color2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


_WCAG_MINIMUM = {("AA", False): 4.5, ("AA", True): 3.0,
                 ("AAA", False): 7.0, ("AAA", True): 4.5}


def is_readable(foreground, background, *, level: str = "AA",
                large_text: bool = False) -> bool:
    """
    Checks if text in `foreground` color is readable on `background`
    according to WCAG 2.x

    ====== =========== ==========
    Level  Normal text Large text
    ====== =========== ==========
    AA     4.5         3.0
    AAA    7.0         4.5
    ====== =========== ==========

    Large text is at least 18pt (24px) or 14pt (~18.7px) bold. A ratio of
    3.0 is also the WCAG minimum for graphics such as plot lines and markers.

    >>> is_readable("#6f6f6f", "#ffffff")              # True
    >>> is_readable("#6f6f6f", "#ffffff", level="AAA") # False

    :param foreground: Text color (hex or RGB tuple)
    :param background: Background color (hex or RGB tuple)
    :param level: 'AA' (default) or 'AAA'
    :param large_text: If True, thresholds for large text are used
    :return: True if contrast is sufficient
    """
    key = (level.strip().upper(), bool(large_text))
    if key not in _WCAG_MINIMUM:
        raise ValueError("'level' should be 'AA' or 'AAA'")
    return contrast_ratio(foreground, background) >= _WCAG_MINIMUM[key]


def text_color(hex_color: str):
    """
    Provides black or white color which can be used for text on given
    background color (whichever has higher WCAG contrast ratio)

    >>> text_color("#ffffff") # '#000000'

    :param hex_color: background color
    :return: proper text color
    """
    if contrast_ratio("#ffffff", hex_color) > contrast_ratio("#000000",
                                                             hex_color):
        return "#ffffff"
    return "#000000"


_SPACES = ("rgb", "lab", "lch")


def _mix(rgb1, rgb2, t: float, space: str) -> tuple:
    if space == "rgb":
        return tuple(a + (b - a) * t for a, b in zip(rgb1, rgb2))
    lab1, lab2 = rgb_to_lab(*rgb1), rgb_to_lab(*rgb2)
    if space == "lab":
        return lab_to_rgb(*(a + (b - a) * t for a, b in zip(lab1, lab2)))
    l1, c1, h1 = lab_to_lch(*lab1)
    l2, c2, h2 = lab_to_lch(*lab2)
    if c1 < 1e-4:
        h1 = h2
    if c2 < 1e-4:
        h2 = h1
    dh = (h2 - h1 + 180) % 360 - 180
    return lab_to_rgb(*lch_to_lab(l1 + (l2 - l1) * t, c1 + (c2 - c1) * t,
                                  h1 + dh * t))


def mix(color1, color2, ratio: float = 0.5, *, space: str = "rgb") -> str:
    """
    Mixes two colors

    >>> mix("#fa4d56", "#4589ff")                  # '#a06bab'
    >>> mix("#fa4d56", "#4589ff", space="lab")     # '#c670a9'
    >>> mix("#fa4d56", "#4589ff", ratio=0.25)      # closer to first color

    :param color1: Hex color or RGB/RGBA tuple (0-1)
    :param color2: Hex color or RGB/RGBA tuple (0-1)
    :param ratio: Amount of `color2` (0 gives `color1`, 1 gives `color2`)
    :param space: Color space used for mixing - 'rgb' (default), 'lab'
        (perceptually uniform) or 'lch' (keeps colors vivid)
    :return: Hex color
    """
    space = _check_space(space)
    if not 0 <= ratio <= 1:
        raise ValueError("'ratio' should be between 0 and 1")
    rgb = _mix(_as_rgb(color1), _as_rgb(color2), ratio, space)
    return rgb_to_hex(*(min(1.0, max(0.0, v)) for v in rgb))


def _check_space(space: str) -> str:
    space = space.strip().lower()
    if space not in _SPACES:
        raise ValueError(f"'space' should be one of {_SPACES}")
    return space


def color_in_between(c1, c2, no_of_colors=1, *, space: str = "rgb") -> list:
    """
    Creates evenly spaced colors between two colors

    >>> color_in_between("#fb4b53", "#408bfc") # ['#9e6ba8']
    >>> color_in_between("#fb4b53", "#408bfc", 3) # ['#cc5b7d', '#9d6ba8', '#6f7bd2']
    >>> color_in_between("#fb4b53", "#408bfc", 3, space="lab") # ['#e4607c', '#c670a6', '#9a7ed0']

    RGB mixing is simple but its middle colors often look dull and grayish.
    'lab' gives perceptually even steps and 'lch' keeps colors vivid by
    going around the color wheel.

    :param c1: Hex of first color
    :param c2: Hex of second color
    :param no_of_colors: How many colors in between? [Default :1]
    :param space: Color space for interpolation - 'rgb' (default), 'lab' or
        'lch'
    :return: List of Colors between provided colors
    """
    space = _check_space(space)
    steps = no_of_colors + 1
    if space != "rgb":
        rgb1, rgb2 = _as_rgb(c1), _as_rgb(c2)
        return [rgb_to_hex(*_mix(rgb1, rgb2, i / steps, space))
                for i in range(1, steps)]
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


def _simulate_dichromacy(r, g, b, offset, red_weight, green_weight,
                         blue_weights):
    _validate(r, g, b)
    r, g, b = (pow(v * 255, 2.2) for v in (r, g, b))
    rg = pow(offset + red_weight * r + green_weight * g, 1 / 2.2)
    bb = offset + blue_weights[0] * b + blue_weights[1] * g + \
        blue_weights[2] * r
    bb = pow(max(0.0, bb), 1 / 2.2)
    rg = min(1.0, rg / 255)
    return rg, rg, min(1.0, bb / 255)


def simulate_green_blindness(r, g, b):
    """
    Adjust RGB values such that it can 'simulate' Green blindness
    (deuteranopia)

    Conversion formula taken from
    https://personal.sron.nl/~pault/#sec:colour_blindness

    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :return: Red, Green, Blue (seen by Green-Blind person)
    """
    return _simulate_dichromacy(r, g, b, 4211, 0.2802, 0.677,
                                (0.95724, 0.02138, -0.02138))


def simulate_red_blindness(r, g, b):
    """
    Adjust RGB values such that it can 'simulate' Red blindness (protanopia)

    Conversion formula taken from
    https://personal.sron.nl/~pault/#sec:colour_blindness

    :param r: Red (between 0-1)
    :param g: Green (between 0-1)
    :param b: Blue (between 0-1)
    :return: Red, Green, Blue (seen by Red-Blind person)
    """
    return _simulate_dichromacy(r, g, b, 782.7, 0.1115, 0.8806,
                                (0.992052, -0.003974, 0.003974))
