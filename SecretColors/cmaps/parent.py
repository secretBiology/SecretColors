#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

import numpy as np

from SecretColors.data.constants import DIV_COLOR_PAIRS
from SecretColors.helpers.logging import Log
from SecretColors.models.palette import Palette
from typing import List


class ColorMapParent:
    """

    This is parent class which will be inherited by all ColorMap objects. It
    includes all basic methods which will be common to all the ColorMaps.

    ..  danger::
        Do not use this class in your workflow. This class is intended as a
        parent class which you can inherit to make new colormaps. For
        general purpose use, you should use
        :class:`~SecretColors.cmaps.ColorMap` instead.

    """

    def __init__(self, matplotlib,
                 palette: Palette = None,
                 log: Log = None,
                 seed=None):
        """
        Initializing of any ColorMap.

        :param matplotlib: matplotlib object from matplotlib library

        :param palette: Palette from which you want colors
        :type palette: Palette

        :param log: Log class
        :type log: Log

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
        """Returns all available ColorMap data. This is valid ONLY for
        special subclass (e.g. BrewerMap). It will return None for 'ColorMap'
        class.

        :rtype: dict
        """
        raise NotImplementedError

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        """
        Seed for Numpy random number generator

        :param value: Seed value
        """
        self._seed = value
        np.random.seed(value)
        self.log.info(f"Random seed set for : {value}")

    @property
    def palette(self) -> Palette:
        """
        :return: Returns current palette from which colors are drawn
        :rtype: Palette
        """
        return self._palette

    @palette.setter
    def palette(self, palette: Palette):
        """
        Set Palette from which colors will be drawn

        Note: Do not set this for special subclasses (like BrewerMap)

        :param palette: Color Palette
        :type palette: Palette

        """
        self._palette = palette
        self.log.info(f"ColorMap is now using '{palette.name}' palette")

    @property
    def get_all(self) -> list:
        """Returns list of available special colormaps. This works only with
        special subclasses like BrewerMap.

        :return: List of colormap names
        :rtype: List[str]
        """
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

    def get_colors(self, name: str, no_of_colors: int) -> list:
        """
        This is easy way to get the available colors in current colormap

        .. code-block:: python

            cm = BrewerMap(matplotlib)
            cm.get_colors('Spectral', 9) # Returns 9 'Spectral' colors from BrewerMap colormap


        .. warning::

            Be careful in using :paramref:`no_of_colors` argument. It actually
            points
            to number of colors available in given colormap. For example,
            'Tableau' map from :class:`~SecretColors.cmaps.TableauMap`
            contains two list of colors, 10 and 20. So you need to enter
            either 10 or 20. Any other number will raise ValueError. You can
            check which all options are available by :attr:`get_all`
            property. More about this can be read in documentation of
            :func:`~SecretColors.cmaps.parent.ColorMapParent.get` function.

        :param name: Name of the special colormap
        :type name: str
        :param no_of_colors: Number of colors (see warning above)
        :type no_of_colors: int
        :return: List of colors
        :rtype: List[str]

        :raises: ValueError (if used on
            :class:`~SecretColors.cmaps.ColorMap` or wrong
            :paramref:`no_of_colors` provided)
        """
        if self.data is not None:
            if name not in self.data.keys():
                self.log.error(f"'{name}' is not available in current "
                               f"colormap. Following are allowed arguments "
                               f"here: {self.get_all}")
            if str(no_of_colors) not in self.data[name].keys():
                n = list(self.data[name].keys())
                if "type" in n:
                    n.remove("type")
                n = [int(x) for x in n]
                self.log.error(f"Currently following number of colors are "
                               f"allowed for {name}. : {n}")
            return self.data[name][no_of_colors]
        return []

    def _default(self, name, backup, kwargs):
        if "self" in kwargs:
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

        :paramref:`no_of_colors` is probably the most important parameter in the
        colormap classes. In this library each colormap data is structured
        in the form of dictionary as shown below::

            data = { 'map_name' : {
                    '10': [c1, c2, ... c10],
                    '5' : [b1, b2, ... b5],
                    ...
                    'type': Type of colormap
                }
            }

        In above example, if you want to access list [c1, c2...c10], you can
        do following,

        >>> YourMap().get('map_name',no_of_colors=10) # Returns [c1, c2 ...c10]

        You can check which all colormaps are
        available by :attr:`~SecretColors.cmaps.parent.ColorMapParent.get_all` property


        :param name: Exact Name of the Colormap
        :type name: str

        :param no_of_colors: Number of colors. (See discussion above)
        :type no_of_colors: int

        :param is_qualitative: If True, listed colormap will be returned. (
            default: False)
        :type is_qualitative: bool

        :param is_reversed: If True, colormap will be reversed. (default:
            False)
        :type is_reversed: bool

        :return: Colormap object
        :rtype: :class:`matplotlib.colors.ListedColormap` or :class:`matplotlib.colors.LinearSegmentedColormap`
        """
        if self.data is None:
            self.log.error(f"This method can only be used with special "
                           f"colormap. If you are using 'ColorMap' class "
                           f"directly. You can only use standard maps. or "
                           f"create your own.")
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

    def random_divergent(self, is_qualitative=False, is_reversed=False):
        names = []
        if self.data is not None:
            for k in self.data:
                if self.data[k]["type"] == "div":
                    names.append(k)

        if len(names) > 0:
            np.random.shuffle(names)
            keys = list(self.data[names[0]].keys())
            keys.remove("type")
            np.random.shuffle(keys)
            kwargs = locals()
            kwargs["no_of_colors"] = int(keys[0])
            return self._special_maps(names[0], None, kwargs)
        else:
            names = [x for x in DIV_COLOR_PAIRS]
            np.random.shuffle(names)
            cols = []
            for c in names[0]:
                for s in c[1]:
                    cols.append(self.palette.get(c[0], shade=s))
            return self.from_list(cols)


class ColorMap(ColorMapParent):
    """
    This is simple wrapper around
    :class:`~SecretColors.cmaps.parent.ColorMapParent`. This wrapper let you
    utilize all methods from its parent class. For all general purpose use,
    you should use this class. If you want more specialized ColorMaps,
    use their respective classes. Following is the simplest use where you
    want to visualize your data in typical 'greens' palette

    .. code-block:: python

        import matplotlib
        import matplotlib.pyplot as plt
        from SecretColors.cmaps import ColorMap
        import numpy as np

        cm = ColorMap(matplotlib)
        data = np.random.rand(5, 5)
        plt.imshow(data, cmap=cm.greens())
        plt.colorbar()
        plt.show()

    You can easily change standard colormaps like following

    .. code-block:: python

        cm.reds()  # Reds colormap
        cm.oranges() # Oranges colormap
        cm.blues()  # Blues colormap
        cm.grays()  # Grays colormap

    All standard colormaps accepts following basic options (which should be
    provided as a named arguments)

        - :no_of_colors: Number of colors you want in your
            colormap. It usually defines how smaooth your color gradient will be
        - :starting_shade: What will be the first shade of your colormap
        - :ending_shade: What will be the last shade of your colormap
        - :is_qualitative: If True,
            :class:`matplotlib.colors.ListedColormap` will be used instead
            :class:`matplotlib.colors.LinearSegmentedColormap`. Essentially it
            will provide discrete colormap instead linear
        - :is_reversed: If True, colormap will be reversed

    .. code-block:: python

        cm.purples(no_of_colors=8)
        cm.greens(starting_shade=30, ending_shade=80)
        cm.blues(is_qualitative=True)
        cm.reds(ending_shade=50, is_reversed=True, no_of_colors=5)

    You can mix-and-match every argument. Essentially there are infinite
    possibilities.

    If you want even more fine-tune control over your colormap, you can use
    your own colormaps by :func:`~SecretColors.cmaps.parent.ColorMapParent
    .from_list` method.

    .. code-block:: python

        cm = ColorMap(matplotlib)
        p = Palette()
        my_colors = [p.red(shade=30), p.white(), p.blue(shade=60)]
        my_cmap = cm.from_list(my_colors)
        plt.imshow(data, cmap=my_cmap)

    We have some in-build color lists for divergent colormaps. You can use
    :func:`~SecretColors.cmaps.parent.ColorMapParent.random_divergent` for
    its easy access. Read :class:`~SecretColors.cmaps.parent.ColorMapParent`
    documentation for more details on helper functions.

    If you like colors from specific :class:`~SecretColors.Palette`, you can
    easily switch all colors with single line

    .. code-block:: python

        cm = ColorMap(matplotlib)
        cm.palette = Palette("material") # Material Palette colors will be used.
        cm.palette = Palette("brewer") # ColorBrewer colors will be used.


    .. tip::
        For "brewer" and "tableau", you should prefer using
        :class:`~SecretColors.cmaps.BrewerMap` and
        :class:`~SecretColors.cmaps.TableauMap` intsead just changing
        palette here. As these classes will provide you much more additional
        methods which are only available in those classes.


    """

    @property
    def data(self) -> dict:
        return None


def run():
    from SecretColors.data.cmaps.brewer import BREWER_DATA

    for b in BREWER_DATA:
        print(f"* {b}")
