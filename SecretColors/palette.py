#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

import matplotlib.pyplot as plt

from SecretColors.models import ColorWheel, Color
from SecretColors.utils import hsl_to_hex, color_in_between


def see(color_list: list):
    for i, c in enumerate(color_list):
        plt.bar(i, 1, color=c)

    plt.yticks([])
    plt.show()


def text(color, text_color):
    plt.bar(0, 1, color=color)
    plt.text(0, 0.5, "Text", ha="center", color=text_color, size=30)
    plt.show()


def color_be(c1, c2):
    w1 = ColorWheel(c1)
    w2 = ColorWheel(c2)

    h = (w1.hue + w2.hue) / 2
    return hsl_to_hex(1 - h, w1.saturation, w1.lightness)


def run():
    c = 0
