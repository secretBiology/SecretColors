#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#

from SecretColors.helpers.decorators import deprecated_aliases
import random
import warnings
from SecretColors._validation import count
from SecretColors.helpers.decorators import REMOVAL, deprecated

from SecretColors.cmaps.maps import _build, colors as map_colors, from_colors
from SecretColors.data.constants import DIV_COLOR_PAIRS
from SecretColors.helpers.logging import Log
from SecretColors.models.palette import Palette


def _colors_module(obj):
    for candidate in (getattr(obj, "colors", None), obj):
        if hasattr(candidate, "LinearSegmentedColormap") and hasattr(
                candidate, "ListedColormap"):
            return candidate
    return None


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

    def __init__(self, matplotlib=None,
                 palette: Palette = None,
                 log: Log = None,
                 seed=None):
        """
        Initializing of any ColorMap.

        :param matplotlib: (Optional) matplotlib module. It is not needed
            anymore as matplotlib is imported automatically when required.
            Kept for backward compatibility.

        :param palette: Palette from which you want colors
        :type palette: Palette

        :param log: Log class
        :type log: Log

        :param seed: Seed for random number generation
        """
        warnings.warn(
            f"{type(self).__name__} is deprecated. Use 'from SecretColors import cmaps', "
            "then cmaps.cmap(name, n=..., discrete=False) for named colormaps, "
            "cmaps.from_colors(color_list) instead of from_list(), or "
            "cmaps.colors(name, n=...) for color lists. Set n to your previous color "
            "count and pass palette=... when using a custom palette. "
            f"{REMOVAL}", DeprecationWarning, stacklevel=2)
        if matplotlib is not None and _colors_module(matplotlib) is None:
            raise TypeError(f"First argument should be the matplotlib module "
                            f"(or omitted), not {type(matplotlib)}")
        self._mat = matplotlib
        if log is None:
            log = Log()
        self.log = log
        if palette is None:
            palette = Palette()
            self.log.info(f"ColorMap will use '{palette.name}' palette")
        self._palette = palette
        self._seed = seed
        self._rng = random.Random(seed)
        if seed is not None:
            self.log.info(f"Random seed set for : {seed}")
        self.n = 10

    @property
    @deprecated("Read 'colormap.n' instead of 'colormap.no_of_colors'.")
    def no_of_colors(self):
        return self.n

    @no_of_colors.setter
    @deprecated("Assign 'colormap.n = value' instead of 'colormap.no_of_colors = value'.")
    def no_of_colors(self, value):
        self.n = count(value)

    @property
    def _mpl_colors(self):
        if self._mat is None:
            return None
        return _colors_module(self._mat)

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
        Seed for random number generator

        :param value: Seed value
        """
        self._seed = value
        self._rng.seed(value)
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
        return _build(color_list, "secret_color", False, self._mpl_colors)

    def _get_listed_segment(self, color_list: list):
        """
        :param color_list: List of colors
        :return: ListedColormap
        """
        return _build(color_list, "secret_color", True, self._mpl_colors)

    def _derive_map(self, color_list: list,
                    discrete=False,
                    reverse=False):
        """
        :param color_list: List of colors
        :param discrete: If True, makes listed colormap
        :param reverse: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """

        if reverse:
            color_list = [x for x in reversed(color_list)]
        if discrete:
            return self._get_listed_segment(color_list)
        else:
            return self._get_linear_segment(color_list)

    def _get_colors(self, key: str, n: int, backup: str,
                    staring_shade, end):

        n = count(n, minimum=2)
        colors = None
        # First check if for given combinations of parameters, colors are
        # available
        if self.data is not None:
            if key in self.data:
                if str(n) in self.data[key]:
                    colors = map_colors(key, n=n)
                    self.log.info("Colormap for given combination found")

        if colors is None:
            self.log.info("Colormap for given combination not found. "
                          "Searching standard colors")

        if (staring_shade is not None or
                end is not None or
                colors is None):
            if colors is not None:
                self.log.warn("Overriding the available standard Colormaps "
                              "because start or end is "
                              "provided")

            color = self.palette.find_color(backup)
            if color is not None:
                if staring_shade is None:
                    staring_shade = min(color.get_all_shades())
                if end is None:
                    end = max(color.get_all_shades())

            return map_colors(backup, palette=self.palette, n=n,
                              start=staring_shade, end=end)

        return colors

    @deprecated_aliases(no_of_colors='n')
    def get_colors(self, name: str, n: int) -> list:
        """
        This is easy way to get the available colors in current colormap

        .. code-block:: python

            cm = BrewerMap()
            cm.get_colors('Spectral', 9) # Returns 9 'Spectral' colors from BrewerMap colormap


        .. warning::

            Be careful in using `n` argument. It actually
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
        :param n: Number of colors (see warning above)
        :type n: int
        :return: List of colors
        :rtype: List[str]

        :raises: ValueError (if used on
            :class:`~SecretColors.cmaps.ColorMap` or wrong
            `n` provided)
        """
        n = count(n)
        if self.data is not None:
            if name not in self.data.keys():
                self.log.error(f"'{name}' is not available in current "
                               f"colormap. Following are allowed arguments "
                               f"here: {self.get_all}",
                               exception=ValueError)
            if str(n) not in self.data[name].keys():
                n = list(self.data[name].keys())
                if "type" in n:
                    n.remove("type")
                n = [int(x) for x in n]
                self.log.error(f"Currently following number of colors are "
                               f"allowed for {name}. : {n}",
                               exception=ValueError)
            return map_colors(name, n=n)
        return []

    def _default(self, name, backup, *, n: int = None,
                 start: float = None, end: float = None,
                 discrete: bool = False, reverse=False):
        colors = self._get_colors(key=name,
                                  n=self.n if n is None else n,
                                  backup=backup or name,
                                  staring_shade=start,
                                  end=end)
        return self._derive_map(colors,
                                discrete=discrete,
                                reverse=reverse)

    def _special_maps(self, name, backup, *, n: int = None,
                      discrete: bool = False, reverse=False):
        if name not in self.data.keys():
            self.log.error(f"There is no '{name}' colormap in our "
                           f"database. Following special colormaps are"
                           f" available in current class :"
                           f" {list(self.data.keys())}",
                           exception=ValueError)
        n = count(self.n if n is None else n)
        cols = list(self.data[name].keys())
        if 'type' in cols:
            cols.remove('type')
        cols = [int(x) for x in cols]
        if n not in cols:
            self.log.error(f"Sorry, for {name} colormap, 'n' "
                           f"argument can "
                           f"only take these values: {cols}.",
                           exception=ValueError)
        return self._default(name, backup, n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(is_qualitative='discrete', is_reversed='reverse')
    def from_list(self, color_list: list, discrete: bool = False,
                  reverse=False):
        """
        You can create your own colormap with list of own colors

        :param color_list: List of colors
        :param discrete: If True, makes listed colormap
        :param reverse: Reverses the order of color in Colormap
        :return: Colormap which can be directly used with matplotlib
        """
        return from_colors(color_list, discrete=discrete, reverse=reverse,
                           name="secret_color", _mpl_colors=self._mpl_colors)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    def get(self, name: str, *, n: int = None,
            discrete: bool = False, reverse=False):
        """
        Get arbitrary color map from current ColorMap object

        `n` is probably the most important parameter in the
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

        >>> YourMap().get('map_name',n=10) # Returns [c1, c2 ...c10]

        You can check which all colormaps are
        available by :attr:`~SecretColors.cmaps.parent.ColorMapParent.get_all` property


        :param name: Exact Name of the Colormap
        :type name: str

        :param n: Number of colors. (See discussion above)
        :type n: int

        :param discrete: If True, listed colormap will be returned. (
            default: False)
        :type discrete: bool

        :param reverse: If True, colormap will be reversed. (default:
            False)
        :type reverse: bool

        :return: Colormap object
        :rtype: :class:`matplotlib.colors.ListedColormap` or :class:`matplotlib.colors.LinearSegmentedColormap`
        """
        if self.data is None:
            self.log.error("This method can only be used with special "
                           "colormap. If you are using 'ColorMap' class "
                           "directly. You can only use standard maps. or "
                           "create your own.",
                           exception=ValueError)
        return self._special_maps(name, None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def greens(self, *, start: float = None,
               end: float = None,
               n: int = None,
               discrete: bool = False,
               reverse=False):
        return self._default(None, "green", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def reds(self, *, start: float = None,
             end: float = None,
             n: int = None,
             discrete: bool = False,
             reverse=False):
        return self._default(None, "red", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def oranges(self, *, start: float = None,
                end: float = None,
                n: int = None,
                discrete: bool = False,
                reverse=False):
        return self._default(None, "orange", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def purples(self, *, start: float = None,
                end: float = None,
                n: int = None,
                discrete: bool = False,
                reverse=False):
        return self._default(None, "purple", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def grays(self, *, start: float = None,
              end: float = None,
              n: int = None,
              discrete: bool = False,
              reverse=False):
        return self._default(None, "gray", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def blues(self, *, start: float = None,
              end: float = None,
              n: int = None,
              discrete: bool = False,
              reverse=False):
        return self._default(None, "blue", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(is_qualitative='discrete', is_reversed='reverse')
    def random_divergent(self, discrete=False, reverse=False):
        names = []
        if self.data is not None:
            for k in self.data:
                if self.data[k]["type"] == "div":
                    names.append(k)

        if len(names) > 0:
            self._rng.shuffle(names)
            keys = list(self.data[names[0]].keys())
            keys.remove("type")
            self._rng.shuffle(keys)
            return self._special_maps(names[0], None,
                                      n=int(keys[0]),
                                      discrete=discrete,
                                      reverse=reverse)
        else:
            names = [x for x in DIV_COLOR_PAIRS]
            self._rng.shuffle(names)
            cols = []
            for c in names[0]:
                for s in c[1]:
                    cols.append(self.palette.get(c[0], shade=s))
            return self.from_list(cols, discrete, reverse)


class ColorMap(ColorMapParent):
    """
    This is simple wrapper around
    :class:`~SecretColors.cmaps.parent.ColorMapParent`. This wrapper let you
    utilize all methods from its parent class. For all general purpose use,
    you should use this class. If you want more specialized ColorMaps,
    use their respective classes. Following is the simplest use where you
    want to visualize your data in typical 'greens' palette

    .. code-block:: python

        import matplotlib.pyplot as plt
        from SecretColors.cmaps import ColorMap
        import numpy as np

        cm = ColorMap()
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

        - :n: Number of colors you want in your
            colormap. It usually defines how smaooth your color gradient will be
        - :start: What will be the first shade of your colormap
        - :end: What will be the last shade of your colormap
        - :discrete: If True,
            :class:`matplotlib.colors.ListedColormap` will be used instead
            :class:`matplotlib.colors.LinearSegmentedColormap`. Essentially it
            will provide discrete colormap instead linear
        - :reverse: If True, colormap will be reversed

    .. code-block:: python

        cm.purples(n=8)
        cm.greens(start=30, end=80)
        cm.blues(discrete=True)
        cm.reds(end=50, reverse=True, n=5)

    You can mix-and-match every argument. Essentially there are infinite
    possibilities.

    If you want even more fine-tune control over your colormap, you can use
    your own colormaps by :func:`~SecretColors.cmaps.parent.ColorMapParent
    .from_list` method.

    .. code-block:: python

        cm = ColorMap()
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

        cm = ColorMap()
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

