from typing import Union

try:
    import numexpr
except ImportError:
    pass
import numpy as np
import pandas as pd
from a_pandas_ex_obj_into_cell import pd_add_obj_into_cells
from a_pandas_ex_to_tuple import pd_add_tuples

pd_add_tuples()
pd_add_obj_into_cells()


def nearest_color_numexpression(colors, color):
    try:
        f1 = numexpr.evaluate("(sum((colors - color) ** 2, axis=1))")
        return np.sqrt(f1)
    except Exception as fe:
        return np.sqrt(np.sum((colors - color) ** 2, axis=1))


def get_closest_colors(
    wanted_colors: list[tuple],
    colorlist: Union[pd.DataFrame, list],
) -> pd.DataFrame:
    df = colorlist
    if not isinstance(wanted_colors, list):
        wanted_colors = [wanted_colors]
    allresas = []
    if isinstance(df, pd.DataFrame):
        valco = df[["red", "green", "blue"]].value_counts().index.__array__()
    else:
        valco = np.asarray(colorlist)
    colors = np.asarray([np.asarray(l) for l in valco])

    for colortuple in wanted_colors:
        color = np.array(colortuple)
        distances = nearest_color_numexpression(colors, color)
        daxas = pd.concat(
            [pd.DataFrame(colors), pd.DataFrame(distances)], axis=1, ignore_index=True
        ).sort_values(by=3)
        daxas[0] = daxas[0].astype(np.uint8)
        daxas[1] = daxas[1].astype(np.uint8)
        daxas[2] = daxas[2].astype(np.uint8)
        daxas[3] = daxas[3].astype(np.float16)
        daxas.columns = ["r", "g", "b", "rating"]
        daxas = daxas.d_one_object_to_several_cells(
            column="rgb",
            value=colortuple,
            indexlist=None,
            ffill=True,
        )
        allresas.append(daxas.copy())
    daxasfinal = pd.concat(allresas, ignore_index=True)
    return daxasfinal


def pd_add_closest_color():
    pd.Q_find_closest_color = get_closest_colors
