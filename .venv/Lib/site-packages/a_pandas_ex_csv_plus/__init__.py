import os
from typing import Union

import regex
from flatten_everything import flatten_everything
from more_itertools import consecutive_groups
import pandas as pd
import numpy as np


def convert_to_df(
    string_table: Union[list, str], regex_sep: str = r"\s+", tolerance: float = 1.0
) -> pd.DataFrame:
    if isinstance(string_table,str):
        if os.path.exists(string_table):
            with open(string_table,mode='r', encoding='utf-8') as f:
                string_table = f.read()
    spareg = regex.compile(regex_sep)
    alltables = string_table
    if not isinstance(alltables, list):
        alltables = [alltables]
    stringtab_split = [y for y in "\n".join(alltables).splitlines() if len(y) > 0]
    malen = np.array(stringtab_split).dtype.itemsize // 4
    stringtab_split = [x.ljust(malen) for x in stringtab_split]
    coua = pd.Series(
        (
            flatten_everything(
                [
                    [tuple(range(*k.span())) for k in spareg.finditer(y)]
                    for y in stringtab_split
                ]
            )
        )
    ).value_counts() / len(stringtab_split)
    coua = coua.to_frame().T
    dae = []
    for col in coua:
        reca = coua.loc[(coua[col] >= tolerance), col]
        la = len(reca)
        if la >= 1:
            dae.append((la, col))

    revas = sorted(dae, reverse=True)
    splittax = sorted([int(x[1]) for x in revas if x[0] == revas[0][0]])

    grono = list([tuple(x) for x in consecutive_groups(splittax)])
    allgu = []
    for _ in stringtab_split:
        start = 0
        gut = ()
        for x in grono:

            for y in x:
                try:
                    gut += (_[start:y],)
                except Exception:
                    gut += ("",)
                start = y
        gut += (_[start:],)
        allgu.append(gut)
    df3 = pd.DataFrame(allgu)
    descri = df3.describe().T
    df3 = (
        df3.T.loc[
            descri.loc[
                ~(
                    (descri["unique"] == 1)
                    & (descri["top"].str.contains(r"^\s*$", regex=True))
                )
            ].index
        ]
        .T.reset_index(drop=True)
        .applymap(str.strip)
        .copy()
    ).astype("string")
    return df3


def pd_add_convert_to_df():
    pd.Q_convert_to_df = convert_to_df
