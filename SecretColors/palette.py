"""
IBM Palette is taken from
https://github.com/IBM-Design/colors/blob/master/source/colors.js
"""


def int_to_hex(num: int):
    """
    Converts integer to hex. Automatically rounds of the float
    :param num: Integer to be converted
    :return: Hex string
    """
    return hex(int(num)).rstrip("L").lstrip("0x")


def rgb_to_hex(rgb_tuple):
    """
    Converts RGB tuple to hex. Ignores alpha channel
    :param rgb_tuple: RGB tuple .
    :return: Hex color
    """
    return "#" + int_to_hex(rgb_tuple[0]) + int_to_hex(rgb_tuple[1]) + \
           int_to_hex(rgb_tuple[2])


def rgb_to_hsv(rgb_tuple):
    import numpy as np
    """
    Code from https://github.com/matplotlib/
    matplotlib/blob/master/lib/matplotlib/colors.py
    """
    # make sure it is an ndarray
    rgb_tuple = np.asarray(rgb_tuple)

    # check length of the last dimension, should be _some_ sort of rgb
    if rgb_tuple.shape[-1] != 3:
        raise ValueError("Last dimension of input array must be 3; "
                         "shape {} was found.".format(rgb_tuple.shape))

    in_ndim = rgb_tuple.ndim
    if rgb_tuple.ndim == 1:
        rgb_tuple = np.array(rgb_tuple, ndmin=2)

    # make sure we don't have an int image
    rgb_tuple = rgb_tuple.astype(np.promote_types(rgb_tuple.dtype, np.float32))

    out = np.zeros_like(rgb_tuple)
    arr_max = rgb_tuple.max(-1)
    ipos = arr_max > 0
    delta = rgb_tuple.ptp(-1)
    s = np.zeros_like(delta)
    s[ipos] = delta[ipos] / arr_max[ipos]
    ipos = delta > 0
    # red is max
    idx = (rgb_tuple[..., 0] == arr_max) & ipos
    out[idx, 0] = (rgb_tuple[idx, 1] - rgb_tuple[idx, 2]) / delta[idx]
    # green is max
    idx = (rgb_tuple[..., 1] == arr_max) & ipos
    out[idx, 0] = 2. + (rgb_tuple[idx, 2] - rgb_tuple[idx, 0]) / delta[idx]
    # blue is max
    idx = (rgb_tuple[..., 2] == arr_max) & ipos
    out[idx, 0] = 4. + (rgb_tuple[idx, 0] - rgb_tuple[idx, 1]) / delta[idx]

    out[..., 0] = (out[..., 0] / 6.0) % 1.0
    out[..., 1] = s
    out[..., 2] = arr_max

    if in_ndim == 1:
        out.shape = (3,)

    return out[0], out[1], out[2]


def hex_to_rgb(hex_color: str):
    """
    Converts hex color to RGB
    :param hex_color: Color in Hex
    :return: RGB tuple
    """
    if len(hex_color.replace("#", "")) == 8:
        r, g, b, a = [hex_color.replace("#", "")[i:i + 2] for i in
                      range(0, 8, 2)]

        return int(r, 16), int(g, 16), int(b, 16), int(a)
    elif len(hex_color.replace("#", "")) == 6:
        r, g, b = [hex_color.replace("#", "")[i:i + 2] for i in
                   range(0, 6, 2)]

        return int(r, 16), int(g, 16), int(b, 16)
    elif len(hex_color.replace("#", "")) == 3:
        r, g, b = [x for x in hex_color.replace("#", "")]
        return int(r + r, 16), int(g + g, 16), int(b + b, 16)

    else:
        raise Exception("Invalid Hex Code")


def color_in_between(c1, c2, steps=2) -> list:
    """
    Creates color between two colors
    :param c1: Hex of first color
    :param c2: Hex of second color
    :param steps: How many divisions in between? (Default :2)
    :return: List of Colors between provided colors in RGB space
    """
    all_colors = []
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    rdelta, gdelta, bdelta = (r2 - r1) / steps, (g2 - g1) / steps, (
            b2 - b1) / steps
    for step in range(steps - 1):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        all_colors.append(rgb_to_hex((r1, g1, b1)))
    return all_colors


def hex_to_hsv(hex_color: str):
    """
    Converts hex to HSV value
    :param hex_color: Hex color
    :return: HSV tuple
    """
    return rgb_to_hsv(hex_to_rgb(hex_color))


class IBMPalette:
    """
    Class for IBM color palette
    """

    __name = "name"
    __synonyms = "synonyms"
    __core = "core"
    __values = "values"
    __grade = "grade"
    __value = "value"

    __ibm_palette = [
        {
            __name: 'ultramarine',
            __synonyms: ['cool-blue'],
            __core: '60',
            __values: [
                {__grade: '1', __value: 'e7e9f7'},
                {__grade: '10', __value: 'd1d7f4'},
                {__grade: '20', __value: 'b0bef3'},
                {__grade: '30', __value: '89a2f6'},
                {__grade: '40', __value: '648fff'},
                {__grade: '50', __value: '3c6df0'},
                {__grade: '60', __value: '3151b7'},
                {__grade: '70', __value: '2e3f8f'},
                {__grade: '80', __value: '252e6a'},
                {__grade: '90', __value: '20214f'}
            ]
        },
        {
            __name: 'blue',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'e1ebf7'},
                {__grade: '10', __value: 'c8daf4'},
                {__grade: '20', __value: 'a8c0f3'},
                {__grade: '30', __value: '79a6f6'},
                {__grade: '40', __value: '5392ff'},
                {__grade: '50', __value: '2d74da'},
                {__grade: '60', __value: '1f57a4'},
                {__grade: '70', __value: '25467a'},
                {__grade: '80', __value: '1d3458'},
                {__grade: '90', __value: '19273c'}
            ]
        },
        {
            __name: 'cerulean',
            __synonyms: ['warm-blue'],
            __core: '40',
            __values: [
                {__grade: '1', __value: 'deedf7'},
                {__grade: '10', __value: 'c2dbf4'},
                {__grade: '20', __value: '95c4f3'},
                {__grade: '30', __value: '56acf2'},
                {__grade: '40', __value: '009bef'},
                {__grade: '50', __value: '047cc0'},
                {__grade: '60', __value: '175d8d'},
                {__grade: '70', __value: '1c496d'},
                {__grade: '80', __value: '1d364d'},
                {__grade: '90', __value: '1b2834'}
            ]
        },
        {
            __name: 'aqua',
            __core: '30',
            __values: [
                {__grade: '1', __value: 'd1f0f7'},
                {__grade: '10', __value: 'a0e3f0'},
                {__grade: '20', __value: '71cddd'},
                {__grade: '30', __value: '00b6cb'},
                {__grade: '40', __value: '12a3b4'},
                {__grade: '50', __value: '188291'},
                {__grade: '60', __value: '17616b'},
                {__grade: '70', __value: '164d56'},
                {__grade: '80', __value: '13393e'},
                {__grade: '90', __value: '122a2e'}
            ]
        },
        {
            __name: 'teal',
            __core: '40',
            __values: [
                {__grade: '1', __value: 'c0f5e8'},
                {__grade: '10', __value: '8ee9d4'},
                {__grade: '20', __value: '40d5bb'},
                {__grade: '30', __value: '00baa1'},
                {__grade: '40', __value: '00a78f'},
                {__grade: '50', __value: '008673'},
                {__grade: '60', __value: '006456'},
                {__grade: '70', __value: '124f44'},
                {__grade: '80', __value: '133a32'},
                {__grade: '90', __value: '122b26'}
            ]
        },
        {
            __name: 'green',
            __core: '30',
            __values: [
                {__grade: '1', __value: 'cef3d1'},
                {__grade: '10', __value: '89eda0'},
                {__grade: '20', __value: '57d785'},
                {__grade: '30', __value: '34bc6e'},
                {__grade: '40', __value: '00aa5e'},
                {__grade: '50', __value: '00884b'},
                {__grade: '60', __value: '116639'},
                {__grade: '70', __value: '12512e'},
                {__grade: '80', __value: '123b22'},
                {__grade: '90', __value: '112c1b'}
            ]
        },
        {
            __name: 'lime',
            __core: '20',
            __values: [
                {__grade: '1', __value: 'd7f4bd'},
                {__grade: '10', __value: 'b4e876'},
                {__grade: '20', __value: '95d13c'},
                {__grade: '30', __value: '81b532'},
                {__grade: '40', __value: '73a22c'},
                {__grade: '50', __value: '5b8121'},
                {__grade: '60', __value: '426200'},
                {__grade: '70', __value: '374c1a'},
                {__grade: '80', __value: '283912'},
                {__grade: '90', __value: '1f2a10'}
            ]
        },
        {
            __name: 'yellow',
            __core: '10',
            __values: [
                {__grade: '1', __value: 'fbeaae'},
                {__grade: '10', __value: 'fed500'},
                {__grade: '20', __value: 'e3bc13'},
                {__grade: '30', __value: 'c6a21a'},
                {__grade: '40', __value: 'b3901f'},
                {__grade: '50', __value: '91721f'},
                {__grade: '60', __value: '70541b'},
                {__grade: '70', __value: '5b421a'},
                {__grade: '80', __value: '452f18'},
                {__grade: '90', __value: '372118'}
            ]
        },
        {
            __name: 'gold',
            __core: '20',
            __values: [
                {__grade: '1', __value: 'f5e8db'},
                {__grade: '10', __value: 'ffd191'},
                {__grade: '20', __value: 'ffb000'},
                {__grade: '30', __value: 'e39d14'},
                {__grade: '40', __value: 'c4881c'},
                {__grade: '50', __value: '9c6d1e'},
                {__grade: '60', __value: '74521b'},
                {__grade: '70', __value: '5b421c'},
                {__grade: '80', __value: '42301b'},
                {__grade: '90', __value: '2f261c'}
            ]
        },
        {
            __name: 'orange',
            __core: '30',
            __values: [
                {__grade: '1', __value: 'f5e8de'},
                {__grade: '10', __value: 'fdcfad'},
                {__grade: '20', __value: 'fcaf6d'},
                {__grade: '30', __value: 'fe8500'},
                {__grade: '40', __value: 'db7c00'},
                {__grade: '50', __value: 'ad6418'},
                {__grade: '60', __value: '814b19'},
                {__grade: '70', __value: '653d1b'},
                {__grade: '80', __value: '482e1a'},
                {__grade: '90', __value: '33241c'}
            ]
        },
        {
            __name: 'peach',
            __core: '40',
            __values: [
                {__grade: '1', __value: 'f7e7e2'},
                {__grade: '10', __value: 'f8d0c3'},
                {__grade: '20', __value: 'faad96'},
                {__grade: '30', __value: 'fc835c'},
                {__grade: '40', __value: 'fe6100'},
                {__grade: '50', __value: 'c45433'},
                {__grade: '60', __value: '993a1d'},
                {__grade: '70', __value: '782f1c'},
                {__grade: '80', __value: '56251a'},
                {__grade: '90', __value: '3a201b'}
            ]
        },
        {
            __name: 'red',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'f7e6e6'},
                {__grade: '10', __value: 'fccec7'},
                {__grade: '20', __value: 'ffaa9d'},
                {__grade: '30', __value: 'ff806c'},
                {__grade: '40', __value: 'ff5c49'},
                {__grade: '50', __value: 'e62325'},
                {__grade: '60', __value: 'aa231f'},
                {__grade: '70', __value: '83231e'},
                {__grade: '80', __value: '5c1f1b'},
                {__grade: '90', __value: '3e1d1b'}
            ]
        },
        {
            __name: 'magenta',
            __core: '40',
            __values: [
                {__grade: '1', __value: 'f5e7eb'},
                {__grade: '10', __value: 'f5cedb'},
                {__grade: '20', __value: 'f7aac3'},
                {__grade: '30', __value: 'f87eac'},
                {__grade: '40', __value: 'ff509e'},
                {__grade: '50', __value: 'dc267f'},
                {__grade: '60', __value: 'a91560'},
                {__grade: '70', __value: '831b4c'},
                {__grade: '80', __value: '5d1a38'},
                {__grade: '90', __value: '401a29'}
            ]
        },
        {
            __name: 'purple',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'f7e4fb'},
                {__grade: '10', __value: 'efcef3'},
                {__grade: '20', __value: 'e4adea'},
                {__grade: '30', __value: 'd68adf'},
                {__grade: '40', __value: 'cb71d7'},
                {__grade: '50', __value: 'c22dd5'},
                {__grade: '60', __value: '9320a2'},
                {__grade: '70', __value: '71237c'},
                {__grade: '80', __value: '501e58'},
                {__grade: '90', __value: '3b1a40'}
            ]
        },
        {
            __name: 'violet',
            __core: '60',
            __values: [
                {__grade: '1', __value: 'ece8f5'},
                {__grade: '10', __value: 'e2d2f4'},
                {__grade: '20', __value: 'd2b5f0'},
                {__grade: '30', __value: 'bf93eb'},
                {__grade: '40', __value: 'b07ce8'},
                {__grade: '50', __value: '9753e1'},
                {__grade: '60', __value: '7732bb'},
                {__grade: '70', __value: '602797'},
                {__grade: '80', __value: '44216a'},
                {__grade: '90', __value: '321c4c'}
            ]
        },
        {
            __name: 'indigo',
            __core: '70',
            __values: [
                {__grade: '1', __value: 'e9e8ff'},
                {__grade: '10', __value: 'dcd4f7'},
                {__grade: '20', __value: 'c7b6f7'},
                {__grade: '30', __value: 'ae97f4'},
                {__grade: '40', __value: '9b82f3'},
                {__grade: '50', __value: '785ef0'},
                {__grade: '60', __value: '5a3ec8'},
                {__grade: '70', __value: '473793'},
                {__grade: '80', __value: '352969'},
                {__grade: '90', __value: '272149'}
            ]
        },
        {
            __name: 'gray',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'eaeaea'},
                {__grade: '10', __value: 'd8d8d8'},
                {__grade: '20', __value: 'c0bfc0'},
                {__grade: '30', __value: 'a6a5a6'},
                {__grade: '40', __value: '949394'},
                {__grade: '50', __value: '777677'},
                {__grade: '60', __value: '595859'},
                {__grade: '70', __value: '464646'},
                {__grade: '80', __value: '343334'},
                {__grade: '90', __value: '272727'}
            ]
        },
        {
            __name: 'cool-gray',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'e3ecec'},
                {__grade: '10', __value: 'd0dada'},
                {__grade: '20', __value: 'b8c1c1'},
                {__grade: '30', __value: '9fa7a7'},
                {__grade: '40', __value: '8c9696'},
                {__grade: '50', __value: '6f7878'},
                {__grade: '60', __value: '535a5a'},
                {__grade: '70', __value: '424747'},
                {__grade: '80', __value: '343334'},
                {__grade: '90', __value: '272727'}
            ]
        },
        {
            __name: 'warm-gray',
            __core: '50',
            __values: [
                {__grade: '1', __value: 'efe9e9'},
                {__grade: '10', __value: 'e2d5d5'},
                {__grade: '20', __value: 'ccbcbc'},
                {__grade: '30', __value: 'b4a1a1'},
                {__grade: '40', __value: '9e9191'},
                {__grade: '50', __value: '7d7373'},
                {__grade: '60', __value: '5f5757'},
                {__grade: '70', __value: '4b4545'},
                {__grade: '80', __value: '373232'},
                {__grade: '90', __value: '2a2626'}
            ]
        },
        {
            __name: 'neutral-white',
            __core: '1',
            __values: [
                {__grade: '1', __value: 'fcfcfc'},
                {__grade: '2', __value: 'f9f9f9'},
                {__grade: '3', __value: 'f6f6f6'},
                {__grade: '4', __value: 'f3f3f3'}
            ]
        },
        {
            __name: 'cool-white',
            __core: '1',
            __values: [
                {__grade: '1', __value: 'fbfcfc'},
                {__grade: '2', __value: 'f8fafa'},
                {__grade: '3', __value: 'f4f7f7'},
                {__grade: '4', __value: 'f0f4f4'}
            ]
        },
        {
            __name: 'warm-white',
            __core: '1',
            __values: [
                {__grade: '1', __value: 'fdfcfc'},
                {__grade: '2', __value: 'fbf8f8'},
                {__grade: '3', __value: 'f9f6f6'},
                {__grade: '4', __value: 'f6f3f3'}
            ]
        },
        {
            __name: 'black',
            __core: '100',
            __values: [
                {__grade: '100', __value: '000'}
            ]
        },
        {
            __name: 'white',
            __core: '0',
            __values: [
                {__grade: '0', __value: 'fff'}
            ]
        }
    ]

    @property
    def all_colors(self) -> list:
        cols = []
        for c in self.__ibm_palette:
            for m in c[self.__values]:
                cols.append('#' + dict(m)[self.__value])
        return cols

    @property
    def random(self) -> str:
        import random
        obj = self.__ibm_palette[random.randint(0, len(self.__ibm_palette) - 1)]
        for v in obj[self.__values]:
            if obj[self.__core] == dict(v)[self.__grade]:
                return '#' + dict(v)[self.__value]
        return '#000'

    def get(self, color_name: str) -> dict:
        for item in self.__ibm_palette:
            if color_name.lower() == dict(item)[self.__name].lower():
                return item
        import warnings
        warnings.warn("%s : No such color found. Available standard colors "
                      "are ultramarine, blue, cerulean, aqua, teal, green, "
                      "lime, yellow, gold, orange, peach, red, magenta, "
                      "purple, violet, indigo, gray, cool-gray, warm-gray, "
                      "neutral-white, cool-white, warm-white, black, "
                      "white" % color_name)

    @staticmethod
    def __calibrate_grade(grade: int, name: str) -> int:
        if name == 'black':
            return 100
        elif name == 'white':
            return 0
        elif 'white' in name.lower():
            if grade < 1:
                return 1
            elif grade > 4:
                return 4
            else:
                return grade
        elif grade > 90:
            return 90
        elif grade < 1:
            return 1
        else:
            k = grade - (grade % 10)
            return k if k != 0 else 1

    def __get_color(self, color_item: dict, grade: int = None) -> str:
        for v in color_item[self.__values]:
            if grade is None:
                if dict(v)[self.__grade] == color_item[self.__core]:
                    return '#' + dict(v)[self.__value]
            else:
                if dict(v)[self.__grade] == \
                        str(self.__calibrate_grade(grade,
                                                   color_item[self.__name])):
                    return '#' + dict(v)[self.__value]

    def ultramarine(self, grade=None, no_of_colors: int = 1,
                    start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('ultramarine', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('ultramarine'), grade)

    def blue(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('blue', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('blue'), grade)

    def cerulean(self, grade=None, no_of_colors: int = 1,
                 start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('cerulean', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('cerulean'), grade)

    def aqua(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('aqua', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('aqua'), grade)

    def teal(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('teal', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('teal'), grade)

    def green(self, grade=None, no_of_colors: int = 1,
              start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('green', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('green'), grade)

    def lime(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('lime', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('lime'), grade)

    def gold(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('gold', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('gold'), grade)

    def yellow(self, grade=None, no_of_colors: int = 1,
               start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('yellow', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('yellow'), grade)

    def orange(self, grade=None, no_of_colors: int = 1,
               start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('orange', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('orange'), grade)

    def peach(self, grade=None, no_of_colors: int = 1,
              start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('peach', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('peach'), grade)

    def red(self, grade=None, no_of_colors: int = 1,
            start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('red', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('red'), grade)

    def magenta(self, grade=None, no_of_colors: int = 1,
                start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('magenta', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('magenta'), grade)

    def purple(self, grade=None, no_of_colors: int = 1,
               start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('purple', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('purple'), grade)

    def violet(self, grade=None, no_of_colors: int = 1,
               start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('violet', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('violet'), grade)

    def indigo(self, grade=None, no_of_colors: int = 1,
               start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('indigo', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('indigo'), grade)

    def gray(self, grade=None, no_of_colors: int = 1,
             start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('gray', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('gray'), grade)

    def cool_gray(self, grade=None, no_of_colors: int = 1,
                  start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('cool-gray', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('cool-gray'), grade)

    def warm_gray(self, grade=None, no_of_colors: int = 1,
                  start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('warm-gray', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('warm-gray'), grade)

    def neutral_white(self, grade=None, no_of_colors: int = 1,
                      start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('neutral-white', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('neutral-white'), grade)

    def cool_white(self, grade=None, no_of_colors: int = 1,
                   start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('cool-white', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('cool-white'), grade)

    def warm_white(self, grade=None, no_of_colors: int = 1,
                   start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('warm-white', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('warm-white'), grade)

    def black(self, grade=None, no_of_colors: int = 1,
              start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('black', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('black'), grade)

    def white(self, grade=None, no_of_colors: int = 1,
              start_from: int = 1):
        if no_of_colors != 1:
            return self.__uni_default('white', no_of_colors, start_from)
        else:
            return self.__get_color(self.get('white'), grade)

    def random_set_of(self, number: int):
        from random import shuffle
        col = [x for x in self.all_colors]
        all_colors = []
        for i in range(number):
            shuffle(col)
            all_colors.append(col[0])
        return all_colors

    @staticmethod
    def rgb(hex_color: str):
        return hex_to_rgb(hex_color)

    @staticmethod
    def hsv(hex_color: str):
        return rgb_to_hsv(hex_to_rgb(hex_color))

    def uniform_colors(self, number_of_colors: int) -> list:
        c1 = self.random
        c2 = self.random
        all_colors = [c1]
        all_colors.extend(color_in_between(c1, c2, number_of_colors + 1))
        all_colors.append(c2)
        return all_colors

    @staticmethod
    def uniform_colors_between(number_of_colors: int, c1: str, c2: str) -> \
            list:
        all_colors = [c1]
        all_colors.extend(color_in_between(c1, c2, number_of_colors + 1))
        all_colors.append(c2)
        return all_colors

    def __uni_default(self, name, no_of_colors, start_from):
        if start_from > 80:
            c1 = self.__get_color(self.get(name), 80)
        else:
            c1 = self.__get_color(self.get(name), start_from)
        c2 = self.__get_color(self.get(name), 90)
        all_colors = [c1]
        if no_of_colors > 2:
            all_colors.extend(color_in_between(c1, c2, no_of_colors - 1))
        all_colors.append(c2)
        return all_colors
