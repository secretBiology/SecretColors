Palette
=======

.. autoclass:: SecretColors.Palette
   :members:
   :exclude-members: get_color_dict, get_color_list

Color objects
-------------

Every color returned by SecretColors is a :class:`ColorString` (or
:class:`ColorTuple` in ``rgb`` / ``rgba`` modes). They behave exactly like
``str`` and ``tuple`` and add a few properties.

.. autoclass:: SecretColors.models.objects.ColorString
   :members: rgb, rgba, rgb255, hsl, hsla, hex, alpha, blend
   :inherited-members:

.. autoclass:: SecretColors.models.objects.ColorTuple

.. autoclass:: SecretColors.models.objects.ColorList
