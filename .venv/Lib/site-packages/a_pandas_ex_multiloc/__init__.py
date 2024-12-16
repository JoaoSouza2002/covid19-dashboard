import pandas as pd
from pandas.core.frame import DataFrame


def multiloc(
    dframe: pd.DataFrame,
    column_and_values: list[tuple[str, tuple, tuple[tuple]]],
    query_operator: str = "&",
    print_query=True,
) -> pd.DataFrame:
    df = dframe.fillna(pd.NA).copy()
    wholequery = ""
    columns = column_and_values
    for col in columns:
        operator_ = col[0]
        columnstocheck = col[1]
        valuestocheck = col[2]
        for ini, val_ in enumerate(valuestocheck):
            query = ""
            for ini2, val2_ in enumerate(val_):
                query += f"(df[{repr(columnstocheck[ini2])}] {operator_} {repr(val2_)}){query_operator}"
            query = query.rstrip("|&")
            query = f"({query})"
            query += "|"
            wholequery += query
    wholequery = wholequery.rstrip("|")
    wholequery = wholequery.replace("<NA>", "pd.NA")
    if print_query:
        print(wholequery)
    return df[eval(wholequery)]


def pd_add_multiloc():
    DataFrame.d_multiloc = multiloc


