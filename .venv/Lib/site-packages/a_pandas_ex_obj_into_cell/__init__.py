from typing import Union, Any

from flatten_everything import flatten_everything
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


def get_iat_columns(df, column):
    try:
        return tuple(flatten_everything(np.where(df.columns == column)[0][0]))[0]
    except Exception as fe:
        print(fe)

        return None


def get_iat_index(df, index):
    try:
        return tuple(flatten_everything(np.where(df.index == index)[0][0]))[0]
    except Exception as fe:
        print(fe)
        return None


def put_one_object_into_several_cells(
    dframe: pd.DataFrame,
    column: Union[float, int, str, tuple],
    value: Any,
    indexlist: Union[None, list] = None,
    ffill: bool = False,
    bfill: bool = False,
) -> pd.DataFrame:
    df = dframe.copy()
    if column not in df.columns:
        df[column] = pd.NA
    try:
        df[column] = df[column].astype("object")
    except Exception:
        pass
    if not indexlist:
        idx_col = get_iat_columns(df, column)
        df.iat[0, idx_col] = value
        df[column] = df[column].ffill()
    else:
        sera = pd.Series((value for x in range(len(indexlist))))
        sera.index = indexlist.copy()
        df.loc[indexlist, column] = sera

    if ffill:
        df[column] = df[column].ffill()
    if bfill:
        df[column] = df[column].bfill()
    return df


def put_listitems_into_cells(
    dframe: pd.DataFrame,
    column: Union[float, int, str, tuple],
    values: list,
    indexlist: Union[None, list] = None,
    ffill: bool = False,
    bfill: bool = False,
) -> pd.DataFrame:
    df = dframe.copy()
    if column not in df.columns:
        df[column] = pd.NA
    try:
        df[column] = df[column].astype("object")
    except Exception:
        pass
    idx_col = get_iat_columns(df, column)
    if not indexlist:
        if len(values) == len(df):
            indexlist = df.index.__array__()
    for i, v in zip(indexlist, values):
        i = get_iat_index(df, i)
        df.iat[i, idx_col] = v
    if ffill:
        df[column] = df[column].ffill()
    if bfill:
        df[column] = df[column].bfill()
    return df


def pd_add_obj_into_cells():
    DataFrame.d_one_object_to_several_cells = put_one_object_into_several_cells
    DataFrame.d_list_items_to_cells = put_listitems_into_cells
