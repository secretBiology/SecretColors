# Changelog
# v1.2.0
This is one of the major update since the conception of this project. Many
 changes are essential for robust functionality and proper code maintenance
 . This
 has introduced following important changes
 * Probably the most important change in this version is return values. Any
  color you generate with this library will return `ColorString` or
   `ColorTuple` (depending on `color_mode`) which are subclasses of `str` and
    `tuple` respectively. This will NOT change anything in your workflow. Check the full documentation for its
      use cases.
 * `SecretColors.palettes` is now `SecretColors.data.palettes`. However, if
  you have used `from SecretColors import palette`, your code will NOT be
   impacted. We recommend importing this way.
 * `Palette.color_between` is now deprecated. Use `utils.color_in_between
 ` instead. Using this function will raise `AttributeError`.
 * Using shade value less than 0 or greater than 100 will throw a `ValueError`.
 * `allow_gray_shades` argument from `Palette` is deprecated and will be
  ignored.
 * `ignore_gray` and `force_gray` arguments from `Palette.random()` are
  deprecated and will be ignored.
 * `starting_shade` and `ending_shade` values (if not provided by user) will
  be set to minimum and maximum shades available in that palette instead 0
   and 100.
  
 ### Known Issue
**Pycharm type-hinting not working for 'color methods'**

We have shifted to custom decorators for dynamically creating
 documentation of many class methods. However, due to this change
 , Pycharm will not show typehint for 'color methods' It is known [bug
 ](https://youtrack.jetbrains.com/issue/PY-30190) in PyCharm regarding type hinting.