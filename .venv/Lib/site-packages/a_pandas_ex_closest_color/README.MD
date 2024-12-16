# Calculates the closest colors from 2 lists

```python
pip install a-pandas-ex-closest-color
```

```python

from a_pandas_ex_closest_color import pd_add_closest_color
import pandas as pd
pd_add_closest_color()

colorlist = [
    (0, 0, 0),  # black
    (230, 25, 75),  # red
    (60, 180, 75),  # green
    (255, 225, 25),  # yellow
    (0, 130, 200),  # blue
    (245, 130, 48),  # orange
    (145, 30, 180),  # purple
    (70, 240, 240),  # cyan
    (240, 50, 230),  # magenta
    (210, 245, 60),  # lime
    (250, 190, 190),  # pink
    (0, 128, 128),  # teal
    (230, 190, 255),  # lavender
    (170, 110, 40),  # brown
    (255, 250, 200),  # beige
    (128, 0, 0),  # maroon
    (170, 255, 195),  # mint
    (128, 128, 0),  # olive
    (255, 215, 180),  # coral
    (0, 0, 128),  # navy
    (128, 128, 128),  # grey
    (255, 255, 255),  # white
    (115, 12, 37),  # dark red
    (30, 90, 37),  # dark green
    (127, 112, 12),  # dark yellow
    (0, 65, 100),  # dark blue
    (122, 65, 24),  # dark orange
    (72, 15, 90),  # dark purple
    (35, 120, 120),  # dark cyan
    (120, 25, 115),  # dark magenta
    (105, 122, 30),  # dark lime
    (125, 95, 95),  # dark pink
    (0, 64, 64),  # dark teal
    (115, 95, 127),  # dark lavender
    (85, 55, 20),  # dark brown
    (127, 125, 100),  # dark beige
    (64, 0, 0),  # dark maroon
    (85, 127, 97),  # dark mint
    (64, 64, 0),  # dark olive
    (127, 107, 90),  # dark coral
    (0, 0, 64),  # dark navy
    (64, 64, 64),  # dark grey
]
wanted_colors = [(255, 0, 0), (255, 255, 0), (0, 0, 0)]
df = pd.Q_find_closest_color(wanted_colors=wanted_colors,colorlist=colorlist)
print(df)


       r    g    b    rating          rgb
0    230   25   75   82.9375  (255, 0, 0)
1    128    0    0  127.0000  (255, 0, 0)
2    245  130   48  139.0000  (255, 0, 0)
3    170  110   40  144.6250  (255, 0, 0)
4    115   12   37  145.2500  (255, 0, 0)
..   ...  ...  ...       ...          ...
121  250  190  190  367.0000    (0, 0, 0)
122  255  215  180  379.0000    (0, 0, 0)
123  230  190  255  392.5000    (0, 0, 0)
124  255  250  200  409.2500    (0, 0, 0)
125  255  255  255  441.7500    (0, 0, 0)
[126 rows x 5 columns]


```
