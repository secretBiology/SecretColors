#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

import matplotlib.pylab as plt


def check_colors(colors):
    if type(colors) == str:
        colors = [colors]

    for i, c in enumerate(colors):
        plt.bar(i, 1, color=c)

    plt.show()
