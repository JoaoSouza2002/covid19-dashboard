from typing import Union, Any
import pandas as pd
from pandas.core.frame import DataFrame, Series


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


def horizontal_explode(
    dframe: Union[pd.DataFrame, pd.Series], columnname: Any = 0, concat: bool = True
) -> pd.DataFrame:
    def get_item_from_iter(vara, indi):
        try:
            return vara[indi]
        except Exception:
            return pd.NA

    df, isseries = series_to_dataframe(dframe)
    if isseries:
        df.columns = [columnname]
    maxlenaal = df[columnname].dropna().copy()
    maxlenaal = maxlenaal.loc[
        maxlenaal.apply(lambda x: not isinstance(x, (int, float, bool)))
    ]
    maxlena = maxlenaal.apply(len).max()
    collectionofdf = []
    collectionofdfcol = []
    for co in range(maxlena):
        collectionofdf.append(
            df[columnname].apply(lambda x: get_item_from_iter(x, co)).copy()
        )
        collectionofdfcol.append(str(columnname) + "_" + str(co))
    dfe = pd.concat(collectionofdf, axis=1, ignore_index=True).fillna(pd.NA)
    dfe.columns = collectionofdfcol
    if concat:
        return pd.concat([df.copy(), dfe.copy()], axis=1)
    return dfe.copy()


def pd_add_horizontal_explode():
    DataFrame.ds_horizontal_explode = horizontal_explode
    Series.ds_horizontal_explode = horizontal_explode
