import random
import warnings

from SecretColors.__colors import *
from SecretColors.utils import *


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


class Palette:

    def __init__(self, name: str = PALETTE_IBM, allow_gray_shades: bool = True,
                 show_warning: bool = True, color_mode: str = MODE_HEX):

        self.__palette = self.__get_palette(name)

        self.__colors = {}
        for c in self.__palette.get_all_colors():
            self.__colors[c.name] = c

        self.__allow_gray = allow_gray_shades
        self._show_warning = show_warning
        self.color_mode = color_mode

    @staticmethod
    def __get_palette(name: str) -> ParentPalette:
        """
        :param name: Name of the color palette
        :return: respective palette class
        """
        if name == PALETTE_IBM:
            return IBMPalette()
        elif name == PALETTE_MATERIAL:
            return MaterialPalette()
        else:
            raise Exception(
                "Invalid Color Palette. Available Palettes are: {}".format(
                    ALL_PALETTES
                ))

    def __all_colors(self) -> dict:
        """
        :return: Dictionary of colors from all palettes
        """
        d = {}
        for p in ALL_PALETTES:
            for c in self.__get_palette(p).get_all_colors():
                d[c.name] = c
        return d

    @property
    def name(self):
        """
        :return: Name of the current palette
        """
        return self.__palette.get_palette_name()

    @property
    def version(self):
        """
        :return: Version of the current palette in THIS library
        """
        return self.__palette.get_version()

    @property
    def creator_url(self):
        """
        :return: URL citing original creator
        """
        return self.__palette.get_creator_url()

    @property
    def standard_colors(self):
        """
        :return: Standard colors from the palette
        """
        d = {}
        for x in self.__colors.values():
            if self.__allow_gray:
                d[x.name] = x.hex
            else:
                if x.type != TYPE_GRAY:
                    d[x.name] = x.hex
        return d

    def __convert(self, hex_name: str):
        if self.color_mode == MODE_HEX:
            return hex_name
        elif self.color_mode == MODE_RGB:
            return hex_to_rgb(hex_name)
        elif self.color_mode == MODE_HSL:
            return hex_to_hsl(hex_name)
        else:
            raise Exception("Invalid Color Mode or this color mode is not "
                            "supported yet")

    def __get_color(self, name: str):
        try:
            return self.__colors[name]
        except KeyError:
            _warn("Current palette do not have this color. Using it from other "
                  "palettes. ", self._show_warning)
            return self.__all_colors()[name]

    @staticmethod
    def __random_pick(color: Color, no_of_colors: int = 1,
                      shade: float = None,
                      starting_shade: float = 0,
                      ending_shade: float = 100):
        if shade is not None and no_of_colors == 1:
            return color.shade(shade)
        else:

            k = color.random_between(starting_shade, ending_shade,
                                     no_of_colors)
            if len(k) == 1:
                return k[0]
            else:
                return k

    def random(self, no_of_colors: int = 1, shade: float = None,
               starting_shade: float = 0,
               end_shade: float = 100,
               force_gray: bool = False):

        box = [x for x in self.__colors.values() if x.type != TYPE_GRAY]

        if force_gray:
            box = [x for x in self.__colors.values()]

        if no_of_colors == 1:
            return self.__convert(self.__random_pick(random.sample(box, 1)[0],
                                                     shade=shade,
                                                     starting_shade=starting_shade,
                                                     ending_shade=end_shade))
        elif no_of_colors < len(box):
            return_box = []
            for c in random.sample(box, no_of_colors):
                return_box.append(self.__random_pick(c, shade=shade,
                                                     starting_shade=starting_shade,
                                                     ending_shade=end_shade))

            return [self.__convert(x) for x in return_box]

        else:
            extra_box = []
            for i in range(no_of_colors):
                c = random.sample(box, 1)[0]
                extra_box.append(self.__random_pick(c, shade=shade,
                                                    starting_shade=starting_shade,
                                                    ending_shade=end_shade))

            return [self.__convert(x) for x in extra_box]

    def random_balanced(self, no_of_colors: int = 1):
        return self.random(shade=50, no_of_colors=no_of_colors)

    def __common_color(self, name: str, shade: float = None,
                       no_of_colors: int = 1, starting_shade: float = 0,
                       ending_shade: float = 100):
        c = self.__get_color(name)
        if shade is None:
            shade = c.core_shade_value
        return self.__convert(self.__random_pick(c,
                                                 no_of_colors,
                                                 shade,
                                                 starting_shade, ending_shade
                                                 ))

    def red(self, shade: float = None,
            no_of_colors: int = 1, starting_shade: float = 0,
            ending_shade: float = 100):
        return self.__common_color("red", shade, no_of_colors, starting_shade,
                                   ending_shade)

    def test(self):
        print(self.red(20))
