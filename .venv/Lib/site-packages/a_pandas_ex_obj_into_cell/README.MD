# Puts objects into cells / columns of a Pandas Dataframe



```python
pip install a-pandas-ex-obj-into-cell
```
##### Not best (Pandas) practice, but sometimes very useful :)

```python

from a_pandas_ex_obj_into_cell import pd_add_obj_into_cells
import pandas as pd

pd_add_obj_into_cells()
df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)

d1 = df.d_one_object_to_several_cells(
    column="test1",
    value=({1: ("xx", 331, 11)}),
    indexlist=[1, 2, 3, 7],
    ffill=True,
    bfill=True,
)

print(d1)
d2 = df.d_list_items_to_cells(
    column="test2",
    values=[
        [
            1,
            32,
            4,
        ],
        {33: "dfd", 0: [3, 2]},
        4,
        (5, 34),
    ],
    indexlist=[1, 4, 6, 9],
    ffill=False,
    bfill=False,
)
print(d2)


'''     
PassengerId  Survived  Pclass  ... Cabin Embarked                 test1
0              1         0       3  ...   NaN        S  {1: ('xx', 331, 11)}
1              2         1       1  ...   C85        C  {1: ('xx', 331, 11)}
2              3         1       3  ...   NaN        S  {1: ('xx', 331, 11)}
3              4         1       1  ...  C123        S  {1: ('xx', 331, 11)}
4              5         0       3  ...   NaN        S  {1: ('xx', 331, 11)}
..           ...       ...     ...  ...   ...      ...                   ...
886          887         0       2  ...   NaN        S  {1: ('xx', 331, 11)}
887          888         1       1  ...   B42        S  {1: ('xx', 331, 11)}
888          889         0       3  ...   NaN        S  {1: ('xx', 331, 11)}
889          890         1       1  ...  C148        C  {1: ('xx', 331, 11)}
890          891         0       3  ...   NaN        Q  {1: ('xx', 331, 11)}
[891 rows x 13 columns]
     PassengerId  Survived  Pclass  ... Cabin Embarked                   test2
0              1         0       3  ...   NaN        S                    <NA>
1              2         1       1  ...   C85        C              [1, 32, 4]
2              3         1       3  ...   NaN        S                    <NA>
3              4         1       1  ...  C123        S                    <NA>
4              5         0       3  ...   NaN        S  {33: 'dfd', 0: [3, 2]}
..           ...       ...     ...  ...   ...      ...                     ...
886          887         0       2  ...   NaN        S                     NaN
887          888         1       1  ...   B42        S                     NaN
888          889         0       3  ...   NaN        S                     NaN
889          890         1       1  ...  C148        C                     NaN
890          891         0       3  ...   NaN        Q                     NaN
[891 rows x 13 columns]'''

```
