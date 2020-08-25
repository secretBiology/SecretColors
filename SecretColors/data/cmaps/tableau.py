#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#
#  Tableau v9 color maps
#  Hex values taken from their legacy help page
#  https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm#Version_9.x_(legacy)_color_palette_hex_values


TABLEAU_DATA = {
    "Tableau": {"10": ['#17becf', '#bcbd22', '#7f7f7f', '#e377c2', '#8c564b',
                       '#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4'],
                "20": ['#9edae5', '#17becf', '#dbdb8d', '#bcbd22', '#c7c7c7',
                       '#7f7f7f', '#f7b6d2', '#e377c2', '#c49c94', '#8c564b',
                       '#c5b0d5', '#9467bd', '#ff9896', '#d62728', '#98df8a',
                       '#2ca02c', '#ffbb78', '#ff7f0e', '#aec7e8', '#1f77b4'],
                "type": "regular"},
    "Tableau_medium": {"10": ['#6dccda', '#cdcc5d', '#a2a2a2', '#ed97ca',
                              '#a8786e', '#ad8bc9', '#ed665d', '#67bf5c',
                              '#ff9e4a', '#729ece'], "type": "regular"},
    "Tableau_light": {"10": ['#9edae5', '#dbdb8d', '#c7c7c7', '#f7b6d2',
                             '#c49c94', '#c5b0d5', '#ff9896', '#98df8a',
                             '#ffbb78', '#aec7e8'], "type": "regular"},
    "Gray": {"5": ['#cfcfcf', '#8f8782', '#414451', '#a5acaf', '#60636a'],
             "13": ['#1e1e1e', '#282828', '#333333', '#3f3f3f', '#4b4b4b',
                    '#585858', '#666666', '#747474', '#838383', '#929292',
                    '#a2a2a2', '#b2b2b2', '#c3c3c3'], "type": "seq"},
    "ColorBlind": {"10": ['#cfcfcf', '#ffbc79', '#a2c8ec', '#898989',
                          '#c85200', '#5f9ed1', '#595959', '#ababab',
                          '#ff800e', '#006ba4'], "type": "regular"},
    "TrafficLight": {"9": ['#9fcd99', '#ffdd71', '#f26c64', '#69b764',
                           '#ffc156', '#d82526', '#309343', '#dba13a',
                           '#b10318'], "type": "regular"},
    "PurpleGray": {"6": ['#d7d5c5', '#d098ee', '#995688', '#94917b', '#dc5fbd',
                         '#7b66d2'],
                   "12": ['#dbd4c5', '#8b7c6e', '#d098ee', '#ab6ad5',
                          '#d898ba', '#995688', '#b4b19b', '#5f5a41',
                          '#ffc0da', '#dc5fbd', '#a699e8', '#7b66d2'],
                   "type": "regular"},
    "GreenOrange": {"6": ['#b85a0d', '#39737c', '#ffd94a', '#3cb7cc',
                          '#ff7f0f', '#32a251'],
                    "12": ['#ccc94d', '#82853b', '#86b4a9', '#39737c',
                           '#ffd94a', '#b85a0d', '#98d9e4', '#3cb7cc',
                           '#ffb977', '#ff7f0f', '#acd98d', '#32a251'],
                    "type": "regular"},
    "BlueRed": {"6": ['#e9c39b', '#ea6b73', '#6ba3d6', '#ac613c', '#f02720',
                      '#2c69b0'],
                "12": ['#f4737a', '#bd0a36', '#ddc9b4', '#ac8763', '#b5dffd',
                       '#6ba3d6', '#e9c39b', '#ac613c', '#ffb6b0', '#f02720',
                       '#b5c8e2', '#2c69b0'], "type": "regular"},
    "Cyclic": {"13": ['#6f63bb', '#8a60b0', '#ba43b4', '#c7519c', '#d63a3a',
                      '#ff7f0e', '#ffaa0e', '#ffbf50', '#bcbd22', '#78a641',
                      '#2ca030', '#12a2a8', '#1f83b4'], "type": "regular"},
    "Green": {"7": ['#09622a', '#1a7232', '#27823b', '#339444', '#69a761',
                    '#94bb83', '#bccfb4'], "type": "seq"},
    "Blue": {"7": ['#26456e', '#1c5998', '#1c73b1', '#3a87b7', '#67add4',
                   '#7bc8e2', '#b4d4da'], "type": "seq"},
    "Red": {"9": ['#9c0824', '#b10c1d', '#c21417', '#cf1719',
                  '#d8392c', '#e35745', '#f57667', '#f89a90', '#eac0bd'],
            "type": "seq"},
    "Orange": {"7": ['#7b3014', '#a33202', '#d74401', '#f06511',
                     '#fd8938', '#fdab67', '#f0c294'], "type": "seq"},

    "AquaRed": {"11": ['#bd1100', '#c92b14', '#d43e25', '#e04e35', '#ea5e45',
                       '#f46b55', '#fd7864', '#fe8b7a', '#fd9c8f', '#fbb3ab',
                       '#f5cac7'], "type": "seq"},
    "AquaGreen": {"11": ['#3c8200', '#4a8c1c', '#569735', '#60a24d', '#6cae59',
                         '#7abc5f', '#8ac765', '#9ad26d', '#acdc7a', '#c3e394',
                         '#dbe8b4'], "type": "seq"},
    "AquaBrown": {"11": ['#bb5137', '#bb6348', '#bb7359', '#c08262', '#cc8f63',
                         '#d89c63', '#e4aa63', '#f0b763', '#f7c577', '#f6d29c',
                         '#f3e0c2'], "type": "seq"},
    "RedGreen": {"11": ['#09622a', '#1e7735', '#2f8e41', '#69a761', '#a2c18f',
                        '#cacaca', '#fc8375', '#df513f', '#d11719', '#bd1316',
                        '#9c0824'], "type": "div"},
    "RedBlue": {"11": ['#26456e', '#1c5998', '#1c73b1', '#3a87b7', '#67add4',
                       '#cacaca', '#fc8375', '#df513f', '#d11719', '#bd1316',
                       '#9c0824'], "type": "div"},
    "RedBlack": {"11": ['#1e1e1e', '#383838', '#565656', '#777777', '#9b9b9b',
                        '#cacaca', '#fc8375', '#df513f', '#d11719', '#bd1316',
                        '#9c0824'], "type": "div"},
    "AreaRedGreen": {
        "21": ['#4a8c1c', '#559633', '#5ea049', '#69aa56', '#75b65d',
               '#82c162', '#90cb68', '#a0d571', '#b1de7f', '#c7e298',
               '#e9dabe', '#fca294', '#fe8e7e', '#fd7e6b', '#f7705b',
               '#ef654d', '#e6583e', '#dc4930', '#d23a21', '#c82912',
               '#bd1100'], "type": "div"},
    "OrangeBlue": {
        "13": ['#26456e', '#1c5998', '#1c73b1', '#3a87b7', '#67add4',
               '#7bc8e2', '#cacaca', '#fdab67', '#fd8938', '#f06511',
               '#d74401', '#a33202', '#7b3014'], "type": "div"},

    "GreenBlue": {"11": ['#26456e', '#1c5998', '#1c73b1', '#3a87b7', '#67add4',
                         '#cacaca', '#a2c18f', '#69a761', '#2f8e41', '#1e7735',
                         '#09622a'], "type": "div"},
    "RedWhiteGreen": {
        "11": ['#09622a', '#297839', '#428f49', '#74af72', '#b9d7b7',
               '#ffffff', '#fcb4a5', '#e86753', '#cc312b', '#b41f27',
               '#9c0824'], "type": "div"},
    "RedWhiteBlack": {
        "11": ['#1e1e1e', '#393939', '#575757', '#838383', '#bfbfbf',
               '#ffffff', '#fcb4a5', '#e86753', '#cc312b', '#b41f27',
               '#9c0824'], "type": "div"},

    "OrangeWhiteBlue": {
        "11": ['#26456e', '#2e5f8a', '#3679a8', '#6a9ec5', '#b7cde2',
               '#ffffff', '#ffc2a1', '#fb8547', '#d85a13', '#a84415',
               '#7b3014'], "type": "div"},
    "RedWhiteBlack_light": {
        "10": ['#c6c6c6', '#d1d1d1', '#dddddd', '#e8e8e8', '#f3f3f3',
               '#ffffff', '#fff0f0', '#ffe0e1', '#ffd1d3', '#ffc2c5'],
        "type": "div"},
    "OrangeWhiteBlue_light": {
        "11": ['#c4d8f3', '#d0e0f6', '#dce8f8', '#e8effa',
               '#f3f7fd', '#ffffff', '#fff5eb', '#ffead8',
               '#ffe0c5', '#ffd6b1', '#ffcc9e'], "type": "div"},
    "RedWhiteGreen_light": {
        "11": ['#b7e6a7', '#c6ebb8', '#d5f0ca', '#e3f5db', '#f1faed',
               '#ffffff', '#fff0f0', '#ffe0e1', '#ffd1d3', '#ffc2c5',
               '#ffb2b6'], "type": "div"},
    "RedGreen_light": {
        "11": ['#b7e6a7', '#c1e6b4', '#cae6c0', '#d4e6cc', '#dde6d9',
               '#e5e5e5', '#ecdbdc', '#f2d1d2', '#f8c7c9', '#fcbdc0',
               '#ffb2b6'], "type": "div"}

}
