import itertools
import re
from typing import Union
import pandas as pd
import regex
from a_pandas_ex_less_memory_more_speed import optimize_dtypes
from a_pandas_ex_plode_tool import (
    all_nans_in_df_to_pdNA,
    explode_lists_and_tuples_in_column,
    nested_something_to_df,
)
from a_pandas_ex_df_to_string import ds_to_string
from flatten_everything import flatten_everything
from pandas.core.frame import DataFrame, Series
from a_pandas_ex_string_to_dtypes import convert_stringdf_to_df
import numpy as np


class Trie:
    r"""
    Tr = Trie()
    Tr.trie_regex_from_words(['ich', 'du', 'er', 'sie', 'es', 'wir', 'der', 'die', 'das'])
    text = '.....'
    result = Tr.find(text)
    print(result)
    """

    def __init__(self):
        self.data = {}
        self.union = ""

    def add(self, word: str):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[""] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except Exception:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append("[" + "".join(cc) + "]")

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())

    def trie_regex_from_words(
        self,
        words: list,
        boundary_right: bool = True,
        boundary_left: bool = True,
        capture: bool = False,
        ignorecase: bool = False,
        match_whole_line: bool = False,
    ):
        for word in words:
            self.add(word)
        anfang = ""
        ende = ""
        if match_whole_line is True:
            anfang += r"^\s*"
        if boundary_right is True:
            ende += r"\b"
        if capture is True:
            anfang += "("
        if boundary_left is True:
            anfang += r"\b"
        if capture is True:
            ende += ")"

        if match_whole_line is True:
            ende += r"\s*$"
        if ignorecase is True:
            self.union = regex.compile(anfang + self.pattern() + ende, regex.IGNORECASE)
        else:
            self.union = regex.compile(anfang + self.pattern() + ende)


def trie_regex_search_findall_sub(
    df: Union[pd.DataFrame, pd.Series],
    wordlist: list[str],
    mode: str,
    replace: Union[str, None] = None,
    add_left_to_regex: str = "",
    add_right_to_regex: str = "",
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.Series, pd.DataFrame]:

    trie = Trie()
    trie.trie_regex_from_words(
        words=wordlist,
        boundary_right=False,
        boundary_left=False,
        capture=False,
        match_whole_line=False,
    )
    return regex_findall_to_multiindex_df(
        df,
        regular_expression=add_left_to_regex
        + str(trie.union.pattern)
        + add_right_to_regex,
        flags=flags,
        dtype_string=dtype_string,
        search_or_findall=mode,
        replace=replace,
        line_by_line=line_by_line,
    )



def trie_regex_find_all(
    df: Union[pd.DataFrame, pd.Series],
    wordlist: list[str],
    add_left_to_regex: str = "",
    add_right_to_regex: str = "",
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    r"""

    If you have a huge list of words you want to  search/sub/find_all on this list, you can try to use the Trie regex methods to get the job done faster


    It is worth trying if:
    1) your DataFrame/Series has a lot of text in each cell
    2) you want to search for a lot of words in each cell

    The more words you have, and the more text is in each cell, the faster it gets.
    If you want to know more about, I recommend: https://stackoverflow.com/a/42789508/15096247

    Example:

    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
    allstrings=pd.DataFrame([[df.Name.to_string() *2] *2,[df.Name.to_string() *2] *2]) #lets create a little dataframe with a lot of text in each cell
    hugeregexlist=df.Name.str.extract(r'^\s*(\w+)').drop_duplicates()[0].to_list() #lets get all names (first word) in the titanic DataFrame
    #it should look like that: ['Braund',  'Cumings',  'Heikkinen',  'Futrelle',  'Allen',  'Moran',  'McCarthy',  'Palsson',  'Johnson',  'Nasser' ... ]
    %timeit allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')

    776 ms ± 2.83 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    allstrings.ds_trie_regex_find_all(hugeregexlist, add_left_to_regex=r'\b', add_right_to_regex=r'\b')
    Out[6]:
        result_0 result_1 result_2  ... result_2133 result_2134 result_2135
    0 0   Braund   Harris  Cumings  ...    Johnston        Behr      Dooley
      1   Braund   Harris  Cumings  ...    Johnston        Behr      Dooley
    1 0   Braund   Harris  Cumings  ...    Johnston        Behr      Dooley
      1   Braund   Harris  Cumings  ...    Johnston        Behr      Dooley


    Let's compare with a regular regex search
    hugeregex=r"\b(?:" + "|".join([f'(?:{y})' for y in df.Name.str.extract(r'^\s*(\w+)').drop_duplicates()[0].to_list()]) + r")\b"  #let's create a regex from all names
    #it should look like this: '\\b(?:(?:Braund)|(?:Cumings)|(?:Heikkinen)|(?:Futrelle)|(?:Allen)|(?:Moran)|(?:McCarthy)|(?:Palsson)|(?:Johnson)|(?:Na...
    %timeit allstrings.ds_regex_find_all(hugeregex)

    945 ms ± 3.14 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    That's pretty good, right?

    Another good thing is that you can search in every cell, no matter what dtype it is.
    There won't be thrown any exception, because everything is converted to string before performing any action.
    If you pass "dtype_string=False", each column will be converted to the best available dtype after the actions have been completed

        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            wordlist: list[str]
               All strings you are looking for
            add_left_to_regex: str
                if you want to add something before the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            add_right_to_regex: str
                if you want to add something after the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]

    """
    return trie_regex_search_findall_sub(
        df,
        wordlist=wordlist,
        flags=flags,
        dtype_string=dtype_string,
        add_left_to_regex=add_left_to_regex,
        add_right_to_regex=add_right_to_regex,
        mode="findall",
        replace=None,
        line_by_line=line_by_line,
    )


def trie_regex_search(
    df: Union[pd.DataFrame, pd.Series],
    wordlist: list[str],
    add_left_to_regex: str = "",
    add_right_to_regex: str = "",
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    r"""
    Check out the docs of df.trie_regex_find_all() for detailed information about Trie regex

    Here is one example
    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
    #hugeregexlist = ['Braund',  'Cumings',  'Heikkinen',  'Futrelle',  'Allen',  'Moran',  'McCarthy',  'Palsson',  'Johnson',  'Nasser' ... ]

    allstrings.ds_trie_regex_search(hugeregexlist,line_by_line=True)

    Out[25]:
          result_0
    0 0     Braund
      0    Cumings
      0  Heikkinen
      0   Futrelle
      0      Allen
    ..         ...
    1 1   Montvila
      1     Graham
      1   Johnston
      1       Behr
      1     Dooley
    [7124 rows x 1 columns]

        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            wordlist: list[str]
               All strings you are looking for
            add_left_to_regex: str
                if you want to add something before the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            add_right_to_regex: str
                if you want to add something after the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]

    """
    return trie_regex_search_findall_sub(
        df,
        wordlist=wordlist,
        flags=flags,
        dtype_string=dtype_string,
        add_left_to_regex=add_left_to_regex,
        add_right_to_regex=add_right_to_regex,
        mode="search",
        replace=None,
        line_by_line=line_by_line,
    )


def trie_regex_sub(
    df: Union[pd.DataFrame, pd.Series],
    wordlist: list[str],
    replace: str,
    add_left_to_regex: str = "",
    add_right_to_regex: str = "",
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    r"""
    Check out the docs of df.trie_regex_find_all() for detailed information

    Some examples with DataFrames / Series
    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
    #hugeregexlist = ['Braund',  'Cumings',  'Heikkinen',  'Futrelle',  'Allen',  'Moran',  'McCarthy',  'Palsson',  'Johnson',  'Nasser' ... ]

    df.Name.ds_trie_regex_sub(hugeregexlist, 'HANS',add_left_to_regex=r'^\b',add_right_to_regex=r'\b')

    Out[16]:
                                                     Name
    0                               HANS, Mr. Owen Harris
    1    HANS, Mrs. John Bradley (Florence Briggs Thayer)
    2                                   HANS, Miss. Laina
    3            HANS, Mrs. Jacques Heath (Lily May Peel)
    4                             HANS, Mr. William Henry
    ..                                                ...
    886                                 HANS, Rev. Juozas
    887                        HANS, Miss. Margaret Edith
    888              HANS, Miss. Catherine Helen "Carrie"
    889                             HANS, Mr. Karl Howell
    890                                 HANS, Mr. Patrick
    [891 rows x 1 columns]


    allstrings.ds_trie_regex_search(hugeregexlist,line_by_line=True)

    Out[25]:
          result_0
    0 0     Braund
      0    Cumings
      0  Heikkinen
      0   Futrelle
      0      Allen
    ..         ...
    1 1   Montvila
      1     Graham
      1   Johnston
      1       Behr
      1     Dooley
    [7124 rows x 1 columns]



        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            wordlist: list[str]
               All strings you are looking for
            replace: str
               the replacement you want to use (groups are allowed)
            add_left_to_regex: str
                if you want to add something before the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            add_right_to_regex: str
                if you want to add something after the generated Trie regex -> \b for example
                allstrings.ds_trie_regex_find_all(hugeregexlist,add_left_to_regex=r'\b',add_right_to_regex=r'\b')
               (default  = "")
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]

    """
    return trie_regex_search_findall_sub(
        df,
        wordlist=wordlist,
        flags=flags,
        dtype_string=dtype_string,
        add_left_to_regex=add_left_to_regex,
        add_right_to_regex=add_right_to_regex,
        mode="sub",
        replace=replace,
        line_by_line=line_by_line,
    )


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


def _regex_replace_to_multiindex_df(
    df: Union[pd.DataFrame, pd.Series],
    regular_expression: str,
    replace: str,
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.DataFrame, pd.Series]:
    r"""
    Use regex.sub against a DataFrame/Series without having to fear any exception! You can get
    the results as strings (dtype_string=True) or even as float, int, category (dtype_string=False) - Whatever
    fits best!

    Some examples
    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")


         PassengerId  Survived  Pclass  ...     Fare Cabin  Embarked
    0              1         0       3  ...   7.2500   NaN         S
    1              2         1       1  ...  71.2833   C85         C
    2              3         1       3  ...   7.9250   NaN         S
    3              4         1       1  ...  53.1000  C123         S
    4              5         0       3  ...   8.0500   NaN         S
    ..           ...       ...     ...  ...      ...   ...       ...
    886          887         0       2  ...  13.0000   NaN         S
    887          888         1       1  ...  30.0000   B42         S
    888          889         0       3  ...  23.4500   NaN         S
    889          890         1       1  ...  30.0000  C148         C
    890          891         0       3  ...   7.7500   NaN         Q
    [891 rows x 12 columns]


    subst=df.ds_regex_sub(regular_expression=r'^\b8\d(\d)\b', replace=r'\g<1>00000',dtype_string=False)

    Out[5]:
         PassengerId  Survived  Pclass  ...     Fare Cabin Embarked
    0              1         0       3  ...   7.2500  <NA>        S
    1              2         1       1  ...  71.2833   C85        C
    2              3         1       3  ...   7.9250  <NA>        S
    3              4         1       1  ...  53.1000  C123        S
    4              5         0       3  ...   8.0500  <NA>        S
    ..           ...       ...     ...  ...      ...   ...      ...
    886       700000         0       2  ...  13.0000  <NA>        S
    887       800000         1       1  ...  30.0000   B42        S
    888       900000         0       3  ...  23.4500  <NA>        S
    889            0         1       1  ...  30.0000  C148        C
    890       100000         0       3  ...   7.7500  <NA>        Q
    [891 rows x 12 columns]


    subst.dtypes
    Out[8]:
    PassengerId      uint32
    Survived          uint8
    Pclass            uint8
    Name             string
    Sex            category
    Age              object
    SibSp             uint8
    Parch             uint8
    Ticket           object
    Fare            float64
    Cabin          category
    Embarked       category

    As you can see, the numbers that we have substituted have been converted to int

    Let's do something like math.floor in a very unconventional way :)

    df.Fare
    Out[16]:
    0       7.2500
    1      71.2833
    2       7.9250
    3      53.1000
    4       8.0500
            ...
    886    13.0000
    887    30.0000
    888    23.4500
    889    30.0000
    890     7.7500
    Name: Fare, Length: 891, dtype: float64

    Fareint=df.Fare.ds_regex_sub(r'(\d+)\.\d+$', r'\g<1>',dtype_string=False)

    0       7
    1      71
    2       7
    3      53
    4       8
    ..    ...
    886    13
    887    30
    888    23
    889    30
    890     7

    Fareint.dtypes
    Out[18]:
    Fare    uint16
    #You should not use this method if there are other ways to convert float to int.
    #It serves best for data cleaning, at least that's what I am using it for.

        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            regular_expression: str
               Syntax from https://pypi.org/project/regex/
            replace: str
               the replacement you want to use (groups are allowed)
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]
    """
    return regex_findall_to_multiindex_df(
        df,
        regular_expression,
        flags=flags,
        dtype_string=dtype_string,
        search_or_findall="sub",
        replace=replace,
        line_by_line=line_by_line,
    )


def _regex_search_to_multiindex_df(
    df: Union[pd.DataFrame, pd.Series],
    regular_expression: str,
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.DataFrame, pd.Series]:
    r"""
    Use regex.search against a DataFrame/Series without having to fear any exception! You can get
    the results as strings (dtype_string=True) or even as float, int, category (dtype_string=False) - Whatever
    fits best!

    Some examples

    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")

    multilinetest=df.Name.map(lambda x: f'{x}\n' * 3) #Every name 3x in each cell to test line_by_line

    #using line_by_line=False
    multilinetest.ds_regex_search(regular_expression=r'^.*(\bM\w+\b)\s+(\bW\w+\b)', line_by_line=False, flags=re.IGNORECASE)
    Out[13]:
                                                 result_0
    58  Name           West, Miss. Constance Mirium\nWest
        Name                                       Mirium
        Name                                         West
    426 Name   Clarke, Mrs. Charles V (Ada Maria Winfield
        Name                                        Maria
        Name                                     Winfield
    472 Name       West, Mrs. Edwy Arthur (Ada Mary Worth
        Name                                         Mary
        Name                                        Worth
    862 Name  Swift, Mrs. Frederick Joel (Margaret Welles
        Name                                     Margaret
        Name                                       Welles

    #using line_by_line=True
    multilinetest.ds_regex_search(regular_expression=r'^.*(\bM\w+\b)\s+(\bW\w+\b)', line_by_line=True, flags=re.IGNORECASE)
    Out[19]:
                                                 result_0
    426 Name   Clarke, Mrs. Charles V (Ada Maria Winfield
        Name                                        Maria
        Name                                     Winfield
        Name   Clarke, Mrs. Charles V (Ada Maria Winfield
        Name                                        Maria
        Name                                     Winfield
        Name   Clarke, Mrs. Charles V (Ada Maria Winfield
        Name                                        Maria
        Name                                     Winfield
    472 Name       West, Mrs. Edwy Arthur (Ada Mary Worth
        Name                                         Mary
        Name                                        Worth
        Name       West, Mrs. Edwy Arthur (Ada Mary Worth
        Name                                         Mary
        Name                                        Worth
        Name       West, Mrs. Edwy Arthur (Ada Mary Worth
        Name                                         Mary
        Name                                        Worth
    862 Name  Swift, Mrs. Frederick Joel (Margaret Welles
        Name                                     Margaret
        Name                                       Welles
        Name  Swift, Mrs. Frederick Joel (Margaret Welles
        Name                                     Margaret
        Name                                       Welles
        Name  Swift, Mrs. Frederick Joel (Margaret Welles
        Name                                     Margaret
        Name                                       Welles

    Now, we get a match for each line!

        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            regular_expression: str
               Syntax from https://pypi.org/project/regex/
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]
    """
    return regex_findall_to_multiindex_df(
        df,
        regular_expression,
        flags=flags,
        dtype_string=dtype_string,
        search_or_findall="search",
        line_by_line=line_by_line,
    )


def _regex_findall_to_multiindex_df(
    df: Union[pd.DataFrame, pd.Series],
    regular_expression: str,
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    line_by_line: bool = False,
) -> Union[pd.DataFrame, pd.Series]:
    r"""

    Use regex.findall against a DataFrame/Series without having to fear any exception! You can get
    the results as strings (dtype_string=True) or even as float, int, category (dtype_string=False) - Whatever
    fits best!

    Some examples

    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")


    df.Name.ds_regex_find_all(regular_expression=r'(\bM\w+\b)\s+(\bW\w+\b)')
              result_0  result_1
    426 Name     Maria  Winfield
    472 Name      Mary     Worth
    862 Name  Margaret    Welles

    multilinetest=df.Name.map(lambda x: f'{x}\n' * 3) #Every name 3x in each cell

    multilinetest.ds_regex_find_all(regular_expression=r'^.*(\bM\w+\b)\s+(\bW\w+\b)', line_by_line=False)

    Out[3]:
              result_0  result_1
    58  Name    Mirium      West
    426 Name     Maria  Winfield
    472 Name      Mary     Worth
    862 Name  Margaret    Welles


    multilinetest.ds_regex_find_all(regular_expression=r'^.*(\bM\w+\b)\s+(\bW\w+\b)', line_by_line=True)
    Out[7]:
              result_0  result_1
    426 Name     Maria  Winfield
        Name     Maria  Winfield
        Name     Maria  Winfield
    472 Name      Mary     Worth
        Name      Mary     Worth
        Name      Mary     Worth
    862 Name  Margaret    Welles
        Name  Margaret    Welles
        Name  Margaret    Welles

    By using line_by_line=True you can be sure that the regex engine will check every single line!

        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            regular_expression: str
               Syntax from https://pypi.org/project/regex/
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
            line_by_line:bool
                If you want to split the line before searching. Useful, if you want to use ^....$ more than once.
               (default  =False)
        Returns:
            Union[pd.Series, pd.DataFrame]
    """
    return regex_findall_to_multiindex_df(
        df,
        regular_expression,
        flags=flags,
        dtype_string=dtype_string,
        search_or_findall="findall",
        line_by_line=line_by_line,
    )


def _regex_find_all_with_position_repeated_capture_groups(
    df: Union[pd.DataFrame, pd.Series],
    regular_expression: str,
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
) -> Union[pd.DataFrame, pd.Series]:
    r"""
    Using this method, you can get each match from REPEATED CAPTURE GROUPS! (A very rare feature in regex engines)
    Besides that, you will see the exact position of each group/match.

    df=pd.read_csv( "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")

    special=df.ds_regex_find_all_special(r'\b(Ma(\w)+)(\w+)\b', dtype_string=False)


                                                                           aa_start_0  ... aa_match_6
    aa_index aa_column aa_whole_match aa_whole_start aa_whole_end aa_group             ...
    7        Name      Master         9              15           0                 9  ...        NaN
                                                                  1                 9  ...        NaN
                                                                  2                11  ...        NaN
                                                                  3                14  ...        NaN
    10       Name      Marguerite     17             27           0                17  ...        NaN
                                                                               ...  ...        ...
    885      Name      Margaret       20             28           3                27  ...        NaN
    887      Name      Margaret       14             22           0                14  ...        NaN
                                                                  1                14  ...        NaN
                                                                  2                16  ...        NaN
                                                                  3                21  ...        NaN

    If you use any common regex engine, you can't get the repeated capture groups, since every new result overwrites the old one:
    import re
    re.findall('(Ma(\w)+)', 'Margaret')
    Out[11]: [('Margaret', 't')]

    Using this method you will get all repeated capture groups, they won't be overwritten!

    Results for index 887
                                                                       aa_start_0  aa_start_1  aa_start_2  aa_start_3  aa_start_4  aa_start_5  aa_start_6  aa_stop_0  aa_stop_1  aa_stop_2  aa_stop_3  aa_stop_4  aa_stop_5  aa_stop_6 aa_match_0 aa_match_1 aa_match_2 aa_match_3 aa_match_4 aa_match_5 aa_match_6
    aa_column aa_whole_match aa_whole_start aa_whole_end aa_group
    Name      Margaret       14             22           0                 14        <NA>        <NA>        <NA>        <NA>        <NA>        <NA>         22       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>   Margaret       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>
                                                         1                 14        <NA>        <NA>        <NA>        <NA>        <NA>        <NA>         21       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>    Margare       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>
                                                         2                 16          17          18          19          20        <NA>        <NA>         17         18         19         20         21       <NA>       <NA>          r          g          a          r          e       <NA>       <NA>
                                                         3                 21        <NA>        <NA>        <NA>        <NA>        <NA>        <NA>         22       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>          t       <NA>       <NA>       <NA>       <NA>       <NA>       <NA>


    If you want to convert the results to the best available dtype, use:

    df.ds_regex_find_all_special(r'\b(Ma(\w)+)(\w+)\b', dtype_string=False)

    Out[3]:
                                                                            aa_start_0  ...  aa_match_6
    aa_index aa_column aa_whole_match aa_whole_start aa_whole_end aa_group              ...
    7        Name      Master         9              15           0                  9  ...        <NA>
                                                                  1                  9  ...        <NA>
                                                                  2                 11  ...        <NA>
                                                                  3                 14  ...        <NA>
    10       Name      Marguerite     17             27           0                 17  ...        <NA>
                                                                                ...  ...         ...
    885      Name      Margaret       20             28           3                 27  ...        <NA>
    887      Name      Margaret       14             22           0                 14  ...        <NA>
                                                                  1                 14  ...        <NA>
                                                                  2                 16  ...        <NA>
                                                                  3                 21  ...        <NA>
    [764 rows x 21 columns]


    aa_start_0       uint8
    aa_start_1       Int64
    aa_start_2       Int64
    aa_start_3       Int64
    aa_start_4       Int64
    aa_start_5       Int64
    aa_start_6       Int64
    aa_stop_0        uint8
    aa_stop_1        Int64
    aa_stop_2        Int64
    aa_stop_3        Int64
    aa_stop_4        Int64
    aa_stop_5        Int64
    aa_stop_6        Int64
    aa_match_0    category
    aa_match_1    category
    aa_match_2    category
    aa_match_3    category
    aa_match_4    category
    aa_match_5    category
    aa_match_6    category
        Parameters:
            df: Union[pd.DataFrame, pd.Series]
            regular_expression: str
               Syntax from https://pypi.org/project/regex/
            flags:int
                You can use any flag that is available here: https://pypi.org/project/regex/
               (default  =regex.UNICODE)
            dtype_string:bool
                If True, it returns all results as a string
                If False, data types are converted to the best available
               (default  =True)
        Returns:
            Union[pd.Series, pd.DataFrame]
    """
    df2, isseries = series_to_dataframe(df)
    if isinstance(regular_expression, str):
        regular_expression_ = regex.compile(regular_expression, flags=flags)
    else:
        regular_expression_ = regular_expression
    strdf = ds_to_string(df2).copy()
    allresults = []
    for coltosearch in strdf.columns:

        for ini_, number in zip(strdf[coltosearch].index, strdf[coltosearch]):
            for x in regular_expression_.finditer(number):
                start_ = x.allspans()
                end_ = x.allcaptures()
                tempresult = [
                    list(flatten_everything(list(zip(*y))))
                    for y in list(zip(start_, end_))
                ]
                wend = x.end()
                wstart = x.start()
                for ini, _ in enumerate(tempresult):
                    allresults.append(
                        (
                            {
                                "aa_index": ini_,
                                "aa_column": coltosearch,
                                "aa_whole_match": x.group(),
                                "aa_group": ini,
                                "aa_whole_start": wstart,
                                "aa_whole_end": wend,
                                "aa_start": list(itertools.islice(_, 0, len(_), 3)),
                                "aa_stop": list(itertools.islice(_, 1, len(_), 3)),
                                "aa_match": list(itertools.islice(_, 2, len(_), 3)),
                            }
                        ).copy()
                    )

    dfr = pd.DataFrame.from_records(allresults)

    for col in ["aa_start", "aa_stop", "aa_match"]:
        dfr = (explode_lists_and_tuples_in_column(dfr, col, concat_with_df=True)).drop(
            columns=[col]
        )
    if dtype_string is False:
        dfr = optimize_dtypes(dfr, verbose=False)
    multiind = pd.MultiIndex.from_frame(
        dfr[
            [
                "aa_index",
                "aa_column",
                "aa_whole_match",
                "aa_whole_start",
                "aa_whole_end",
                "aa_group",
            ]
        ].copy()
    )
    dfr = dfr.drop(
        columns=[
            "aa_index",
            "aa_column",
            "aa_whole_match",
            "aa_group",
            "aa_whole_start",
            "aa_whole_end",
        ]
    ).copy()
    dfr = dfr.set_index(multiind)
    if dtype_string is False:
        dfr = optimize_dtypes(dfr, verbose=False)
    return dfr.copy()


def regex_findall_to_multiindex_df(
    df: Union[pd.DataFrame, pd.Series],
    regular_expression: str,
    flags: int = regex.UNICODE,
    dtype_string: bool = True,
    search_or_findall: str = "findall",
    replace: Union[str, None] = None,
    line_by_line: bool = False,
) -> Union[pd.DataFrame, pd.Series]:

    df2, isseries = series_to_dataframe(df)
    if isinstance(regular_expression, str):
        # regular_expression = re.compile(regular_expression)
        regular_expression_ = regex.compile(regular_expression, flags=flags)
    else:
        regular_expression_ = regular_expression
    strdf = ds_to_string(df2).copy()
    allre = []

    def search_instead_of_findall(x):
        if line_by_line:
            z_results = []
            for _ in x.splitlines():
                try:
                    zz_result = regular_expression_.search(_).allcaptures()
                    if zz_result is not None:
                        z_results.extend(zz_result)
                    else:
                        pass
                except Exception:
                    pass
                    continue
            return z_results
        else:
            try:
                return regular_expression_.search(x).allcaptures()
            except Exception:
                return []

    def replace_instead_of_findall(x, replace_):
        if line_by_line:
            z_results = []
            for _ in x.splitlines():
                try:
                    zz_result = regular_expression_.sub(replace_, _)
                    z_results.append(zz_result)
                except Exception:
                    z_results.append("")
                    continue
            return z_results
        else:
            try:
                repl = regular_expression_.sub(replace_, x)
                return [repl]
            except Exception as das:
                return []

    def findall_original(x):
        if line_by_line:
            z_results = []
            for _ in x.splitlines():
                try:
                    zz_result = regular_expression_.findall(_)
                    if any(zz_result):
                        z_results.append(flatten_everything([__ for __ in zz_result]))
                    else:
                        continue
                except Exception:
                    continue
            return z_results
        try:
            repl = regular_expression_.findall(x)
            return repl
        except Exception as das:
            return []

    for col in df2.columns:
        # strdf[col] = strdf[col].str.findall(regular_expression)
        if search_or_findall == "findall":
            strdf[col] = strdf[col].map(lambda x: findall_original(x))
        elif search_or_findall == "search":
            strdf[col] = strdf[col].map(lambda x: search_instead_of_findall(x))
        elif search_or_findall == "sub":
            strdf[col] = strdf[col].map(
                lambda x: replace_instead_of_findall(x, replace)
            )

        # baba.captures()
        df21 = all_nans_in_df_to_pdNA(
            strdf[col].to_frame().rename(columns={0: col}),
            include_na_strings=False,
            include_empty_iters=True,
        )
        try:
            exploded = explode_lists_and_tuples_in_column(df21[col])
            allre.append(exploded.to_frame().copy())
        except Exception:
            allre.append(df21.copy())

    try:
        dfn = nested_something_to_df(allre)
        dfn = dfn.dropna(subset="aa_value").copy().reset_index()
        dfn1 = dfn.set_index(
            pd.MultiIndex.from_tuples([x[1:] for x in dfn.aa_all_keys.to_list()])
        )
        dfn1 = (
            dfn1.drop(columns=([x for x in dfn1.columns if x.startswith("level_")]))
            .drop(columns=["index", "aa_all_keys"])
            .swaplevel(0, 1)
            .unstack()
            .droplevel(0, 1)
            .copy()
        )
        dfn1.columns = [f"result_{x}" for x in dfn1.columns]
        try:
            dfn1 = dfn1.droplevel(2)
        except Exception:
            pass
        if dtype_string is False:
            try:
                dfn1 = convert_stringdf_to_df(dfn1.copy())
            except Exception as f:
                pass
        try:
            if search_or_findall == "sub":
                dfn1 = dfn1.unstack().droplevel(0, 1)
                if not isseries:
                    try:
                        dfn1 = dfn1.filter(df.columns)
                    except Exception:
                        pass
                if dtype_string is False:
                    dfn1 = optimize_dtypes(dfn1, verbose=False)
                return dfn1
        except Exception as F:
            pass
        try:
            if np.sum([list(xaaa) for xaaa in zip(*dfn1.index)][-1]) == 0:
                dfn1 = dfn1.droplevel(-1)
        except Exception as f:
            pass
        return dfn1
    except TypeError:
        return pd.DataFrame()


def pd_add_regex_enhancements():
    DataFrame.ds_trie_regex_search = trie_regex_search
    Series.ds_trie_regex_search = trie_regex_search
    DataFrame.ds_trie_regex_sub = trie_regex_sub
    Series.ds_trie_regex_sub = trie_regex_sub
    DataFrame.ds_trie_regex_find_all = trie_regex_find_all
    Series.ds_trie_regex_find_all = trie_regex_find_all
    DataFrame.ds_regex_find_all = _regex_findall_to_multiindex_df
    Series.ds_regex_find_all = _regex_findall_to_multiindex_df
    DataFrame.ds_regex_find_all_special = _regex_find_all_with_position_repeated_capture_groups
    Series.ds_regex_find_all_special = _regex_find_all_with_position_repeated_capture_groups
    DataFrame.ds_regex_search = _regex_search_to_multiindex_df
    Series.ds_regex_search = _regex_search_to_multiindex_df
    DataFrame.ds_regex_sub = _regex_replace_to_multiindex_df
    Series.ds_regex_sub = _regex_replace_to_multiindex_df

