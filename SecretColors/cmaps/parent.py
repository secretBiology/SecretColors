#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

from SecretColors.models.palette import Palette
from SecretColors.helpers.logging import Log
import numpy as np


class ColorMapParent:
    """
    Main ColorMap class which will be inherited by all ColorMap objects
    """

    def __init__(self, matplotlib,
                 palette: Palette = None,
                 log: Log = None,
                 seed=None):
        """
        Initializing of any ColorMap.

        ..  warning::

            Avoid using :paramref:`palette` when using subclasses.

        :param matplotlib: matplotlib object from matplotlib library
        :param palette: Palette from which you want colors
        :param log: Log class
        :param seed: Seed for random number generation
        """
        self._mat = matplotlib
        if log is None:
            log = Log()
        self.log = log
        if palette is None:
            palette = Palette()
            self.log.info(f"ColorMap will use '{palette.name}' palette")
        self._palette = palette
        self._seed = seed
        if seed is not None:
            np.random.seed(seed)
            self.log.info(f"Random seed set for : {seed}")
        self.no_of_colors = 10

    @property
    def data(self) -> dict:
        raise NotImplementedError

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        np.random.seed(value)
        self.log.info(f"Random seed set for : {value}")

    @property
    def palette(self):
        return self._palette

    @palette.setter
    def palette(self, palette: Palette):
        self._palette = palette
        self.log.info(f"ColorMap is now using '{palette.name}' palette")

    @property
    def get_all(self) -> list:
        if self.data is None:
            return []
        else:
            return list(self.data.keys())

    def _get_linear_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: LinearSegmentedColormap
        """
        try:
            return self._mat.colors.LinearSegmentedColormap.from_list(
                "secret_color", color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def _get_listed_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: ListedColormap
        """
        try:
            return self._mat.colors.ListedColormap(color_list)
        except AttributeError:
            raise Exception("Matplotlib is required to use this function")

    def _derive_map(self, color_list: list,
                    is_qualitative=False,
                    is_reversed=False):
        """
        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :param is_reversed: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """

        if is_reversed:
            color_list = [x for x in reversed(color_list)]
        if is_qualitative:
            return self._get_listed_segment(color_list)
        else:
            return self._get_linear_segment(color_list)

    def _get_colors(self, key: str, no_of_colors: int, backup: str,
                    staring_shade, ending_shade):

        if no_of_colors < 2:
            self.log.error("Minimum of 2 colors are required for generating "
                           "Colormap", exception=ValueError)
        colors = None
        # First check if for given combinations of parameters, colors are
        # available
        if self.data is not None:
            if key in self.data:
                if str(no_of_colors) in self.data[key]:
                    colors = self.data[key][str(no_of_colors)]
                    self.log.info("Colormap for given combination found")

        if colors is None:
            self.log.info("Colormap for given combination not found.")
            self.log.info("Searching standard colors")
            # Just make request for the color so that additional colors will
            # be added to palette
            self.palette.get(backup)

        if (staring_shade is not None or
                ending_shade is not None or
                colors is None):
            self.log.warn("Overriding the available standard Colormaps "
                          "because starting_shade or ending_shade is provided")

            if staring_shade is None:
                staring_shade = min(self.palette.colors[
                                        backup].get_all_shades())
            if ending_shade is None:
                ending_shade = max(
                    self.palette.colors[backup].get_all_shades())

            return self.palette.get(backup, no_of_colors=no_of_colors,
                                    starting_shade=staring_shade,
                                    ending_shade=ending_shade)

        return colors

    def _default(self, name, backup, kwargs):
        del kwargs['self']
        if "starting_shade" not in kwargs:
            kwargs["starting_shade"] = None
        if "ending_shade" not in kwargs:
            kwargs["ending_shade"] = None

        no_of_colors = kwargs['no_of_colors'] or self.no_of_colors
        bak_name = backup or name

        colors = self._get_colors(key=name,
                                  no_of_colors=no_of_colors,
                                  backup=bak_name,
                                  staring_shade=kwargs['starting_shade'],
                                  ending_shade=kwargs['ending_shade'])

        return self._derive_map(colors,
                                is_qualitative=kwargs['is_qualitative'],
                                is_reversed=kwargs['is_reversed'])

    def _special_maps(self, name, backup, kwargs):
        if name not in self.data.keys():
            self.log.error(f"There is no '{name}' colormap in our "
                           f"database. Following special colormaps are"
                           f" available in current class :"
                           f" {list(self.data.keys())}")
        no_of_colors = kwargs['no_of_colors'] or self.no_of_colors
        cols = list(self.data[name].keys())
        if 'type' in cols:
            cols.remove('type')
        cols = [int(x) for x in cols]
        if no_of_colors not in cols:
            self.log.error(f"Sorry, for {name} colormap, 'no_of_colors' "
                           f"argument can "
                           f"only take these values: {cols}.")
        return self._default(name, backup, kwargs)

    def from_list(self, color_list: list, is_qualitative: bool = False,
                  is_reversed=False):
        """
        You can create your own colormap with list of own colors

        :param color_list: List of colors
        :param is_qualitative: If True, makes listed colormap
        :param is_reversed: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """
        return self._derive_map(color_list, is_qualitative, is_reversed)

    def get(self, name: str, *, no_of_colors: int = None,
            is_qualitative: bool = False, is_reversed=False):
        """
        Get arbitrary color map from current ColorMap object

        Number of colors is probably the most important parameter in the
        colormap classes. In this library each colormap data is structured
        in the form of dictionary. You can check which all colormaps are
        available by :attr:`~SecretColors.cmaps.parent.ColorMapParent
        .get_all` property

        .. note::

            Subsequent indented lines comprise
            the body of the topic, and are
            interpreted as body elements.



        :param name: Exact Name of the Colormap
        :type name: str

        :param no_of_colors: Number of colors. (See discussion above)
        :type no_of_colors: int

        :param is_qualitative:
        :param is_reversed:
        :return:
        """
        return self._special_maps(name, None, locals())

    def greens(self, *, starting_shade: float = None,
               ending_shade: float = None,
               no_of_colors: int = None,
               is_qualitative: bool = False,
               is_reversed=False):
        return self._default(None, "green", locals())

    def reds(self, *, starting_shade: float = None,
             ending_shade: float = None,
             no_of_colors: int = None,
             is_qualitative: bool = False,
             is_reversed=False):
        return self._default(None, "red", locals())

    def oranges(self, *, starting_shade: float = None,
                ending_shade: float = None,
                no_of_colors: int = None,
                is_qualitative: bool = False,
                is_reversed=False):
        return self._default(None, "orange", locals())

    def purples(self, *, starting_shade: float = None,
                ending_shade: float = None,
                no_of_colors: int = None,
                is_qualitative: bool = False,
                is_reversed=False):
        return self._default(None, "purple", locals())

    def grays(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default(None, "gray", locals())

    def blues(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default(None, "blue", locals())
