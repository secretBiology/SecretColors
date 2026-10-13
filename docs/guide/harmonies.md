# Color harmonies

```{image} ../images/harmonies-light.png
:class: only-light
:alt: Color harmonies
```
```{image} ../images/harmonies-dark.png
:class: only-dark
:alt: Color harmonies
```

{class}`~SecretColors.ColorWheel` finds colors that go well together by
rotating around the color wheel.

```python
from SecretColors import ColorWheel

cw = ColorWheel("#3f51b5")
cw.complementary()          # ['#3f51b5', '#b5a33f']
cw.triadic()                # ['#3f51b5', '#b53f51', '#51b53f']
cw.tetradic()               # 4 colors, 90 degrees apart
cw.analogous()              # ['#3f51b5', '#683fb5', '#a33fb5']
cw.analogous(loc="middle")  # base color in the middle
```

## Adjusting colors

Each adjustment changes the current color. Use `reset()` to go back to the
original.

```python
cw = ColorWheel("#3f51b5")
cw.make_darker(30)
cw.color                    # '#2c397f'
cw.reset()
cw.rotate_hue(180)
cw.color                    # '#b5a33f'
cw.rotate_saturation(-36)   # angles: 360 = 100 %
cw.rotate_lightness(18)     # saturation and lightness stop at 0 % and 100 %
```

## Readable text

```python
ColorWheel("#3f51b5").text_color()      # '#ffffff'
ColorWheel("#ffeb3b").text_color()      # '#000000'
```
