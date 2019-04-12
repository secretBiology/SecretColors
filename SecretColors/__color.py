"""
SecretColors 2019
Author: Rohit Suratekar

Color and its related classes
"""

import random

from SecretColors.utils import color_in_between


class Shade:
    """
    Class to accommodate shades
    """

    def __init__(self, color: str, value: float, max_shade: float):
        self.hex = color
        self.__value = value
        self.__max_shade = max_shade

    @property
    def value(self):
        return round(self.__value * 100 / self.__max_shade)


class Color:
    """
    Base Color Class
    """

    def __init__(self, data: dict, shades: list, core: int):
        """
        :param data: Dictionary values from __colors.py
        :param shades: List of standard shades
        :param core: Shade of core color (Default Shade)
        """

        self._raw = data
        self.name = data['n'].lower()  # Name
        self.type = data['t'].lower()  # Type
        self.__raw_shade_colors = data['c']
        self.__default_shade_values = shades
        self.__raw_core = core
        max_shade = max(shades)
        self.__default_shades_dict = {}
        for i, s in enumerate(self.__raw_shade_colors):
            x = Shade(s, self.__default_shade_values[i], max_shade)
            self.__default_shades_dict[x.value] = x

    @property
    def shade_slabs(self) -> list:
        """
        :return: Standard normalized shade slabs
        """
        return [round(x * 100 / max(self.__default_shade_values))
                for x in self.__default_shade_values]

    @property
    def core_shade_value(self) -> int:
        """
        :return: Normalized value of core shade
        """
        return round(self.__raw_core * 100 / max(self.__default_shade_values))

    @property
    def default_shades_list(self) -> list:
        """
        :return: List of default shades
        """
        return [x for x in self.__default_shades_dict.values()]

    @property
    def hex(self):
        """
        :return: Hex value of default shade
        """
        try:
            return self.__default_shades_dict[self.core_shade_value].hex
        except KeyError:
            for x in self.__default_shades_dict.values():
                return x.hex

    def __str__(self):
        """
        :return: Hex value of core shade
        """
        return self.hex

    def shade(self, value: float = None) -> str:
        """
        :param value: Shade percentage (min and max is defined in the palette)
        :return: Hex code for given shade
        """
        if value is None:
            return self.__default_shades_dict[self.core_shade_value].hex
        else:
            if value > 100:
                # If value is more than 100, return maximum shade available
                return self.__default_shades_dict[max(self.shade_slabs)].hex
            elif int(value) in self.shade_slabs:
                # If value is available in standard shade slabs, return it
                return self.__default_shades_dict[int(value)].hex
            else:
                for i, s in enumerate(self.shade_slabs):
                    if value > s:
                        cols = color_in_between(
                            self.__default_shades_dict[s].hex,
                            self.__default_shades_dict[
                                self.shade_slabs[i - 1]].hex,
                            101)

                        ind = round((self.shade_slabs[i - 1] - s) * 100 /
                                    self.shade_slabs[i - 1]) - 1
                        return cols[int(ind)]

            # If value is below minimum standard shade, use white as a first
            # color and then calculate the shade

            col2 = color_in_between(
                self.__default_shades_dict[min(self.shade_slabs)].hex,
                "#ffffff", 102)

            ind2 = round((min(self.shade_slabs) - value) * 100 / min(
                self.shade_slabs)) - 1

            return col2[int(ind2) + 1]  # +1 will skip white

    def random_between(self, starting_shade: float, ending_shade: float,
                       no_of_colors: int = 1):
        if starting_shade < 0 or ending_shade > 100:
            raise Exception("Shade value should be between 0 and 100")
        else:
            random_shades = []
            for i in range(no_of_colors):
                random_shades.append(
                    random.uniform(starting_shade, ending_shade))

            return [self.shade(x) for x in random_shades]
