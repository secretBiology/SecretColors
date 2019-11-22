"""
SecretColors 2019
Author: Rohit Suratekar

All base models will go here
"""

import matplotlib.pyplot as plt

from SecretColors.constants import *
from SecretColors.helpers import Log
from SecretColors.utils import *


class MetaData:
    def __init__(self):
        self.name = ""
        self.url = ""
        self.last_update = ""
        self.core_shade = 50
        self.version = 1


class PaletteColor:
    def __init__(self, data, shades, log: Log):
        self.data = data
        self._log = log
        self.name = data["n"]
        self.type = data["t"]

        if len(shades) > len(set(shades)):
            self._log.error("Shades provided for '{}' color contains "
                            "duplicate values. All shades should be "
                            "unique.".format(self.name))

        temp_shades = shades
        temp_values = data["c"]
        temp = zip(temp_shades, temp_values)
        temp = sorted(temp, key=lambda x: x[0])
        temp_shades, temp_values = zip(*temp)

        self._shades = list(temp_shades)
        self._values = list(temp_values)
        self.lightest = temp_values[0]
        self.lightest_shade = temp_shades[0]
        self.darkest = temp_values[-1]
        self.darkest_shade = temp_shades[-1]

        try:
            self.selected = data["s"]
        except KeyError:
            self.selected = None

        self._normalized_colors = None
        self._normalized_shades = None

    @property
    def scaling_factor(self):
        # Do the 'logical normalization'
        # more details on
        # https://weirddata.github.io/2019/06/11/secret-colors-2.html#shades
        return math.pow(10, math.ceil(math.log10(self.darkest_shade)))

    def _process(self):
        n = min(self._shades)
        if n > 0:
            self._shades.insert(0, 0)
            self._values.insert(0, WHITE)
            self._log.info("White is added to normalize the '{}' "
                           "color".format(self.name))
        elif n < 0:
            self._log.error("Shade values should be positive. One or more "
                            "shade values for '{}' are negative."
                            .format(self.name))

        self._shades = [x * 100 / self.scaling_factor for x in self._shades]

        if max(self._shades) < 100:
            self._shades.append(100)
            self._values.append(BLACK)
            self._log.info("Black is added to normalize the '{}' "
                           "color.".format(self.name))

        self._normalized_shades = self._shades
        self._normalized_colors = self._values
        self._log.info("Color '{}' is normalized".format(self.name))

    @property
    def color_list(self) -> list:
        if self._normalized_colors is None:
            self._process()
        return self._normalized_colors

    @property
    def shades(self) -> list:
        if self._normalized_shades is None:
            self._process()
        return self._normalized_shades

    def _calculate(self, shade):
        temp = [x for x in self.shades]
        temp.append(shade)
        temp = sorted(temp)
        i = temp.index(shade)
        c1 = self.color_list[i - 1]
        c2 = self.color_list[i]

        ex_total = self.shades[i] - self.shades[i - 1]
        ex = self.shades[i] - shade
        ex = int(round(100 - (ex * 100 / ex_total)))
        cols = color_in_between(c1, c2, 100)
        return cols[ex]

    def get(self, shade):
        """
        Gets the color shade from given colors and shade list.
        Generates the new color if not found

        Shade will be extracted as described in following blog
        https://weirddata.github.io/2019/06/11/secret-colors-2.html#logic


        :param shade: Shade of the color between 0 to 100
        :return: Hex color
        """

        if shade > 100:
            return BLACK
        elif shade < 0:
            return WHITE
        elif round(shade, 2) in self.shades:
            return self.color_list[self.shades.index(round(shade, 2))]
        else:
            return self._calculate(round(shade, 2))

    def core(self, core_shade):
        if self.selected is None:
            return self.get(core_shade)
        else:
            return self.get(self.selected * 100 / self.scaling_factor)


class AllPaletteColors:

    def __init__(self, log: Log):
        self._log = log
        self._colors = None

    @property
    def meta(self) -> MetaData:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.meta.name

    @property
    def url(self) -> str:
        return self.meta.url

    @property
    def core_shade(self) -> float:
        return self.meta.core_shade

    @property
    def last_update(self) -> str:
        return self.meta.last_update

    @property
    def shades(self) -> list:
        raise NotImplementedError

    @property
    def raw_colors(self) -> list:
        raise NotImplementedError

    @property
    def normalized_core_shade(self):
        factor = math.pow(10, math.ceil(math.log10(max(self.shades))))
        return self.core_shade * 100 / factor

    @property
    def colors(self) -> dict:
        if self._colors is None:
            self._colors = {}
            for c in self.raw_colors:
                model = PaletteColor(c, self.shades, self._log)
                self._colors[model.name] = model
        return self._colors

    def get_color(self, name) -> PaletteColor:
        try:
            return self.colors[name]
        except KeyError:
            self._log.warn("Color '{}' not found in {}.".format(name,
                                                                self.name))
            return None


class Color:
    def __init__(self, base_color, *, mode=None, log: Log = None):
        if log is None:
            log = Log()
        self._log = log
        self.r, self.g, self.b = self._change_mode(base_color, mode)

        self.hue, self.saturation, self.lightness = rgb_to_hsl(self.r,
                                                               self.g,
                                                               self.b)

    def _change_mode(self, base_color, mode):
        if mode is None:
            try:
                return hex_to_rgb(base_color)
            except AttributeError:
                self._log.warn("Assuming RGB color mode")
                return base_color
        elif mode == "rgb":
            return base_color
        elif mode == "hsv":
            return hsl_to_rgb(*base_color)
        else:
            self._log.error(f"Something went wrong with mode {mode}")
        return 0, 0, 0

    def _convert(self, h, s, l):
        raise NotImplementedError

    def saturate(self, percentage: float):
        return self._convert(self.hue,
                             self.saturation * percentage / 100,
                             self.lightness)

    def lighter(self, percentage: float):
        av = (1 - self.lightness) * percentage / 100
        return self._convert(self.hue, self.saturation, self.lightness + av)

    def darker(self, percentage: float):
        av = self.lightness * percentage / 100
        return self._convert(self.hue, self.saturation, self.lightness - av)


class ColorString(Color, str):

    def _convert(self, h, s, l):
        return hsl_to_hex(h, s, l)


class ColorTuple(Color, tuple):

    def _convert(self, h, s, l):
        return hsb_to_rgb(h, s, l)


def run():
    c = ColorString("#ff767c")
    c2 = ColorString("#6ea6ff")
    t = ColorTuple((0.1, 0.6, 1))
    print(type(c))
    plt.bar([0, 1, 2], [1, 1, 1], color=[c.lighter(50), c, c.darker(30)])
    print(type(c) )
    plt.show()
