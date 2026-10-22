#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  ColorMap implementation for the Tableau Palette


from SecretColors.helpers.decorators import deprecated_aliases
from SecretColors.cmaps.parent import ColorMapParent
from SecretColors.data.cmaps.tableau import TABLEAU_DATA
from SecretColors.data.constants import PALETTE_TABLEAU
from SecretColors.helpers.decorators import cmap_docs
from SecretColors.helpers.logging import Log
from SecretColors.models.palette import Palette

MP_NAME = "TableauMap"


class TableauMap(ColorMapParent):
    """
    Tableau Color Maps are derived from `Tableau <https://www.tableau.com/>`_
    Visualization Software. Unfortunately, their current version is not
    available publicly and hence we could not include here. Current color
    values are from their 9.x Legacy version which can be found `here
    <https://help.tableau.com/current/pro/desktop/en-us
    /formatting_create_custom_colors.htm#Version_9.x_(
    legacy)_color_palette_hex_values>`_ . This class acts as an wrapper
    around original colors which you can easily manipulate. This class is
    inherited from :class:`~SecretColors.cmaps.parent.ColorMapParent` and
    overrides few default methods which are available in our database.

    Simplest way to use this class in your ``matplotlib`` workflow is following

    ..  code-block:: python
        :emphasize-lines: 4

        import matplotlib.pyplot as plt
        from SecretColors.cmaps import TableauMap
        tm = TableauMap()
        plt.imshow(data, cmap=tm.tableau())
        plt.show()

    Here, :func:`~SecretColors.cmaps.TableauMap.tableau` is one of
    the available standard color map in this class. If you know the exact
    name of the color map, you can use following as well

    ..  code-block:: python

        plt.imshow(data, cmap= tm.get("Tableau")) # Alternate way
        tm.get_all  # Gives you all available colormaps
        tm.data # Returns available color data

    To know which all color maps are available in current class you can use
    ``get_all`` attribute. These methods can be heavily
    customized. Take a look at
    :class:`~SecretColors.cmaps.parent.ColorMapParent` documentation.



    .. admonition:: List of available colormaps in TableauMap

        ..  hlist::
            :columns: 3

            * Tableau
            * Tableau_medium
            * Tableau_light
            * Gray
            * ColorBlind
            * TrafficLight
            * PurpleGray
            * GreenOrange
            * BlueRed
            * Cyclic
            * Green
            * Blue
            * Red
            * Orange
            * AquaRed
            * AquaGreen
            * AquaBrown
            * RedGreen
            * RedBlue
            * RedBlack
            * AreaRedGreen
            * OrangeBlue
            * GreenBlue
            * RedWhiteGreen
            * RedWhiteBlack
            * OrangeWhiteBlue
            * RedWhiteBlack_light
            * OrangeWhiteBlue_light
            * RedWhiteGreen_light
            * RedGreen_light

    ..  seealso::

        :class:`SecretColors.cmaps.parent.ColorMapParent`

    """

    def __init__(self, matplotlib=None, log: Log = None, seed=None):
        super().__init__(matplotlib, palette=Palette(PALETTE_TABLEAU),
                         log=log, seed=seed)

    @property
    def data(self):
        return TABLEAU_DATA

        # Other special maps

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def grays(self, *, start: float = None,
              end: float = None,
              n: int = None,
              discrete: bool = False,
              reverse=False):
        return self._default("Gray", "gray", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def greens(self, *, start: float = None,
               end: float = None,
               n: int = None,
               discrete: bool = False,
               reverse=False):
        return self._default("Green", "green", start=start,
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
        return self._default("Blue", "blue", start=start,
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
        return self._default("Red", "red", start=start,
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
        return self._default("Orange", "orange", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Tableau")
    def tableau(self, *, n: int = None,
                discrete: bool = False, reverse=False):
        return self._special_maps("Tableau", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Tableau_light")
    def tableau_light(self, *, n: int = None,
                      discrete: bool = False, reverse=False):
        return self._special_maps("Tableau_light", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Tableau_medium")
    def tableau_medium(self, *, n: int = None,
                       discrete: bool = False, reverse=False):
        return self._special_maps("Tableau_medium", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "ColorBlind")
    def colorblind(self, *, n: int = None,
                   discrete: bool = False, reverse=False):
        return self._special_maps("ColorBlind", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "TrafficLight")
    def traffic_light(self, *, n: int = 9,
                      discrete: bool = False, reverse=False):
        return self._special_maps("TrafficLight", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PurpleGray")
    def purple_gray(self, *, n: int = 12,
                    discrete: bool = False, reverse=False):
        return self._special_maps("PurpleGray", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "GreenOrange")
    def green_orange(self, *, n: int = 12,
                     discrete: bool = False, reverse=False):
        return self._special_maps("GreenOrange", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "BlueRed")
    def blue_red(self, *, n: int = 12,
                 discrete: bool = False, reverse=False):
        return self._special_maps("BlueRed", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Cyclic")
    def cyclic(self, *, n: int = 13,
               discrete: bool = False, reverse=False):
        return self._special_maps("Cyclic", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "AquaRed")
    def aqua_red(self, *, n: int = 11,
                 discrete: bool = False, reverse=False):
        return self._special_maps("AquaRed", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "AquaGreen")
    def aqua_green(self, *, n: int = 11,
                   discrete: bool = False, reverse=False):
        return self._special_maps("AquaGreen", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "AquaBrown")
    def aqua_brown(self, *, n: int = 11,
                   discrete: bool = False, reverse=False):
        return self._special_maps("AquaBrown", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedBlue")
    def red_blue(self, *, n: int = 11,
                 discrete: bool = False, reverse=False):
        return self._special_maps("RedBlue", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedBlack")
    def red_black(self, *, n: int = 11,
                  discrete: bool = False, reverse=False):
        return self._special_maps("RedBlack", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "AreaRedGreen")
    def area_red_green(self, *, n: int = 21,
                       discrete: bool = False, reverse=False):
        return self._special_maps("AreaRedGreen", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "OrangeBlue")
    def orange_blue(self, *, n: int = 13,
                    discrete: bool = False, reverse=False):
        return self._special_maps("OrangeBlue", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "GreenBlue")
    def green_blue(self, *, n: int = 11,
                   discrete: bool = False, reverse=False):
        return self._special_maps("GreenBlue", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedWhiteGreen")
    def red_white_green(self, *, n: int = 11,
                        discrete: bool = False, reverse=False):
        return self._special_maps("RedWhiteGreen", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedWhiteBlack")
    def red_white_black(self, *, n: int = 11,
                        discrete: bool = False, reverse=False):
        return self._special_maps("RedWhiteBlack", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "OrangeWhiteBlue")
    def orange_white_blue(self, *, n: int = 11,
                          discrete: bool = False, reverse=False):
        return self._special_maps("OrangeWhiteBlue", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedWhiteBlack_light")
    def red_white_black_light(self, *, n: int = 10,
                              discrete: bool = False, reverse=False):
        return self._special_maps("RedWhiteBlack_light", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "OrangeWhiteBlue_light")
    def orange_white_blue_light(self, *, n: int = 11,
                                discrete: bool = False,
                                reverse=False):
        return self._special_maps("OrangeWhiteBlue_light", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedWhiteGreen_light")
    def red_white_green_light(self, *, n: int = 11,
                              discrete: bool = False,
                              reverse=False):
        return self._special_maps("RedWhiteGreen_light", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RedGreen_light")
    def red_green_light(self, *, n: int = 11,
                        discrete: bool = False,
                        reverse=False):
        return self._special_maps("RedGreen_light", None,
                                  n=n,
                                  discrete=discrete,
                                  reverse=reverse)

