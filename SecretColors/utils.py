"""
SecretColors 2019
Author: Rohit Suratekar

Utility functions used in this module.
These can also be used as standalone functions.
"""
import warnings


def _warn(message: str, show_warning: bool = True) -> None:
    """
    Simple function to generate warning
    :param message: Message you want to send
    :param show_warning: If False, warnings will be suppressed
    """
    if show_warning:
        m = message + "\nTo suppress warning use 'show_warning=False' in " \
                      "constructor of the palette"
        ##
        warnings.warn(m)


def __int_to_hex(num: int):
    """
    Converts integer to hex. Automatically rounds of the float
    :param num: Integer to be converted
    :return: Hex string
    """
    return '%02x' % int(num)


def rgb_to_hex(r, g, b):
    """
    Converts RGB tuple to hex. Ignores alpha channel
    All Red, Green, Blue values should be between 0 to 1

    >>> rgb_to_hex(0.251, 0.545, 0.988) # '#408afb'

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: Hex color
    """
    return "#" + __int_to_hex(r * 255) + __int_to_hex(
        g * 255) + __int_to_hex(b * 255)


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Converts hex color to RGB

    >>> hex_to_rgb("#408afb") # (0.251, 0.541, 0.984)

    :param hex_color: Color in Hex
    :return: (Red, Green, Blue) between 0 to 1
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


def hex_to_rgb255(hex_color: str) -> tuple:
    """
    Converts hex color to RGB with 0 to 255 range instead 0 to 1

    >>> hex_to_rgb255("#fb4b53") # (251, 75, 83)

    :param hex_color: Color in Hex
    :return: (Red, Green, Blue) between 0 to 255
    """
    if len(hex_color.replace("#", "")) == 8:
        r, g, b, a = [hex_color.replace("#", "")[i:i + 2] for i in
                      range(0, 8, 2)]

        return round(int(r, 16), 3), round(int(g, 16), 3), round(
            int(b, 16), 3), int(a)
    elif len(hex_color.replace("#", "")) == 6:
        r, g, b = [hex_color.replace("#", "")[i:i + 2] for i in
                   range(0, 6, 2)]

        return round(int(r, 16), 3), round(int(g, 16), 3), round(
            int(b, 16), 3)

    elif len(hex_color.replace("#", "")) == 3:
        r, g, b = [x for x in hex_color.replace("#", "")]
        return round(int(r + r, 16), 3), round(int(g + g, 16), 3), round(
            int(b + b, 16), 3)

    else:
        raise Exception("Invalid Hex Code")


def color_in_between(c1, c2, no_of_colors=1) -> list:
    """
    Creates color between two colors

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


def text_color(hex_color: str):
    """
    Provides black or white color which can be used for text on given hex
    color background

    Taken from:
    https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color

    >>> text_color("#ffffff") # '#000000'

    :param hex_color: background color
    :return: proper text color
    """
    r, g, b = hex_to_rgb(hex_color)
    score = (r * 0.299 + g * 0.587 + b * 0.114)
    return "#000000" if score > 0.729 else "#ffffff"


def rgb_to_hsl(r, g, b) -> tuple:
    """
    Converts RGB tuple into HSL tuple
    Calculations are taken from  http://www.easyrgb.com/en/math.php

    :param r: Red (between 0 to 1)
    :param g: Green (between 0 to 1)
    :param b: Blue (between 0 to 1)
    :return: (hue, saturation, lightness) All between 0 to 1
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


def hsl_to_rgb(h, s, l) -> tuple:
    """
    Converts HSL values to RGB tuple.
    Calculations are taken from http://www.easyrgb.com/en/math.php

    :param h: Hue (between 0 to 1)
    :param s: Saturation (between 0 to 1)
    :param l: Lightness (between 0 to 1)
    :return: (Red, Green, Blue) between 0 to 1
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


def hex_to_hsl(hex_name: str) -> tuple:
    """
    Converts Hex Color to HSL tuple

    :param hex_name: Color code in Hex
    :return: (Hue, Saturation, Lightness) between 0 to 1
    """
    r, g, b = hex_to_rgb(hex_name)
    return rgb_to_hsl(r, g, b)


def hsl_to_hex(h, s, l):
    """
    Converts HSL to Hex

    :param h: Hue (between 0 to 1)
    :param s: Saturation (between 0 to 1)
    :param l: Lightness (between 0 to 1)
    :return: Hex color
    """
    r, g, b = hsl_to_rgb(h, s, l)
    return rgb_to_hex(r, g, b)


def hex_to_ahex(hex_name: str, alpha: float):
    """
    Adds Transparency unit to hex code

    :param hex_name: Color in hex format
    :param alpha: Transparency between 0 to 1
    :return: Hex code with transparency value
    """
    if alpha > 1 or alpha < 0:
        raise Exception("Alpha value should be between 0 and 1")
    if len(hex_name) == 7:
        return "#{}{}".format(__int_to_hex(int(alpha * 255)), hex_name[1:7])
    else:
        raise Exception("Invalid Hex")


def hex_to_hex_a(hex_name: str, alpha: float):
    """
    Adds Transparency unit to hex code

    :param hex_name: Color in hex format
    :param alpha: Transparency between 0 to 1
    :return: Hex code with transparency value
    """
    if alpha > 1 or alpha < 0:
        raise Exception("Alpha value should be between 0 and 1")
    if len(hex_name) == 7:
        return "#{}{}".format(hex_name[1:7], __int_to_hex(int(alpha * 255)))
    else:
        raise Exception("Invalid Hex")


def hex_to_rgba(hex_name: str, alpha: float):
    """
    Hex to RGBA

    :param hex_name: Color in hex format
    :param alpha: Transparency between 0 to 1
    :return: (Red, Green, Blue, Alpha) all between 0 to 1
    """
    if alpha > 1 or alpha < 0:
        raise Exception("Alpha value should be between 0 and 1")
    r, b, g = hex_to_rgb(hex_name)
    return r, g, b, alpha


def hex_to_hsla(hex_name: str, alpha: float):
    """
    Hex to HSLA

    :param hex_name: Color in hex format
    :param alpha: Transparency between 0 to 1
    :return: (Hue, Saturation, Lightness, Alpha) all between 0 to 1
    """
    if alpha > 1 or alpha < 0:
        raise Exception("Alpha value should be between 0 and 1")
    h, s, l = hex_to_hsl(hex_name)
    return h, s, l, alpha
