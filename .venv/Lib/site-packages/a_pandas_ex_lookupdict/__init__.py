import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from typing import Union


def get_lookup_dict(df, as_index: list, as_values: Union[list, None] = None) -> dict:
    if not isinstance(as_index, list):
        as_index = [as_index]
    if not as_values:
        as_values = [x for x in df.columns.to_list() if x not in as_index]
    elif not isinstance(as_values, list):
        as_index = [as_values]
    dfn = df.sort_values(by=as_index).reset_index(drop=True)
    nparr = dfn[as_values].__array__()

    indexnumber = dfn.drop_duplicates(subset=as_index, keep="last").index.__array__()
    colors = dfn.drop_duplicates(subset=as_index, keep="last")[as_index].__array__()
    if 0 not in indexnumber:
        indexnumber = np.concatenate([np.array([0]), indexnumber])
    didi = {tuple(colors[ini]): nparr[x:y] for ini, x, y in
        zip(range(len(indexnumber)), indexnumber[:], indexnumber[1:])}
    return didi


def pd_add_lookup_dict():
    DataFrame.d_get_lookup_dict = get_lookup_dict


