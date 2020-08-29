#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  CMap implementation for Brewer

from SecretColors.data.cmaps.brewer import BREWER_DATA
from SecretColors.data.constants import PALETTE_BREWER
from SecretColors.cmaps.parent import ColorMapParent
from SecretColors.models.palette import Palette
from SecretColors.helpers.decorators import cmap_docs

MP_NAME = "BrewerMap"


class BrewerMap(ColorMapParent):
    """
    ColorBrewer2 is probably one of the best known colormap, special in the
    cartography community. It provides very robust and nice color maps which
    many people use in their daily visualization needs. We provide all the
    functionality of ColorBrewer maps in this class. You can take a look at
    their `site <https://colorbrewer2.org/>`_ for more details.

    Simplest way to use this class in your ``matplotlib`` workflow is following

    ..  code-block:: python
        :emphasize-lines: 5

        import matplotlib
        import matplotlib.pyplot as plt
        from SecretColors.cmaps import BrewerMap
        bm = BrewerMap(matplotlib)
        plt.imshow(data, cmap=bm.spectral())
        plt.show()

    Here, :func:`~SecretColors.cmaps.BrewerMap.spectral` is one of
    the available standard color map in this class. If you know the exact
    name of the color map, you can use following as well

    ..  code-block:: python

        plt.imshow(data, cmap= bm.get("Spectral")) # Alternate way
        bm.get_all  # Gives you all available colormaps
        bm.data # Returns available color data

    To know which all color maps are available in current class you can use
    ``get_all`` attribute. These methods can be heavily
    customized. Take a look at
    :class:`~SecretColors.cmaps.parent.ColorMapParent` documentation.

    .. admonition:: List of available colormaps in BrewerMap

        ..  hlist::
            :columns: 3

            * Spectral
            * RdYlGn
            * RdBu
            * PiYG
            * PRGn
            * RdYlBu
            * BrBG
            * RdGy
            * PuOr
            * Set2
            * Accent
            * Set1
            * Set3
            * Dark2
            * Paired
            * Pastel2
            * Pastel1
            * OrRd
            * PuBu
            * BuPu
            * Oranges
            * BuGn
            * YlOrBr
            * YlGn
            * Reds
            * RdPu
            * Greens
            * YlGnBu
            * Purples
            * GnBu
            * Greys
            * YlOrRd
            * PuRd
            * Blues
            * PuBuGn

    """

    def __init__(self, matplotlib):
        super().__init__(matplotlib)
        self.palette = Palette(PALETTE_BREWER)
        self.no_of_colors = 9

    @property
    def data(self):
        return BREWER_DATA

    def greens(self, *, starting_shade: float = None,
               ending_shade: float = None,
               no_of_colors: int = None,
               is_qualitative: bool = False,
               is_reversed=False):
        return self._default("Greens", "green", locals())

    def oranges(self, *, starting_shade: float = None,
                ending_shade: float = None,
                no_of_colors: int = None,
                is_qualitative: bool = False,
                is_reversed=False):
        return self._default("Oranges", "orange", locals())

    def reds(self, *, starting_shade: float = None,
             ending_shade: float = None,
             no_of_colors: int = None,
             is_qualitative: bool = False,
             is_reversed=False):
        return self._default("Reds", "red", locals())

    def purples(self, *, starting_shade: float = None,
                ending_shade: float = None,
                no_of_colors: int = None,
                is_qualitative: bool = False,
                is_reversed=False):
        return self._default("Purples", "purple", locals())

    def grays(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default("Greys", "gray", locals())

    def blues(self, *, starting_shade: float = None,
              ending_shade: float = None,
              no_of_colors: int = None,
              is_qualitative: bool = False,
              is_reversed=False):
        return self._default("Blues", "blue", locals())

    # Other special maps

    @cmap_docs(MP_NAME, "Spectral")
    def spectral(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Spectral", None, locals())

    @cmap_docs(MP_NAME, "RgYlGn")
    def rd_yl_gn(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdYlGn", None, locals())

    @cmap_docs(MP_NAME, "RdBu")
    def rd_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdBu", None, locals())

    @cmap_docs(MP_NAME, "PiYG")
    def pi_yg(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PiYG", None, locals())

    @cmap_docs(MP_NAME, "PRGn")
    def pr_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PRGn", None, locals())

    @cmap_docs(MP_NAME, "RdYlBu")
    def rd_yl_bu(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdYlBu", None, locals())

    @cmap_docs(MP_NAME, "BrBG")
    def br_bg(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BrBG", None, locals())

    @cmap_docs(MP_NAME, "RdGy")
    def rd_gy(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdGy", None, locals())

    @cmap_docs(MP_NAME, "PuOr")
    def pu_or(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuOr", None, locals())

    @cmap_docs(MP_NAME, "Set1")
    def set1(self, *, no_of_colors: int = None,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set1", None, locals())

    @cmap_docs(MP_NAME, "Set2")
    def set2(self, *, no_of_colors: int = 8,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set2", None, locals())

    @cmap_docs(MP_NAME, "Accent")
    def accent(self, *, no_of_colors: int = 8,
               is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Accent", None, locals())

    @cmap_docs(MP_NAME, "Set3")
    def set3(self, *, no_of_colors: int = None,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set3", None, locals())

    @cmap_docs(MP_NAME, "Dark2")
    def dark2(self, *, no_of_colors: int = 8,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Dark2", None, locals())

    @cmap_docs(MP_NAME, "Paired")
    def paired(self, *, no_of_colors: int = None,
               is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Paired", None, locals())

    @cmap_docs(MP_NAME, "Pastel2")
    def pastel2(self, *, no_of_colors: int = 8,
                is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Pastel2", None, locals())

    @cmap_docs(MP_NAME, "Pastel1")
    def pastel1(self, *, no_of_colors: int = None,
                is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Pastel1", None, locals())

    @cmap_docs(MP_NAME, "OrRd")
    def or_rd(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("OrRd", None, locals())

    @cmap_docs(MP_NAME, "PuBU")
    def pu_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuBu", None, locals())

    @cmap_docs(MP_NAME, "BuPu")
    def bu_pu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BuPu", None, locals())

    @cmap_docs(MP_NAME, "BuGn")
    def bu_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BuGn", None, locals())

    @cmap_docs(MP_NAME, "YlOrBr")
    def yl_or_br(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlOrBr", None, locals())

    @cmap_docs(MP_NAME, "YlGn")
    def yl_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlGn", None, locals())

    @cmap_docs(MP_NAME, "RdPu")
    def rd_pu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdPu", None, locals())

    @cmap_docs(MP_NAME, "YlGnBu")
    def yl_gn_bu(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlGnBu", None, locals())

    @cmap_docs(MP_NAME, "GnBu")
    def gn_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("GnBu", None, locals())

    @cmap_docs(MP_NAME, "YlOrRd")
    def yl_or_rd(self, *, no_of_colors: int = 8,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlOrRd", None, locals())

    @cmap_docs(MP_NAME, "PuRd")
    def pu_rd(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuRd", None, locals())

    @cmap_docs(MP_NAME, "PuBuGn")
    def pu_bu_gn(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuBuGn", None, locals())
