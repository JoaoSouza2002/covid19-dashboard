# Edit bluestacks.conf with pandas  

## pip install a-pandas-ex-bstcfg2df

### Tested against BlueStacks 5.10

```python
from a_pandas_ex_bstcfg2df import get_bst_config_df, write_df_to_bstcfg
df = get_bst_config_df(conffile=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf")
print(df)
"""
    aa_key_1                     aa_key_2  ... aa_values aa_values_stripped
0        bst        bluestacks_account_id  ...        ""                   
1        bst                campaign_hash  ...        ""                   
2        bst                campaign_name  ...        ""                   
3        bst           custom_resolutions  ...        ""                   
4        bst  feedback_popup_ignored_apps  ...        ""                   
..       ...                          ...  ...       ...                ...
687      bst                     instance  ...   "52383"              52383
688      bst                     instance  ...   "52383"              52383
689      bst                     instance  ...   "52383"              52383
690      bst                     instance  ...   "52383"              52383
691      bst                     instance  ...   "54468"              54468
[692 rows x 7 columns]
"""

write_df_to_bstcfg(
    df,
    conffile=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
    value_column="aa_values",
)
write_df_to_bstcfg(
    df,
    conffile=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
    value_column="aa_values_stripped",
)
```