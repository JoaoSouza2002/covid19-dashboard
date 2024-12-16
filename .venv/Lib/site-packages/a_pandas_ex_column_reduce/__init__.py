from functools import reduce
import pandas as pd
from pandas.core.frame import Series


def column_reduce_update_each_loop(
    df: pd.Series,
    expression: str, func=None,

        own_value_against_own_value: bool = True,
    ignore_exceptions: bool = True,
    print_exceptions: bool = True,
) -> pd.Series:

    def execute_function(indi0, x, indi1, y, expression, own_value_against_own_value,func):
        try:
            if not own_value_against_own_value:
                if indi0 == indi1:
                    return x

            return eval(expression)
        except Exception as fe:
            if not ignore_exceptions:
                raise fe
            if print_exceptions:
                print(fe)
            return x
    columnsvals = df.copy()
    columnsvals = columnsvals.reset_index(drop=True)
    applyindex = columnsvals.index.copy()
    applycols = columnsvals.copy()

    counter = 0
    for vala in zip(applyindex, applycols):
        x = reduce(
            lambda x, y: execute_function(
                vala[0], x, y[0], y[1], expression, own_value_against_own_value,func
            ),
            zip(applycols.index, columnsvals),
            vala[1],
        )
        columnsvals.iloc[counter] = x
        counter += 1
    columnsvals.index = df.index.__array__().copy()
    return columnsvals


def column_reduce(
    df: pd.Series,
    expression: str,
    func=None,
    own_value_against_own_value: bool = True,
    ignore_exceptions: bool = True,
    print_exceptions: bool = True,
) -> pd.Series:
    def execute_function(indi0, x, indi1, y, expression, own_value_against_own_value,func):
        try:
            if not own_value_against_own_value:
                if indi0 == indi1:
                    return x

            return eval(expression)
        except Exception as fe:
            if not ignore_exceptions:
                raise fe
            if print_exceptions:
                print(fe)
            return x

    columnsvals = df.copy()
    columnsvals = columnsvals.reset_index(drop=True)

    va1 = pd.Series(
        (
            reduce(
                lambda x, y: execute_function(
                    vala[0], x, y[0], y[1], expression, own_value_against_own_value,func
                ),
                zip(columnsvals.index, columnsvals),
                vala[1],
            )
            for vala in zip(columnsvals.index, columnsvals)
        )
    )
    va1.index = df.index.__array__().copy()
    return va1



def pd_add_column_reduce():
    Series.s_column_reduce = column_reduce
    Series.s_column_reduce_update = column_reduce_update_each_loop





