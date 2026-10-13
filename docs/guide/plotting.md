# Plotting

```{image} ../images/examples-light.png
:class: only-light
:alt: Example plots
```
```{image} ../images/examples-dark.png
:class: only-dark
:alt: Example plots
```

## Make it the default

Set the matplotlib color cycle once, and every plot uses SecretColors.

```python
import matplotlib.pyplot as plt
from cycler import cycler
from SecretColors import Palette

p = Palette()
plt.rcParams["axes.prop_cycle"] = cycler(color=[
    p.blue(shade=60), p.red(), p.teal(), p.purple(shade=60), p.orange()])
```

:::{tip}
This order of IBM colors keeps adjacent series distinguishable for
colorblind readers and has enough contrast on a white background. For dark
backgrounds use `p.blue()`, `p.red()`, `p.teal()`, `p.purple()`,
`p.orange(shade=60)`.
:::

## Single plots

```python
p = Palette()
plt.hist(a, color=p.magenta(), alpha=0.75)
plt.hist(b, color=p.cyan(), alpha=0.75)
plt.plot(x, y, color=p.blue(shade=70))
plt.scatter(x, y, c=p.green(no_of_colors=len(x)))
```

## Other libraries

Colors are plain strings, so they work everywhere.

::::{tab-set}
:::{tab-item} seaborn
```python
import seaborn as sns
sns.set_palette([p.blue(shade=60), p.red(), p.teal()])
sns.heatmap(data, cmap="sc.RdBu")         # after cmaps.register()
```
:::
:::{tab-item} plotly
```python
import plotly.express as px
from SecretColors import cmaps
px.scatter(df, x="x", y="y", color="group",
           color_discrete_sequence=cmaps.colors("tol_bright"))
px.imshow(data, color_continuous_scale=cmaps.colors("RdBu"))
```
:::
:::{tab-item} bokeh
```python
from SecretColors import cmaps
colors = cmaps.colors("Tableau", n=3)
figure.scatter(x, y, color=colors[0])
```
:::
:::{tab-item} altair
```python
import altair as alt
from SecretColors import cmaps
alt.Color("group:N", scale=alt.Scale(range=cmaps.colors("cud")))
```
:::
::::
