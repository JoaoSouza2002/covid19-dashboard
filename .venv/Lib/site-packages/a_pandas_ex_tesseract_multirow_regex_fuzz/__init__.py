import os
from typing import Union, Any
import more_itertools
import regex
from flatten_everything import flatten_everything
from rapidfuzz import fuzz
import pytesseract
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed
import numpy as np
from pandas.core.frame import DataFrame, Series
pd_add_less_memory_more_speed()
import pandas as pd
import requests

def isurl(url: str) -> bool:
    """Check *url* is URL or not."""
    if url and '://' in url:
        return True
    else:
        return False

def get_tesseract_dataframe(
    img:Any,
    lang:Union[str,None]=None,
    config:str="",
    nice:int=0,
    timeout:int=0,
) -> pd.DataFrame:
    """
    pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pd_add_regex_fuzz_multiline()
    df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')
    """
    if isinstance(img,str):
        if isurl(img):
            req=requests.get(img)
            tmpfilename = os.path.join(os.getcwd(), '___tesseract_tmp_image')
            tmpfilename = tmpfilename + '.' + img.split('.')[-1]
            with open(tmpfilename, mode='wb') as f:
                f.write(req.content)
            img=tmpfilename

    daten = pytesseract.image_to_data(
        img,
        pandas_config={"on_bad_lines": "warn"},
        lang=lang,
        config=config,
        nice=nice,
        timeout=timeout,
    )

    splitted = [x.split("\t") for x in daten.splitlines()]
    header = splitted[0]
    df = pd.DataFrame.from_records(splitted[1:], columns=header)
    df = df.ds_reduce_memory_size(verbose=False).ds_reduce_memory_size(verbose=False)
    return df


def get_rolling_df(df:Union[pd.DataFrame,pd.Series], fuzzsearch:str, column:Union[str,int,float], method:str="weighted") ->list:
    algor = get_algor(partial_full_weighted=method)

    df["aa_weighted"] = (
        df[column]
        .apply(lambda x: algor(x, fuzzsearch))
        .sort_values(ascending=False)
    )
    df["aa_len"] = df[column].str.len()
    alletmp = []
    for rooo in range(1):
        dfrolli = (
            df.rolling(1, win_type="gaussian", closed="neither", center=True)
            .aa_weighted.mean(std=rooo + 1)
            .sort_values(ascending=False)
        )
        dfhelp = df.reindex(dfrolli.index)
        dfhelp = dfhelp.loc[dfhelp["aa_weighted"] != 0]
        alletmp.append(dfhelp)
    return alletmp.copy()


def get_algor(partial_full_weighted: str):
    algor = fuzz.WRatio
    if partial_full_weighted == "full":
        algor = fuzz.ratio
    if partial_full_weighted == "partial":
        algor = fuzz.partial_ratio
    return algor


def permutation_df(rollingdfs, fuzzsearch, column, method="weighted"):
    alletmp = rollingdfs
    checkeddfs = []
    algor = get_algor(partial_full_weighted=method)
    for dfss in alletmp:
        for group in more_itertools.consecutive_groups(
            sorted(list(flatten_everything(dfss.index.to_list())))
        ):
            gruppe = list((group))
            dfslo = dfss.loc[dfss.index.isin(gruppe)].sort_index()
            for grasx in more_itertools.distinct_permutations(
                dfslo[column].to_list(), r=len(fuzzsearch.split())
            ):
                checkeddfs.append(
                    [(y, fu, algor(y, fu)) for y, fu in zip(grasx, fuzzsearch.split())]
                )
    dfxa = pd.DataFrame.from_records(checkeddfs)
    dfxa2 = dfxa.copy()
    return dfxa, dfxa2


def caluculate_fuzz_results(df, dfxa, dfxa2, column):
    dfxa2["aa_complete_string"] = ""
    dfxa2["aa_points"] = 0.0
    for col in dfxa.columns:

        dfxa2["aa_complete_string"] = (
            dfxa2["aa_complete_string"]
            + " "
            + pd.Series([x[0] for x in dfxa[col].__array__()])
        )
        dfxa2["aa_points"] = dfxa2["aa_points"] + pd.Series(
            [x[2] for x in dfxa[col]]
        ).astype("float")
    dfxa2 = dfxa2.sort_values(by="aa_points", ascending=False)
    dfres = [
        [((df.loc[df[column].isin(y)])) for y in dfxa2.aa_complete_string.str.split()]
    ]
    finaldf = [x.drop_duplicates(subset=column).copy() for x in dfres[0]]
    finaldf = pd.concat(
        [
            x.assign(
                aa_npsum=(np.sum(np.diff(x.index))),
                aa_weight=np.sum(x.aa_weighted),
                aa_whole_text=" ".join(x[column].to_list()),
            )
            for x in finaldf
        ]
    )
    finaldf = finaldf.reset_index(drop=True)
    return finaldf.copy()


def adjust_new_old_index(finaldf):
    together = []
    for name, group in finaldf.groupby("aa_whole_text"):
        together.append(group.drop_duplicates().copy())
    indexcounter = 0
    withrightindex = together.copy()
    for ini, to in enumerate(together):
        newindex = list(range(indexcounter, indexcounter + len(to), 1))
        indexcounter = indexcounter + len(to)
        withrightindex[ini]["old_index"] = to.index.__array__().copy()
        withrightindex[ini] = withrightindex[ini].sort_values(by="old_index")
        withrightindex[ini].index = newindex.copy()
    dfjoined = pd.concat(withrightindex)
    return dfjoined.copy()


def use_multiindex(dfjoined, fuzzsearch):
    dfjoined["aa_whole_text_len"] = dfjoined["aa_whole_text"].astype("string").str.len()
    dfjoined["aa_whole_text_len_difference"] = (
        len(fuzzsearch) - dfjoined["aa_whole_text_len"]
    )
    dfjoined["aa_whole_text_len_difference"] = dfjoined[
        "aa_whole_text_len_difference"
    ].abs()
    dfjoined3 = dfjoined.copy()
    muind = pd.MultiIndex.from_frame(
        dfjoined[
            [
                "aa_npsum",
                "aa_weight",
                "aa_whole_text",
                "aa_whole_text_len",
                "aa_whole_text_len_difference",
            ]
        ]
    )
    dfjoined2 = dfjoined.set_index(muind)
    sortedindex = dfjoined2.index.sortlevel([0, 1, 4], [True, False, True])[1]
    dfjoined4 = dfjoined3.reindex(sortedindex)
    dfjoined4 = dfjoined4.reset_index(drop=True)
    muind2 = pd.MultiIndex.from_frame(
        dfjoined4[
            [
                "aa_npsum",
                "aa_weight",
                "aa_whole_text",
                "aa_whole_text_len",
                "aa_whole_text_len_difference",
            ]
        ]
    )
    dfjoined4 = dfjoined4.set_index(muind2)
    return dfjoined4.copy()

def fuzz_multiple_lines_series(df:Union[pd.Series,pd.DataFrame], fuzzsearch:str, method:str="weighted") -> pd.DataFrame:
    r"""
    pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pd_add_regex_fuzz_multiline()
    df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')

        level  page_num  block_num  par_num  ...  width  height       conf      text
    0       1         1          0        0  ...    480     360         -1
    1       2         1          1        0  ...    275     177         -1
    2       3         1          1        1  ...    258     109         -1
    3       4         1          1        1  ...    222      19         -1
    4       5         1          1        1  ...     23      14  95.939438        No
    5       5         1          1        1  ...     33      16  96.663704      stop
    6       5         1          1        1  ...     42      18  93.283119    signs,
    7       5         1          1        1  ...     65      19  82.424248  speedin'
    8       5         1          1        1  ...     37      15  96.098083     limit
    9       4         1          1        1  ...    245      19         -1
    10      5         1          1        1  ...     74      19  79.710175  Nobody's
    11      5         1          1        1  ...     49      14  95.714142     gonna
    12      5         1          1        1  ...     37      14  96.856789      slow
    13      5         1          1        1  ...     24       9  95.754181        me
    14      5         1          1        1  ...     43      14  96.090439      down
    15      4         1          1        1  ...    209      19         -1
    16      5         1          1        1  ...     32      15  96.436874      Like
    17      5         1          1        1  ...      8      10  96.436874         a
    18      5         1          1        1  ...     49      18  94.924347    wheel,
    19      5         1          1        1  ...     49      14  92.669563     gonna
    20      5         1          1        1  ...     32      18  96.724014      spin
    21      5         1          1        1  ...     12      14  95.647652        it


    fuzzcolumnsearch = df.text.ds_fuzz_multirow(fuzzsearch='Rocking BAND')
    aa_npsum aa_weight  aa_whole_text   aa_whole_text_len aa_whole_text_len_difference
    1        180.000000 rockin' band    12                0                              rockin'    90.000000       7         1  180.000000     rockin' band          0                 12                             0
                                                          0                                 band    90.000000       4         1  180.000000     rockin' band          1                 12                             0
             130.000000 Playin’ in      10                2                              Playin’    40.000000       7         1  130.000000       Playin’ in         12                 10                             2
                                                          2                                   in    90.000000       2         1  130.000000       Playin’ in         13                 10                             2
             122.142857 promise land    12                0                              promise    45.000000       7         1  122.142857     promise land         22                 12                             0
                                                          0                                 land    77.142857       4         1  122.142857     promise land         23                 12                             0
             96.428571  Satan! Paid     11                1                               Satan!    45.000000       6         1   96.428571      Satan! Paid         56                 11                             1

    """
    df2, isseries = series_to_dataframe(df)
    column= df2.columns[0]
    return fuzz_multiple_lines(df=df2, column=column, fuzzsearch=fuzzsearch, method=method)


def fuzz_multiple_lines(df:Union[pd.Series,pd.DataFrame],column:Union[str,int,bool], fuzzsearch:str, method:str="weighted") -> pd.DataFrame:
    r"""
    pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pd_add_regex_fuzz_multiline()
    df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')

        level  page_num  block_num  par_num  ...  width  height       conf      text
    0       1         1          0        0  ...    480     360         -1
    1       2         1          1        0  ...    275     177         -1
    2       3         1          1        1  ...    258     109         -1
    3       4         1          1        1  ...    222      19         -1
    4       5         1          1        1  ...     23      14  95.939438        No
    5       5         1          1        1  ...     33      16  96.663704      stop
    6       5         1          1        1  ...     42      18  93.283119    signs,
    7       5         1          1        1  ...     65      19  82.424248  speedin'
    8       5         1          1        1  ...     37      15  96.098083     limit
    9       4         1          1        1  ...    245      19         -1
    10      5         1          1        1  ...     74      19  79.710175  Nobody's
    11      5         1          1        1  ...     49      14  95.714142     gonna
    12      5         1          1        1  ...     37      14  96.856789      slow
    13      5         1          1        1  ...     24       9  95.754181        me
    14      5         1          1        1  ...     43      14  96.090439      down
    15      4         1          1        1  ...    209      19         -1
    16      5         1          1        1  ...     32      15  96.436874      Like
    17      5         1          1        1  ...      8      10  96.436874         a
    18      5         1          1        1  ...     49      18  94.924347    wheel,
    19      5         1          1        1  ...     49      14  92.669563     gonna
    20      5         1          1        1  ...     32      18  96.724014      spin
    21      5         1          1        1  ...     12      14  95.647652        it


    fuzzdfsearch = df.ds_fuzz_multirow(column='text',fuzzsearch='Rocking BAND')

                                                                                        level  page_num  block_num  par_num  line_num  word_num  left  top  width  height       conf      text  aa_weighted  aa_len  aa_npsum   aa_weight    aa_whole_text  old_index  aa_whole_text_len  aa_whole_text_len_difference
    aa_npsum aa_weight  aa_whole_text   aa_whole_text_len aa_whole_text_len_difference
    1        180.000000 rockin' band    12                0                                 5         1          1        2         1         4   128  194     55      14  86.868996   rockin'    90.000000       7         1  180.000000     rockin' band          0                 12                             0
                                                          0                                 5         1          1        2         1         5   188  194     40      14  96.840813      band    90.000000       4         1  180.000000     rockin' band          1                 12                             0
             130.000000 Playin’ in      10                2                                 5         1          1        2         1         1    37  194     53      19  41.302063   Playin’    40.000000       7         1  130.000000       Playin’ in         12                 10                             2
                                                          2                                 5         1          1        2         1         2    95  194     14      14  95.126900        in    90.000000       2         1  130.000000       Playin’ in         13                 10                             2
             122.142857 promise land    12                0                                 5         1          1        4         1         7   207  239     64      19  95.758591   promise    45.000000       7         1  122.142857     promise land         22                 12                             0
                                                          0                                 5         1          1        4         1         8   276  239     36      14  89.825577      land    77.142857       4         1  122.142857     promise land         23                 12                             0
             96.428571  Satan! Paid     11                1                                 5         1          1        1         5         2    74  172     49      14  96.457039    Satan!    45.000000       6         1   96.428571      Satan! Paid         56                 11                             1
                                                          1                                 5         1          1        1         5         3   128  171     34      15  96.457039      Paid    51.428571       4         1   96.428571      Satan! Paid         57                 11                             1
             93.857143  spin it         7                 5                                 5         1          1        1         3         5   197  127     32      18  96.724014      spin    48.857143       4         1   93.857143          spin it         60                  7                             5
                                                          5                                 5         1          1        1         3         6   234  127     12      14  95.647652        it    45.000000       2         1   93.857143          spin it         61                  7                             5
             90.000000  Look at         7                 5                                 5         1          1        3         1         3   134  216     38      15  96.986824      Look    45.000000       4         1   90.000000          Look at         28                  7                             5
                                                          5                                 5         1          1        3         1         4   177  219     15      12  95.994835        at    45.000000       2         1   90.000000          Look at         29                  7                             5
             84.428571  Like a          6                 6                                 5         1          1        1         3         1    37  126     32      15  96.436874      Like    24.428571       4         1   84.428571           Like a         24                  6                             6
                                                          6                                 5         1          1        1         3         2    74  131      8      10  96.436874         a    60.000000       1         1   84.428571           Like a         25                  6                             6
             79.200000  way to          6                 6                                 5         1          1        4         1         4   123  244     30      14  96.982368       way    34.200000       3         1   79.200000           way to         54                  6                             6
                                                          6                                 5         1          1        4         1         5   158  241     15      12  96.969261        to    45.000000       2         1   79.200000           way to         55                  6                             6
             76.950000  signs, speedin' 15                3                                 5         1          1        1         1         3   104   82     42      18  93.283119    signs,    42.750000       6         1   76.950000  signs, speedin'         62                 15                             3
                                                          3                                 5         1          1        1         1         4   152   81     65      19  82.424248  speedin'    34.200000       8         1   76.950000  signs, speedin'         63                 15                             3
             75.461538  Nobody's gonna  14                2                                 5         1          1        1         2         1    37  104     74      19  79.710175  Nobody's    39.461538       8         1   75.461538   Nobody's gonna         32                 14                             2
                                                          2                                 5         1          1        1         2         2   115  109     49      14  95.714142     gonna    36.000000       5         1   75.461538   Nobody's gonna         33                 14                             2
             75.000000  No stop         7                 5                                 5         1          1        1         1         1    37   82     23      14  95.939438        No    45.000000       2         1   75.000000
    """

    dfd = df.copy()
    alletmp = get_rolling_df(dfd, fuzzsearch, column=column, method=method)
    dfxa, dfxa2 = permutation_df(
        rollingdfs=alletmp, fuzzsearch=fuzzsearch, column=column, method=method
    )
    finaldf = caluculate_fuzz_results(dfd, dfxa, dfxa2, column=column)
    dfjoined = adjust_new_old_index(finaldf)
    df = use_multiindex(dfjoined, fuzzsearch)
    return df


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


def regex_multiline_dataframe_search_series(
    df_:Union[pd.Series,pd.DataFrame], regular_expression:str, flags:int=regex.UNICODE,separator_for_group_matches:str="Ç"
) -> pd.DataFrame:
    r"""
    pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pd_add_regex_fuzz_multiline()
    df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')

        level  page_num  block_num  par_num  ...  width  height       conf      text
    0       1         1          0        0  ...    480     360         -1
    1       2         1          1        0  ...    275     177         -1
    2       3         1          1        1  ...    258     109         -1
    3       4         1          1        1  ...    222      19         -1
    4       5         1          1        1  ...     23      14  95.939438        No
    5       5         1          1        1  ...     33      16  96.663704      stop
    6       5         1          1        1  ...     42      18  93.283119    signs,
    7       5         1          1        1  ...     65      19  82.424248  speedin'
    8       5         1          1        1  ...     37      15  96.098083     limit
    9       4         1          1        1  ...    245      19         -1
    10      5         1          1        1  ...     74      19  79.710175  Nobody's
    11      5         1          1        1  ...     49      14  95.714142     gonna
    12      5         1          1        1  ...     37      14  96.856789      slow
    13      5         1          1        1  ...     24       9  95.754181        me
    14      5         1          1        1  ...     43      14  96.090439      down
    15      4         1          1        1  ...    209      19         -1
    16      5         1          1        1  ...     32      15  96.436874      Like
    17      5         1          1        1  ...      8      10  96.436874         a
    18      5         1          1        1  ...     49      18  94.924347    wheel,
    19      5         1          1        1  ...     49      14  92.669563     gonna
    20      5         1          1        1  ...     32      18  96.724014      spin
    21      5         1          1        1  ...     12      14  95.647652        it

    regexcolumnsearch = df.text.ds_regex_multirow( r'Like\s*\b\w+\b')
            text aa_regex_results aa_start aa_end
    0                        <NA>     <NA>   <NA>
    1                        <NA>     <NA>   <NA>
    2                        <NA>     <NA>   <NA>
    3                        <NA>     <NA>   <NA>
    4         No             <NA>     <NA>   <NA>
    5       stop             <NA>     <NA>   <NA>
    6     signs,             <NA>     <NA>   <NA>
    7   speedin'             <NA>     <NA>   <NA>
    8      limit             <NA>     <NA>   <NA>
    9                        <NA>     <NA>   <NA>
    10  Nobody's             <NA>     <NA>   <NA>
    11     gonna             <NA>     <NA>   <NA>
    12      slow             <NA>     <NA>   <NA>
    13        me             <NA>     <NA>   <NA>
    14      down             <NA>     <NA>   <NA>
    15                       <NA>     <NA>   <NA>
    16      Like           Like a       64     70
    17         a           Like a       64     70
    18    wheel,             <NA>     <NA>   <NA>
    19     gonna             <NA>     <NA>   <NA>

    df.text.ds_regex_multirow( r'mess.*dues')

    23  Nobody's                                     <NA>     <NA>   <NA>
    24     gonna                                     <NA>     <NA>   <NA>
    25      mess  mess me ‘round  Hey Satan! Paid my dues      108    147
    26        me  mess me ‘round  Hey Satan! Paid my dues      108    147
    27    ‘round  mess me ‘round  Hey Satan! Paid my dues      108    147
    28            mess me ‘round  Hey Satan! Paid my dues      108    147
    29       Hey  mess me ‘round  Hey Satan! Paid my dues      108    147
    30    Satan!  mess me ‘round  Hey Satan! Paid my dues      108    147
    31      Paid  mess me ‘round  Hey Satan! Paid my dues      108    147
    32        my  mess me ‘round  Hey Satan! Paid my dues      108    147
    33      dues  mess me ‘round  Hey Satan! Paid my dues      108    147
    34                                               <NA>     <NA>   <NA>
    35                                               <NA>     <NA>   <NA>
    36   Playin’                                     <NA>     <NA>   <NA>
    """

    df2, isseries = series_to_dataframe(df_)
    column= df2.columns[0]
    return regex_multiline_dataframe_search(df_=df2, column=column, regular_expression=regular_expression, flags=flags,separator_for_group_matches=separator_for_group_matches)

def regex_multiline_dataframe_search(
    df_:Union[pd.Series,pd.DataFrame], column:str,regular_expression:str, flags:int=regex.UNICODE,separator_for_group_matches:str="Ç"
):
    r"""
    pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pd_add_regex_fuzz_multiline()
    df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')

        level  page_num  block_num  par_num  ...  width  height       conf      text
    0       1         1          0        0  ...    480     360         -1
    1       2         1          1        0  ...    275     177         -1
    2       3         1          1        1  ...    258     109         -1
    3       4         1          1        1  ...    222      19         -1
    4       5         1          1        1  ...     23      14  95.939438        No
    5       5         1          1        1  ...     33      16  96.663704      stop
    6       5         1          1        1  ...     42      18  93.283119    signs,
    7       5         1          1        1  ...     65      19  82.424248  speedin'
    8       5         1          1        1  ...     37      15  96.098083     limit
    9       4         1          1        1  ...    245      19         -1
    10      5         1          1        1  ...     74      19  79.710175  Nobody's
    11      5         1          1        1  ...     49      14  95.714142     gonna
    12      5         1          1        1  ...     37      14  96.856789      slow
    13      5         1          1        1  ...     24       9  95.754181        me
    14      5         1          1        1  ...     43      14  96.090439      down
    15      4         1          1        1  ...    209      19         -1
    16      5         1          1        1  ...     32      15  96.436874      Like
    17      5         1          1        1  ...      8      10  96.436874         a
    18      5         1          1        1  ...     49      18  94.924347    wheel,
    19      5         1          1        1  ...     49      14  92.669563     gonna
    20      5         1          1        1  ...     32      18  96.724014      spin
    21      5         1          1        1  ...     12      14  95.647652        it

    regexdfsearch = df.ds_regex_multirow('text', r'Like\s*\b\w+\b')


        level  page_num  block_num  par_num  line_num  word_num  left  top  width  height       conf      text aa_regex_results aa_start aa_end
    0       1         1          0        0         0         0     0    0    480     360         -1                       <NA>     <NA>   <NA>
    1       2         1          1        0         0         0    37   81    275     177         -1                       <NA>     <NA>   <NA>
    2       3         1          1        1         0         0    37   81    258     109         -1                       <NA>     <NA>   <NA>
    3       4         1          1        1         1         0    37   81    222      19         -1                       <NA>     <NA>   <NA>
    4       5         1          1        1         1         1    37   82     23      14  95.939438        No             <NA>     <NA>   <NA>
    5       5         1          1        1         1         2    66   84     33      16  96.663704      stop             <NA>     <NA>   <NA>
    6       5         1          1        1         1         3   104   82     42      18  93.283119    signs,             <NA>     <NA>   <NA>
    7       5         1          1        1         1         4   152   81     65      19  82.424248  speedin'             <NA>     <NA>   <NA>
    8       5         1          1        1         1         5   222   81     37      15  96.098083     limit             <NA>     <NA>   <NA>
    9       4         1          1        1         2         0    37  104    245      19         -1                       <NA>     <NA>   <NA>
    10      5         1          1        1         2         1    37  104     74      19  79.710175  Nobody's             <NA>     <NA>   <NA>
    11      5         1          1        1         2         2   115  109     49      14  95.714142     gonna             <NA>     <NA>   <NA>
    12      5         1          1        1         2         3   169  104     37      14  96.856789      slow             <NA>     <NA>   <NA>
    13      5         1          1        1         2         4   210  109     24       9  95.754181        me             <NA>     <NA>   <NA>
    14      5         1          1        1         2         5   239  104     43      14  96.090439      down             <NA>     <NA>   <NA>
    15      4         1          1        1         3         0    37  126    209      19         -1                       <NA>     <NA>   <NA>
    16      5         1          1        1         3         1    37  126     32      15  96.436874      Like           Like a       64     70
    17      5         1          1        1         3         2    74  131      8      10  96.436874         a           Like a       64     70

    """
    col = column
    df, isseries = series_to_dataframe(df_)
    dfresult = df.copy()
    dfresult["aa_regex_results"] = pd.NA
    aa_regex_resultsindex = len(dfresult.columns) - 1
    dfresult["aa_start"] = pd.NA
    aa_startindex = len(dfresult.columns) - 1

    dfresult["aa_end"] = pd.NA
    aa_endindex = len(dfresult.columns) - 1
    groupsepi = separator_for_group_matches

    df[col] = df[col].astype("string")
    df["aa_brutto_len"] = df[col].str.len()
    df["aa_text_nonewlines"] = (
        df[col].str.replace("\n", " ", regex=False).str.replace("\r", " ", regex=False)
    )
    df["aa_text_nonewlines"] += " "
    df["aa_netto_len"] = df["aa_text_nonewlines"].str.len()
    df["aa_brutto_len_cumsum"] = df["aa_brutto_len"].cumsum()
    df["aa_netto_len_cumsum"] = df["aa_netto_len"].cumsum()
    regexline = "".join(df["aa_text_nonewlines"].to_list())

    for expre in regex.finditer(regular_expression, regexline,flags=flags):
        for start, end in zip((expre.starts()), (expre.ends())):
            alre = df.loc[
                (df["aa_netto_len_cumsum"] > start)
                & (df["aa_netto_len_cumsum"] < end)
            ]
            ilocindexer = df.index.get_indexer(alre.index).tolist()
            try:
                ilocindexer.append(ilocindexer[-1] + 1)
            except Exception as fe:
                pass
            for locas in ilocindexer:
                dfresult.iat[locas, aa_regex_resultsindex] = f"{groupsepi}".join(
                    [str(x_) for x_ in flatten_everything([expre.captures()])]
                )
                dfresult.iat[locas, aa_startindex] = start
                dfresult.iat[locas, aa_endindex] = end
    return dfresult


def pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = tesseractpath
    pd.Q_Tesseract_to_DF = get_tesseract_dataframe

def pd_add_regex_fuzz_multiline():
    DataFrame.ds_fuzz_multirow = fuzz_multiple_lines
    Series.ds_fuzz_multirow = fuzz_multiple_lines_series
    DataFrame.ds_regex_multirow = regex_multiline_dataframe_search
    Series.ds_regex_multirow = regex_multiline_dataframe_search_series


