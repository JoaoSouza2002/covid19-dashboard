import re

from normalize_lists import normalize_lists
import pandas as pd


def decoder(x):
    try:
        return x.decode("utf-8", "ignore")
    except Exception:
        return ""


def get_bst_config_df(conffile=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf"):
    updatedlines = []
    with open(conffile, mode="rb") as f:
        data = f.read()

    updatedlines.extend(
        [
            list(
                (
                    y.split(b"=", maxsplit=1)[-1],
                    *y.split(b"=", maxsplit=1)[0].split(b"."),
                )
            )
            for y in data.splitlines()
        ]
    )
    normli = normalize_lists(*updatedlines, fill_value=None)
    df = pd.DataFrame([[decoder(d) for d in o] for o in normli])
    df = df.rename(columns={0: len(df.columns)})
    df = df.filter((sorted(df.columns))).fillna("")
    df.columns = [f"aa_key_{x}" for x in df.columns[:-1]] + ["aa_values"]
    df["aa_values_stripped"] = df.aa_values.str.strip().str.strip('"')
    return df


def write_df_to_bstcfg(df, conffile, value_column="aa_values"):
    allkeys = [
        re.sub(r"\.+", ".", ".".join(list(i))).strip(".").strip().strip(".")
        for i in zip(
            *[
                df[q].__array__().tolist()
                for q in df[[x for x in df.columns if "key" in x]]
            ]
        )
    ]
    if value_column == "aa_values":
        allvalues = [f"={x}" for x in df[value_column].__array__().tolist()]
    else:
        allvalues = [f'="{x}"' for x in df[value_column].__array__().tolist()]

    newcfg = "\n".join(["".join(list(r)) for r in (zip(allkeys, allvalues))]).strip()
    with open(conffile, mode="w", encoding="utf-8", newline="\n") as f:
        f.write(newcfg)
    return newcfg

