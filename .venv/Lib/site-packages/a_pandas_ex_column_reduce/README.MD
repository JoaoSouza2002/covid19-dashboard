# Apply reduce against a whole Pandas Series

```python
pip install a-pandas-ex-column-reduce
```

```python

from a_pandas_ex_column_reduce import pd_add_column_reduce
import pandas as pd
pd_add_column_reduce()
df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)
df = df[:10]
result1 = df.PassengerId.s_column_reduce(
    expression="str(x) +  str(y)",  # the expression has to be passed as a string and must contain x/y
    own_value_against_own_value=True,  # if False: skips when "index of x == index of y"
    ignore_exceptions=True,  # will ignore the execution of the expression and will go on
    print_exceptions=True,
)
print(f"\n\n{result1=}")

result1=0     112345678910
1     212345678910
2     312345678910
3     412345678910
4     512345678910
5     612345678910
6     712345678910
7     812345678910
8     912345678910
9    1012345678910
dtype: object


result2 = df.PassengerId.s_column_reduce(
    expression="x + y",
    own_value_against_own_value=True,
    ignore_exceptions=True,
    print_exceptions=True,
)
print(f"\n\n{result2=}")

result2=0    56
1    57
2    58
3    59
4    60
5    61
6    62
7    63
8    64
9    65
dtype: int64


# Updates the column after each iteration
result3 = df.PassengerId.s_column_reduce_update(
    expression="x + y if y > 5 else x",
    own_value_against_own_value=True,
    ignore_exceptions=True,
    print_exceptions=True,
)


print(f"\n\n{result3=}")


result3=0       41
1       83
2      167
3      335
4      671
5     1343
6     2681
7     5356
8    10705
9    21402
Name: PassengerId, dtype: int64


# If you use a non-built-in function, you have to pass the function as an argument, and use it as "func" in your expression
# An example using shapely (merging different polygons)
from shapely.ops import unary_union
import shapely
polyshape = []
for k in range(10):
    xmin = k * 10 + 5
    ymin = k * 10 + 5
    xmax = k * 20 + 10
    ymax = k * 20 + 10
    coordsalls = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax], [xmin, ymin]]
    po = shapely.geometry.Polygon(coordsalls)
    polyshape.append(po)
	
df2 = pd.DataFrame(polyshape)
print(f"\n\n{df2=}")
dfj = df2[0].s_column_reduce(
    expression="func([x,y]) if x.intersects(y) else x",
    func=unary_union,
    own_value_against_own_value=True,
    ignore_exceptions=True,
)
print(f"\n\n{dfj=}")
dfj2 = df2[0].s_column_reduce_update(
    expression="func([x,y]) if x.intersects(y) else x",
    func=unary_union,
    own_value_against_own_value=False,
    ignore_exceptions=True,
)
print(f"\n\n{dfj2=}")


df2=                                                   0
0            POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))
1      POLYGON ((15 15, 30 15, 30 30, 15 30, 15 15))
2      POLYGON ((25 25, 50 25, 50 50, 25 50, 25 25))
3      POLYGON ((35 35, 70 35, 70 70, 35 70, 35 35))
4      POLYGON ((45 45, 90 45, 90 90, 45 90, 45 45))
5  POLYGON ((55 55, 110 55, 110 110, 55 110, 55 55))
6  POLYGON ((65 65, 130 65, 130 130, 65 130, 65 65))
7  POLYGON ((75 75, 150 75, 150 150, 75 150, 75 75))
8  POLYGON ((85 85, 170 85, 170 170, 85 170, 85 85))
9  POLYGON ((95 95, 190 95, 190 190, 95 190, 95 95))

dfj=0              POLYGON ((5 5, 5 10, 10 10, 10 5, 5 5))
1    POLYGON ((55 90, 55 110, 65 110, 65 130, 75 13...
2    POLYGON ((45 90, 55 90, 55 110, 65 110, 65 130...
3    POLYGON ((55 90, 55 110, 65 110, 65 130, 75 13...
4    POLYGON ((35 70, 45 70, 45 90, 55 90, 55 110, ...
5    POLYGON ((45 70, 45 90, 55 90, 55 110, 65 110,...
6    POLYGON ((45 70, 45 90, 55 90, 55 110, 65 110,...
7    POLYGON ((45 90, 55 90, 55 110, 65 110, 65 130...
8    POLYGON ((90 55, 90 45, 45 45, 45 90, 55 90, 5...
9    POLYGON ((130 65, 110 65, 110 55, 55 55, 55 11...
dtype: object

dfj2=0              POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))
1    POLYGON ((45 70, 45 90, 55 90, 55 110, 65 110,...
2    POLYGON ((90 45, 70 45, 70 35, 50 35, 50 25, 3...
3    POLYGON ((90 45, 70 45, 70 35, 50 35, 50 25, 3...
4    POLYGON ((90 45, 70 45, 70 35, 50 35, 50 25, 3...
5    POLYGON ((90 45, 70 45, 70 35, 50 35, 50 25, 3...
6    POLYGON ((50 25, 30 25, 30 15, 15 15, 15 30, 2...
7    POLYGON ((85 150, 85 170, 95 170, 95 190, 190 ...
8    POLYGON ((85 150, 85 170, 95 170, 95 190, 190 ...
9    POLYGON ((85 150, 85 170, 95 170, 95 190, 190 ...
Name: 0, dtype: object
```
