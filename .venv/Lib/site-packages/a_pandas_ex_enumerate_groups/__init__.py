from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame, Series
from useful_functions_easier_life import ignore_exceptions


def series_to_dataframe_convert(
    df: Union[pd.DataFrame, pd.Series]
) -> (Union[pd.DataFrame, pd.Series], bool):
    isseries_ = False
    dataf = df.copy()
    if isinstance(dataf, pd.Series):
        isseries_ = True
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
    return dataf, isseries_


def enumerate_groups(dframe, enumerated_column, column_to_enumerate):
    col = column_to_enumerate
    gdf, isseries = series_to_dataframe_convert(dframe)
    if isseries:
        col = gdf.columns[0]
    prefix = "XXXXXXXXXgroup_"
    namesep = ""
    return gdf.d_enumerate_groups_in_multiple_columns(
        columns=[[col]], prefix=prefix, name_sep=namesep
    ).rename(columns={f"{prefix}{column_to_enumerate}": enumerated_column})


def enumerate_all_columns_groups(df, prefix="group_"):
    df = df.reset_index(drop=True)
    dftoog = (
        pd.concat(
            [
                df,
                pd.concat(
                    [
                        ignore_exceptions(
                            lambda: df.groupby(col).ngroup(),
                            exception_value=pd.Series([None] * len(df)),
                        )
                        .to_frame()
                        .rename(columns={0: f"{prefix}{col}"})
                        for col in df.columns
                    ],
                    axis=1,
                ),
            ],
            axis=1,
        )
        .copy()
        .fillna(pd.NA)
    )
    return dftoog


def enumerate_multiple_columns(df, columns, prefix="group_", name_sep="_"):
    groupbycolumns = columns.copy()
    # groupbycolumns = [['x', 'y'], ['vor_region', 'vor_vertices', 'vor_vertices_coords']]

    df = df.reset_index(drop=True)
    dftoog = (
        pd.concat(
            [
                df,
                pd.concat(
                    [
                        ignore_exceptions(
                            lambda: df.groupby(col).ngroup(),
                            exception_value=pd.Series([None] * len(df)),
                        )
                        .to_frame()
                        .rename(
                            columns={
                                0: f"{prefix}{f'{name_sep}'.join([str(p) for p in col])}"
                            }
                        )
                        for col in groupbycolumns
                    ],
                    axis=1,
                ),
            ],
            axis=1,
        )
        .copy()
        .fillna(pd.NA)
    )

    return dftoog


def pd_add_enumerate_group():
    DataFrame.ds_enumerate_groups = enumerate_groups
    Series.ds_enumerate_groups = enumerate_groups
    DataFrame.d_enumerate_all_groups_in_all_columns = enumerate_all_columns_groups
    DataFrame.d_enumerate_groups_in_multiple_columns = enumerate_multiple_columns
