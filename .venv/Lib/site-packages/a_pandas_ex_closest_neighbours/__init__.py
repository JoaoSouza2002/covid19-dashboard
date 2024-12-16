from typing import Union
from a_pandas_ex_less_memory_more_speed import optimize_dtypes
import pandas as pd
from collections import defaultdict
from pandas.core.frame import Series


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def find_neighbours(
    series: pd.Series,
    value: Union[float, int],
    convertdtypes: bool = False,
    accept_exact_match: bool = False,
) -> tuple:
    """

from a_pandas_ex_closest_neighbours import pd_add_closest_neighbours
import pandas as pd
from random import choice  # random dataframe
pd_add_closest_neighbours()
sizes = list(range(1, 100))
df = pd.DataFrame([choice(sizes) for x in range(1000)])
df.columns = ['num']



    df
Out[3]:
     num
0     17
1     32
2     17
3     90
4     76
..   ...
995   69
996   82
997   65
998   84
999   62
[1000 rows x 1 columns]


min_neighbours2, max_neighbours2 = df.num.s_find_closest_neighbours(value=72, convertdtypes=True,
                                                   accept_exact_match=False)
min_neighbours2
Out[8]:
    lower_index  lower_value
0            95           71
1           184           71
2           265           71
3           291           71
4           486           71
5           569           71
6           644           71
7           652           71
8           742           71
9           804           71
10          830           71
11          964           71

max_neighbours2
Out[9]:
    upper_index  upper_value
0            26           73
1            44           73
2           119           73
3           161           73
4           219           73
5           397           73
6           415           73
7           492           73
8           593           73
9           610           73
10          612           73
11          802           73







min_neighbours2, max_neighbours2 = df.num.s_find_closest_neighbours(value=72, convertdtypes=True,
                                                   accept_exact_match=True)

max_neighbours1
Out[4]:
    upper_index  upper_value
0           105           72
1           147           72
2           210           72
3           281           72
4           317           72
5           361           72
6           377           72
7           386           72
8           485           72
9           521           72
10          675           72
11          956           72
12          957           72
min_neighbours1

Out[5]:
    lower_index  lower_value
0           105           72
1           147           72
2           210           72
3           281           72
4           317           72
5           361           72
6           377           72
7           386           72
8           485           72
9           521           72
10          675           72
11          956           72
12          957           72


    Parameters:
        series:pd.Series
            Only pandas.Series
        value:Union[float,int]
            the value you want to have the closest neighbours from
        convertdtypes:bool
            converts string numbers to numbers
            (default=False)
        accept_exact_match:bool
            example:
            True: if you are passing 72, and 72 is in the Series, the minimum and maximum values will be all the same, that means: 72
            False: All cells with 72 are excluded, and you won't see 72 in the results
            (default=False)
    Returns:
        tuple


    """
    nested_dict = lambda: defaultdict(nested_dict)
    nesti = nested_dict()
    df, isseries = series_to_dataframe(series)
    df = df.dropna()
    if convertdtypes:
        df = optimize_dtypes(df, verbose=False)
    colname = df.columns[0]
    mask1 = df[colname] == value
    exactmatch = df[mask1]
    if not exactmatch.empty:
        if accept_exact_match:
            for key, item in exactmatch.iterrows():
                nesti["min"][key] = item[colname]
                nesti["max"][key] = item[colname]
            mindf = (
                pd.Series(nesti["min"])
                .reset_index()
                .rename(columns={"index": "lower_index", 0: "lower_value"})
            )
            maxdf = (
                pd.Series(nesti["max"])
                .reset_index()
                .rename(columns={"index": "upper_index", 0: "upper_value"})
            )

            return mindf, maxdf
        else:
            df = df[~mask1]
    """https://stackoverflow.com/a/53553226/15096247"""
    lowerneighbour_ind = df[df[colname] < value][colname].max()
    upperneighbour_ind = df[df[colname] > value][colname].min()
    lowdf = df.loc[df[colname] == lowerneighbour_ind]
    highdf = df.loc[df[colname] == upperneighbour_ind]
    for key, item in lowdf.iterrows():
        nesti["min"][key] = item[colname]
    for key, item in highdf.iterrows():
        nesti["max"][key] = item[colname]
    mindf = (
        pd.Series(nesti["min"])
        .reset_index()
        .rename(columns={"index": "lower_index", 0: "lower_value"})
    )
    maxdf = (
        pd.Series(nesti["max"])
        .reset_index()
        .rename(columns={"index": "upper_index", 0: "upper_value"})
    )

    return mindf, maxdf


def pd_add_closest_neighbours():
    Series.s_find_closest_neighbours = find_neighbours
