#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  ColorMap implementation for the Tableau Palette


from SecretColors.cmaps.parent import ColorMapParent
from SecretColors.data.cmaps.tableau import TABLEAU_DATA
from SecretColors.data.constants import PALETTE_TABLEAU
from SecretColors.helpers.decorators import cmap_docs
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
        :emphasize-lines: 5

        import matplotlib
        import matplotlib.pyplot as plt
        from SecretColors.cmaps import TableauMap
        tm = TableauMap(matplotlib)
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

    def __init__(self, matplotlib):
        super().__init__(matplotlib)
        self.palette = Palette(PALETTE_TABLEAU)

    @property
    def data(self):
        return TABLEAU_DATA

        # Other special maps

    def grays(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default("Gray", "gray", locals())

    def greens(self, *, starting_shade: float = None,
               ending_shade: float = None,
               no_of_colors: int = None,
               is_qualitative: bool = False,
               is_reversed=False):
        return self._default("Green", "green", locals())

    def blues(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default("Blue", "blue", locals())

    def reds(self, *, starting_shade: float = None,
             ending_shade: float = None,
             no_of_colors: int = None,
             is_qualitative: bool = False,
             is_reversed=False):
        return self._default("Red", "red", locals())

    def oranges(self, *, starting_shade: float = None,
                ending_shade: float = None,
                no_of_colors: int = None,
                is_qualitative: bool = False,
                is_reversed=False):
        return self._default("Orange", "orange", locals())

    @cmap_docs(MP_NAME, "Tableau")
    def tableau(self, *, no_of_colors: int = None,
                is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Tableau", None, locals())

    @cmap_docs(MP_NAME, "Tableau_light")
    def tableau_light(self, *, no_of_colors: int = None,
                      is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Tableau_light", None, locals())

    @cmap_docs(MP_NAME, "Tableau_medium")
    def tableau_medium(self, *, no_of_colors: int = None,
                       is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Tableau_medium", None, locals())

    @cmap_docs(MP_NAME, "ColorBlind")
    def colorblind(self, *, no_of_colors: int = None,
                   is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("ColorBlind", None, locals())

    @cmap_docs(MP_NAME, "TrafficLight")
    def traffic_light(self, *, no_of_colors: int = 9,
                      is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("TrafficLight", None, locals())

    @cmap_docs(MP_NAME, "PurpleGray")
    def purple_gray(self, *, no_of_colors: int = 12,
                    is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PurpleGray", None, locals())

    @cmap_docs(MP_NAME, "GreenOrange")
    def green_orange(self, *, no_of_colors: int = 12,
                     is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("GreenOrange", None, locals())

    @cmap_docs(MP_NAME, "BlueRed")
    def blue_red(self, *, no_of_colors: int = 12,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BlueRed", None, locals())

    @cmap_docs(MP_NAME, "Cyclic")
    def cyclic(self, *, no_of_colors: int = 13,
               is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Cyclic", None, locals())

    @cmap_docs(MP_NAME, "AquaRed")
    def aqua_red(self, *, no_of_colors: int = 11,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("AquaRed", None, locals())

    @cmap_docs(MP_NAME, "AquaGreen")
    def aqua_green(self, *, no_of_colors: int = 11,
                   is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("AquaGreen", None, locals())

    @cmap_docs(MP_NAME, "AquaBrown")
    def aqua_brown(self, *, no_of_colors: int = 11,
                   is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("AquaBrown", None, locals())

    @cmap_docs(MP_NAME, "RedBlue")
    def red_blue(self, *, no_of_colors: int = 11,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RedBlue", None, locals())

    @cmap_docs(MP_NAME, "RedBlack")
    def red_black(self, *, no_of_colors: int = 11,
                  is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RedBlack", None, locals())

    @cmap_docs(MP_NAME, "AreaRedGreen")
    def area_red_green(self, *, no_of_colors: int = 21,
                       is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("AreaRedGreen", None, locals())

    @cmap_docs(MP_NAME, "OrangeBlue")
    def orange_blue(self, *, no_of_colors: int = 13,
                    is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("OrangeBlue", None, locals())

    @cmap_docs(MP_NAME, "GreenBlue")
    def green_blue(self, *, no_of_colors: int = 11,
                   is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("GreenBlue", None, locals())

    @cmap_docs(MP_NAME, "RedWhiteGreen")
    def red_white_green(self, *, no_of_colors: int = 11,
                        is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RedWhiteGreen", None, locals())

    @cmap_docs(MP_NAME, "RedWhiteBlack")
    def red_white_black(self, *, no_of_colors: int = 11,
                        is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RedWhiteBlack", None, locals())

    @cmap_docs(MP_NAME, "OrangeWhiteBlue")
    def orange_white_blue(self, *, no_of_colors: int = 11,
                          is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("OrangeWhiteBlue", None, locals())

    @cmap_docs(MP_NAME, "RedWhiteBlack_light")
    def red_white_black_light(self, *, no_of_colors: int = 10,
                              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RedWhiteBlack_light", None, locals())

    @cmap_docs(MP_NAME, "OrangeWhiteBlue_light")
    def orange_white_blue_light(self, *, no_of_colors: int = 11,
                                is_qualitative: bool = False,
                                is_reversed=False):
        return self._special_maps("OrangeWhiteBlue_light", None, locals())

    @cmap_docs(MP_NAME, "RedWhiteGreen_light")
    def red_white_green_light(self, *, no_of_colors: int = 11,
                              is_qualitative: bool = False,
                              is_reversed=False):
        return self._special_maps("RedWhiteGreen_light", None, locals())

    @cmap_docs(MP_NAME, "RedGreen_light")
    def red_green_light(self, *, no_of_colors: int = 11,
                        is_qualitative: bool = False,
                        is_reversed=False):
        return self._special_maps("RedGreen_light", None, locals())


def run():
    import matplotlib
    b = TableauMap(matplotlib)
    for t in b.get_all:
        print(f"* {t}")
