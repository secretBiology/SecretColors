ColorMaps are essential part of any standard data visualization. Since
beginning of inception of this library, one of the aim was to provide easy
access to diverse colormaps to the users. In this release (v.1.2+), we have
added full support to ColorMaps.

**What is difference between ColorMap and Palette?**

You must have heard of 'color palettes' when you are searching for
good colors on the internet. We have entire class :class:`~SecretColors.Palette`
which is dedicated for generating colors from different standard libraries
and color lists. Then question arises, what are these 'ColorMaps' we are
referring to?

We used word 'ColorMap' to the object which can provide easy access to the
python objects which can be used in various ``matplotlib`` functions.
Matplotlib library uses ``cmap`` (colormaps) in their library. Which are
essentially either :class:`matplotlib.colors.ListedColormap` or
:class:`matplotlib.colors.LinearSegmentedColormap` classes. They provide
nice access to select color based on its value. You can read more about them
on their
`website <https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.colors
.LinearSegmentedColormap.html>`_ .

Hence we have made these ColorMaps which can be directly used in
``matplotlib`` workflow inplace of in-build colormaps. However, it is not
restricted to matplotlib. You can use these object to generate variety of
colors based on value. Or you can just get colors from these ColorMaps and
use them in regular workflow.

**Quick start**

Since v2.0, the simplest way is the functional API in
:mod:`SecretColors.cmaps`. Register all colormaps once and use them by name
anywhere matplotlib colormap names are accepted.

.. code-block:: python

    import matplotlib.pyplot as plt
    from SecretColors import cmaps

    cmaps.register()                         # all maps with 'sc.' prefix
    plt.imshow(data, cmap="sc.greens")
    plt.imshow(data, cmap="sc.Spectral_r")   # reversed version

    plt.imshow(data, cmap=cmaps.cmap("blues", palette="material", start=20))
    cmaps.colors("RdBu", n=7)                # plain hex colors, no matplotlib

The classes described below are still available and work as before.
Passing ``matplotlib`` to them is optional now.
