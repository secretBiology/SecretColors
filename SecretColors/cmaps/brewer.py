#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  CMap implementation for Brewer

from SecretColors.helpers.decorators import deprecated_aliases
from SecretColors.data.cmaps.brewer import BREWER_DATA
from SecretColors.data.constants import PALETTE_BREWER
from SecretColors.cmaps.parent import ColorMapParent
from SecretColors.models.palette import Palette
from SecretColors.helpers.decorators import cmap_docs
from SecretColors.helpers.logging import Log

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
        :emphasize-lines: 4

        import matplotlib.pyplot as plt
        from SecretColors.cmaps import BrewerMap
        bm = BrewerMap()
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

    def __init__(self, matplotlib=None, log: Log = None, seed=None):
        super().__init__(matplotlib, palette=Palette(PALETTE_BREWER),
                         log=log, seed=seed)
        self.n = 9

    @property
    def data(self):
        return BREWER_DATA

    @deprecated_aliases(no_of_colors='n', starting_shade='start', ending_shade='end', is_qualitative='discrete', is_reversed='reverse')
    def greens(self, *, start: float = None,
               end: float = None,
               n: int = None,
               discrete: bool = False,
               reverse=False):
        return self._default("Greens", "green", start=start,
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
        return self._default("Oranges", "orange",
                             start=start,
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
        return self._default("Reds", "red", start=start,
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
        return self._default("Purples", "purple",
                             start=start,
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
        return self._default("Greys", "gray", start=start,
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
        return self._default("Blues", "blue", start=start,
                             end=end,
                             n=n,
                             discrete=discrete,
                             reverse=reverse)

    # Other special maps

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Spectral")
    def spectral(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("Spectral", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RgYlGn")
    def rd_yl_gn(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("RdYlGn", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RdBu")
    def rd_bu(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("RdBu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PiYG")
    def pi_yg(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("PiYG", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PRGn")
    def pr_gn(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("PRGn", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RdYlBu")
    def rd_yl_bu(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("RdYlBu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "BrBG")
    def br_bg(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("BrBG", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RdGy")
    def rd_gy(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("RdGy", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PuOr")
    def pu_or(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("PuOr", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Set1")
    def set1(self, *, n: int = None,
             discrete: bool = False, reverse=False):
        return self._special_maps("Set1", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Set2")
    def set2(self, *, n: int = 8,
             discrete: bool = False, reverse=False):
        return self._special_maps("Set2", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Accent")
    def accent(self, *, n: int = 8,
               discrete: bool = False, reverse=False):
        return self._special_maps("Accent", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Set3")
    def set3(self, *, n: int = None,
             discrete: bool = False, reverse=False):
        return self._special_maps("Set3", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Dark2")
    def dark2(self, *, n: int = 8,
              discrete: bool = False, reverse=False):
        return self._special_maps("Dark2", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Paired")
    def paired(self, *, n: int = None,
               discrete: bool = False, reverse=False):
        return self._special_maps("Paired", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Pastel2")
    def pastel2(self, *, n: int = 8,
                discrete: bool = False, reverse=False):
        return self._special_maps("Pastel2", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "Pastel1")
    def pastel1(self, *, n: int = None,
                discrete: bool = False, reverse=False):
        return self._special_maps("Pastel1", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "OrRd")
    def or_rd(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("OrRd", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PuBU")
    def pu_bu(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("PuBu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "BuPu")
    def bu_pu(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("BuPu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "BuGn")
    def bu_gn(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("BuGn", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "YlOrBr")
    def yl_or_br(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("YlOrBr", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "YlGn")
    def yl_gn(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("YlGn", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "RdPu")
    def rd_pu(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("RdPu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "YlGnBu")
    def yl_gn_bu(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("YlGnBu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "GnBu")
    def gn_bu(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("GnBu", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "YlOrRd")
    def yl_or_rd(self, *, n: int = 8,
                 discrete: bool = False, reverse=False):
        return self._special_maps("YlOrRd", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PuRd")
    def pu_rd(self, *, n: int = None,
              discrete: bool = False, reverse=False):
        return self._special_maps("PuRd", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)

    @deprecated_aliases(no_of_colors='n', is_qualitative='discrete', is_reversed='reverse')
    @cmap_docs(MP_NAME, "PuBuGn")
    def pu_bu_gn(self, *, n: int = None,
                 discrete: bool = False, reverse=False):
        return self._special_maps("PuBuGn", None, n=n,
                                  discrete=discrete,
                                  reverse=reverse)
