#  Copyright (c) SecretBiology  2019.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Main Color file


class ParentPalette:
    """
    Base class to create new colors
    """

    def get_all_colors(self) -> dict:
        """
        :return: get of all colors
        """
        raise NotImplementedError

    def get_palette_name(self) -> str:
        """
        :return: Name of the color palette
        """
        raise NotImplementedError

    def get_creator_url(self) -> str:
        """
        :return: URL of the original resource
        """
        raise NotImplementedError

    def get_shades(self) -> list:
        """
        :return: List of original shades. Note: This will be normalized
        between 0 - 100
        """
        raise NotImplementedError

    def get_core_shade(self) -> int:
        """
        :return: Shade of core color
        """
        raise NotImplementedError

    def get_version(self) -> int:
        """
        :return: Palette version used in this library
        """
        raise NotImplementedError

    def get_last_update(self) -> str:
        """
        :return: Date of last modification happened in this library
        """
        raise NotImplementedError
