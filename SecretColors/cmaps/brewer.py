#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  CMap implementation for Brewer

from SecretColors.data.cmaps.brewer import BREWER_DATA
from SecretColors.data.constants import PALETTE_BREWER
from SecretColors.cmaps.parent import ColorParent
from SecretColors.models.palette import Palette
from SecretColors.helpers.decorators import cmap_docs


class BrewerMap(ColorParent):

    def __init__(self, matplotlib):
        super().__init__(matplotlib)
        self.palette = Palette(PALETTE_BREWER)

    @property
    def data(self):
        return BREWER_DATA

    def _default(self, name, backup, kwargs):
        del kwargs['self']
        if "starting_shade" not in kwargs:
            kwargs["starting_shade"] = None
        if "ending_shade" not in kwargs:
            kwargs["ending_shade"] = None

        no_of_colors = kwargs['no_of_colors'] or 9
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
        no_of_colors = kwargs['no_of_colors'] or 9
        cols = list(self.data[name].keys())
        if 'type' in cols:
            cols.remove('type')
        cols = [int(x) for x in cols]
        if no_of_colors not in cols:
            self.log.error(f"Sorry, for {name} colormap, 'no_of_colors' "
                           f"argument can "
                           f"only take these values: {cols}.")
        return self._default(name, backup, kwargs)

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

    def get(self, name: str, *, no_of_colors: int = None,
            is_qualitative: bool = False, is_reversed=False):
        return self._special_maps(name, None, locals())

    # Other special maps

    @cmap_docs('BrewerMap', "Spectral")
    def spectral(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Spectral", None, locals())

    @cmap_docs('BrewerMap', "RgYlGn")
    def rd_yl_gn(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdYlGn", None, locals())

    @cmap_docs('BrewerMap', "RdBu")
    def rd_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdBu", None, locals())

    @cmap_docs('BrewerMap', "PiYG")
    def pi_yg(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PiYG", None, locals())

    @cmap_docs('BrewerMap', "PRGn")
    def pr_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PRGn", None, locals())

    @cmap_docs('BrewerMap', "RdYlBu")
    def rd_yl_bu(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdYlBu", None, locals())

    @cmap_docs('BrewerMap', "BrBG")
    def br_bg(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BrBG", None, locals())

    @cmap_docs('BrewerMap', "RdGy")
    def rd_gy(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdGy", None, locals())

    @cmap_docs('BrewerMap', "PuOr")
    def pu_or(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuOr", None, locals())

    @cmap_docs('BrewerMap', "Set1")
    def set1(self, *, no_of_colors: int = None,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set1", None, locals())

    @cmap_docs('BrewerMap', "Set2")
    def set2(self, *, no_of_colors: int = 8,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set2", None, locals())

    @cmap_docs('BrewerMap', "Accent")
    def accent(self, *, no_of_colors: int = 8,
               is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Accent", None, locals())

    @cmap_docs('BrewerMap', "Set3")
    def set3(self, *, no_of_colors: int = None,
             is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Set3", None, locals())

    @cmap_docs('BrewerMap', "Dark2")
    def dark2(self, *, no_of_colors: int = 8,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Dark2", None, locals())

    @cmap_docs('BrewerMap', "Paired")
    def paired(self, *, no_of_colors: int = None,
               is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Paired", None, locals())

    @cmap_docs('BrewerMap', "Pastel2")
    def pastel2(self, *, no_of_colors: int = 8,
                is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Pastel2", None, locals())

    @cmap_docs('BrewerMap', "Pastel1")
    def pastel1(self, *, no_of_colors: int = None,
                is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("Pastel1", None, locals())

    @cmap_docs('BrewerMap', "OrRd")
    def or_rd(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("OrRd", None, locals())

    @cmap_docs('BrewerMap', "PuBU")
    def pu_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuBu", None, locals())

    @cmap_docs('BrewerMap', "BuPu")
    def bu_pu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BuPu", None, locals())

    @cmap_docs('BrewerMap', "BuGn")
    def bu_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("BuGn", None, locals())

    @cmap_docs('BrewerMap', "YlOrBr")
    def yl_or_br(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlOrBr", None, locals())

    @cmap_docs('BrewerMap', "YlGn")
    def yl_gn(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlGn", None, locals())

    @cmap_docs('BrewerMap', "RdPu")
    def rd_pu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("RdPu", None, locals())

    @cmap_docs('BrewerMap', "YlGnBu")
    def yl_gn_bu(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlGnBu", None, locals())

    @cmap_docs('BrewerMap', "GnBu")
    def gn_bu(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("GnBu", None, locals())

    @cmap_docs('BrewerMap', "YlOrRd")
    def yl_or_rd(self, *, no_of_colors: int = 8,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("YlOrRd", None, locals())

    @cmap_docs('BrewerMap', "PuRd")
    def pu_rd(self, *, no_of_colors: int = None,
              is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuRd", None, locals())

    @cmap_docs('BrewerMap', "PuBuGn")
    def pu_bu_gn(self, *, no_of_colors: int = None,
                 is_qualitative: bool = False, is_reversed=False):
        return self._special_maps("PuBuGn", None, locals())


def run():
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt
    b = BrewerMap(matplotlib)
    data = np.random.rand(6, 6)
    cmap = b.grays()
    plt.imshow(data, cmap=cmap)
    plt.colorbar()
    plt.show()
