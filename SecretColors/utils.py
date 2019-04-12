"""
Utility functions used in this module
"""


def __int_to_hex(num: int):
    """
    Converts integer to hex. Automatically rounds of the float
    :param num: Integer to be converted
    :return: Hex string
    """
    return '%02x' % int(num)


def rgb_to_hex(rgb_tuple):
    """
    Converts RGB tuple to hex. Ignores alpha channel
    :param rgb_tuple: RGB tuple .
    :return: Hex color
    """
    return "#" + __int_to_hex(rgb_tuple[0] * 255) + __int_to_hex(
        rgb_tuple[1] * 255) + __int_to_hex(rgb_tuple[2] * 255)


def hex_to_rgb(hex_color: str):
    """
    Converts hex color to RGB
    :param hex_color: Color in Hex
    :return: RGB tuple
    """
    if len(hex_color.replace("#", "")) == 8:
        r, g, b, a = [hex_color.replace("#", "")[i:i + 2] for i in
                      range(0, 8, 2)]

        return round(int(r, 16) / 255, 3), round(int(g, 16) / 255, 3), round(
            int(b, 16) / 255, 3), int(a)
    elif len(hex_color.replace("#", "")) == 6:
        r, g, b = [hex_color.replace("#", "")[i:i + 2] for i in
                   range(0, 6, 2)]

        return round(int(r, 16) / 255, 3), round(int(g, 16) / 255, 3), round(
            int(b, 16) / 255, 3)

    elif len(hex_color.replace("#", "")) == 3:
        r, g, b = [x for x in hex_color.replace("#", "")]
        return round(int(r + r, 16) / 255, 3), round(int(g + g, 16) / 255,
                                                     3), round(
            int(b + b, 16) / 255, 3)

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


def get_complementary(hex_color: str):
    """
    Returns complementary color
    :param hex_color: Hex color
    :return: Complementary Hex color
    """

    r, g, b = hex_to_rgb(hex_color)
    k = max([r, g, b]) + min([r, g, b])
    return rgb_to_hex(tuple(k - u for u in (r, g, b)))


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
    return "#000000" if score > 0.729 else "#ffffff"


def rgb_to_hsl(r, g, b):
    """
    http://www.easyrgb.com/en/math.php
    :param r:
    :param g:
    :param b:
    :return:
    """
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

    return round(h, 3), round(s, 3), round(l, 3)


def __hue_to_rgb(v1, v2, vh):
    """
    http://www.easyrgb.com/en/math.php

    :param v1:
    :param v2:
    :param vh:
    :return:
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


def hsl_to_rgb(h, s, l):
    """
    http://www.easyrgb.com/en/math.php

    :param h:
    :param s:
    :param l:
    :return:
    """
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

    return round(r, 3), round(g, 3), round(b, 3)


def hex_to_hsl(hex_name: str):
    r, g, b = hex_to_rgb(hex_name)
    return rgb_to_hsl(r, g, b)


def hsl_to_hex(h, s, l):
    return rgb_to_hex(hsl_to_rgb(h, s, l))
