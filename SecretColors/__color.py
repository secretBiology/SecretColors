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
        """
        :param color: Name of the color
        :param value: Value of the shade
        :param max_shade: Maximum shade possible in current palette
        """
        self.hex = color
        self.__value = value
        self.__max_shade = max_shade

    @property
    def value(self):
        """
        :return: Normalized shade value
        """
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
        if len(shades) > len(self.__raw_shade_colors):
            for i in range(len(shades) - len(self.__raw_shade_colors)):
                self.__raw_shade_colors.append(self.__raw_shade_colors[-1])

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
        """
        Generates colors between two shades of the current color

        :param starting_shade: Minimum shade (0-100)
        :param ending_shade: Maximum Shade (0-100)
        :param no_of_colors: Number of colors
        :return: Color/List of colors (in Hex)
        """
        if starting_shade < 0 or ending_shade > 100:
            raise Exception("Shade value should be between 0 and 100")
        else:
            random_shades = []
            for i in range(no_of_colors):
                random_shades.append(
                    random.uniform(starting_shade, ending_shade))

            return [self.shade(x) for x in random_shades]

    def gradient(self, starting_shade: float, ending_shade: float,
                 no_of_colors: int = 2, include_first: bool = False,
                 include_last: bool = False,
                 include_both: bool = False) -> list:

        """
        Generates the color gradient

        :param starting_shade: Minimum shade
        :param ending_shade: Maximum Shade
        :param no_of_colors: Number of colors
        :param include_first: If True, starting shade will be included
        :param include_last: If True, end shade will be included
        :param include_both: If True, both starting and ending shade will be
        included in the final list of colors
        :return: List of Colors
        """
        if no_of_colors < 2:
            raise Exception("No of colors should be minimum 2")

        if no_of_colors < 3:
            if include_both or (include_first and include_last):
                return [self.shade(starting_shade), self.shade(ending_shade)]
            elif include_first:
                return [self.shade(starting_shade),
                        self.shade(
                            random.uniform(starting_shade, ending_shade))]
            elif include_last:
                return [self.shade(
                    random.uniform(starting_shade, ending_shade)),
                    self.shade(ending_shade)]

        grad_shades = []
        if include_both or (include_first and include_last):
            step_count = -2
            grad_shades.append(starting_shade)
        elif include_first:
            step_count = -1
            grad_shades.append(starting_shade)
        elif include_last:
            step_count = -1
        else:
            step_count = 0

        step = (ending_shade - starting_shade) / (no_of_colors + step_count + 1)

        for i in range(no_of_colors + step_count):
            if len(grad_shades) > 0:
                grad_shades.append(grad_shades[-1] + step)
            else:
                grad_shades.append(starting_shade + step)

        if include_last or include_both:
            grad_shades.append(ending_shade)

        return [self.shade(x) for x in grad_shades]
