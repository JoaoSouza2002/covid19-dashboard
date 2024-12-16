from typing import Union, Iterator

import pandas as pd
from pandas.core.frame import DataFrame, Series


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df
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


def pandas_to_tuples(
    dframe: Union[pd.DataFrame, pd.Series], index: bool = True, columns: bool = True
) -> Iterator[tuple]:
    df, isseries = series_to_dataframe(dframe)
    if index is False and columns is True:
        return (
            x[1:]
            for x in [(df.columns[0],) + tuple(df.columns.to_list())]
            + df.to_records().tolist()
        )
    if index is True and columns is True:
        return (
            x
            for x in [("index",) + tuple(df.columns.to_list())]
            + df.to_records().tolist()
        )
    if index is True and columns is False:
        return (x for x in df.to_records().tolist())
    if index is False and columns is False:
        return (x[1:] for x in df.to_records().tolist())


def pd_add_tuples():
    DataFrame.ds_to_tuples = pandas_to_tuples
    Series.ds_to_tuples = pandas_to_tuples

