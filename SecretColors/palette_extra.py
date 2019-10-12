#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#
#
#  Library Name: SecretColors_old
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
# All palette related things will go here

import random

import numpy as np

from SecretColors._colors import *
from SecretColors._constants import TYPE_GRAY
from SecretColors._helpers import Log
from SecretColors.utils import *


class Palette:
    def __init__(self, name=PALETTE_IBM,
                 color_mode=MODE_HEX
                 ):
        self._name = name
        self._log = Log()
        self._raw_palette = None
        self._all_palettes_colors = None

        self.color_mode = color_mode

    def send(self, *args):
        print(args)
        return args

    def _process_alpha(self, alpha, values):
        if values is None:
            return []
        # TODO
        print(values)
        return values

    @property
    def _all_raw_colors(self):
        if self._all_palettes_colors is None:
            names = []
            for p in ALL_PALETTES:
                names.extend(self._get_raw_palette(p).colors.values())
            self._all_palettes_colors = {x.name: x for x in names}
        return self._all_palettes_colors

    @property
    def _palette(self):
        if self._raw_palette is None:
            self._raw_palette = self._get_raw_palette(self._name)
            self._log.info("'{}' selected as a current palette in the '{}' "
                           "mode".format(self._raw_palette.name,
                                         self.color_mode))
        return self._raw_palette

    def _get_raw_palette(self, name: str):
        """
        :param name: Name of the color palette
        :return: respective palette class
        """
        if name == PALETTE_IBM:
            return IBMPalette(self._log)
        elif name == PALETTE_MATERIAL:
            return MaterialPalette(self._log)
        elif name == PALETTE_BREWER:
            return ColorBrewer(self._log)
        elif name == PALETTE_CLARITY:
            return ClarityPalette(self._log)
        else:
            self._log.error(
                "Invalid Color Palette. Available Palettes are: {}".format(
                    ALL_PALETTES))

    def _get_color(self, name: str):
        if name.strip().lower() not in self._all_raw_colors.keys():
            self._log.error(
                "{} not found in any of the palettes.".format(name))

        c = self._palette.get_color(name)
        if c is not None:
            return c
        else:
            self._log.warn("Color '{}' not found in current palette, "
                           "assigning it from other palettes".format(name))
            return self._all_raw_colors[name.strip().lower()]

    def _check_limit(self, include_start, include_end, include_both):
        if include_both:
            self._log.info("'include_both' option will ignore "
                           "'include_start' and 'include_end'")
            return True, True

        if not include_both and include_both is not None:
            self._log.info("'include_both' option will ignore "
                           "'include_start' and 'include_end'")
            return False, False

        if include_start is None:
            include_start = False

        if include_end is None:
            include_end = False

        return include_start, include_end

    def _adjust_limits(self,
                       no_of_colors,
                       starting_shade,
                       end_shade,
                       include_start,
                       include_end,
                       include_both):

        start, end = self._check_limit(include_start, include_end,
                                       include_both)

        if all([start, end]):
            return np.linspace(starting_shade, end_shade, no_of_colors)

        sd = np.linspace(starting_shade, end_shade, no_of_colors + 2)

        if not start and not end:
            sd = sd[1:-1]
        elif not start and end:
            sd = sd[2:]
        elif start and not end:
            sd = sd[:-2]
        return sd

    def _get_hex(self,
                 name,
                 no_of_colors: int = 1,
                 shade: float = None,
                 starting_shade: float = 0,
                 end_shade: float = 100,
                 include_start: bool = None,
                 include_end: bool = None,
                 include_both: bool = None):

        # If number of colors requested zero, send blank
        if no_of_colors == 0:
            return None

        if starting_shade > end_shade:
            self._log.warn("Starting shade is greater than ending shade. "
                           "Result might be reversed.")

        c = self._get_color(name)

        if no_of_colors == 1:
            if shade is None:
                self._log.info("No shade is specified for '{}'. core shade "
                               "will be returned".format(name))
                return c.core(self._palette.normalized_core_shade)
            else:
                return c.get(shade)

        # If no of colors are greater than 1, ignore shades and generate new
        sd = self._adjust_limits(no_of_colors, starting_shade, end_shade,
                                 include_start, include_end, include_both)

        return [c.get(x) for x in sd]

    def _random_hex(self,
                    no_of_colors: int = 1,
                    shade: float = None,
                    starting_shade: float = 0,
                    end_shade: float = 100,
                    alpha: float = 1,
                    ignore_gray: bool = False):

        if no_of_colors == 0:
            return None

        possible_colors = []
        for c in self._palette.colors.keys():
            if not ignore_gray or c.type != TYPE_GRAY:
                possible_colors.append(c)

        temp = []
        for x in range(no_of_colors):
            c = random.sample(possible_colors, 1)[0]
            if shade is None:
                shade = np.random.uniform(starting_shade, end_shade, 1)[0]

            temp.append(self._get_hex(c, shade=shade))

        self._log.info("Following random colors are generated {}".format(temp))

        if len(temp) == 1:
            return temp[0]

        return temp

    def random(self,
               no_of_colors: int = 1,
               shade: float = None,
               starting_shade: float = 0,
               end_shade: float = 100,
               alpha: float = 1,
               ignore_gray: bool = False,
               print_colors: bool = False):

        c = self._random_hex(no_of_colors, shade, starting_shade,
                             end_shade, alpha, ignore_gray)
        if print_colors:
            print("Random Colors: {}".format(c))

        return self._process_alpha(alpha, c)

    def random_gradient(self,
                        no_of_colors: int = 3,
                        shade: float = None,
                        starting_shade: float = 0,
                        end_shade: float = 100,
                        alpha: float = 1,
                        ignore_gray: bool = False,
                        print_colors: bool = False,
                        complementary=True):

        if no_of_colors < 2:
            return self.random(no_of_colors, shade, starting_shade,
                               end_shade, alpha, ignore_gray, print_colors)

        r1 = self._random_hex(1, shade, starting_shade, end_shade, alpha,
                              ignore_gray)

        r2 = get_complementary(r1)

        if not complementary:
            r2 = self._random_hex(1, shade, starting_shade, end_shade, alpha,
                                  ignore_gray)

        if no_of_colors == 2:
            if print_colors:
                print("Random Colors : {}".format([r1, r2]))
            return self._process_alpha(alpha, [r1, r2])

        temp = [r1]
        temp.extend(color_in_between(r1, r2, no_of_colors - 2))
        temp.append(r2)

        if print_colors:
            print("Random Colors : {}".format(temp))

        return self._process_alpha(alpha, temp)

    def color_between(self,
                      hex1: str, hex2: str,
                      no_of_colors: int = 1,
                      include_start: bool = None,
                      include_end: bool = None,
                      include_both: bool = None,
                      alpha: float = 1,
                      print_colors: bool = False):
        pass

    def test(self):
        import matplotlib.pyplot as plt
        c1 = self._get_hex("blue")
        h, s, l = hex_to_hsl(c1)

        print(h * 360, s, l)

        plt.bar(0, 1, color=hsl_to_hex(h, s, l))
        plt.bar(1, 1, color=hsl_to_hex(h + 0.1, s, l))
        plt.bar(2, 1, color=hsl_to_hex(h + 0.2, s, l))

        plt.show()


def run():
    p = Palette()
    p.test()
