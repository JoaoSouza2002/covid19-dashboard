```python
pip install a-pandas-ex-tesseract-multirow-regex-fuzz
```

```python
from a_pandas_ex_tesseract_multirow_regex_fuzz import pd_add_regex_fuzz_multiline,pd_add_tesseract
pd_add_tesseract(tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pd_add_regex_fuzz_multiline()
df=pd.Q_Tesseract_to_DF(r'https://i.ytimg.com/vi/fa82Qpw6lyE/hqdefault.jpg')
```

### Tesseract results in a DataFrame (from url, path, PIL, cv2)

```python
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
```

### Fuzzsearch in multiple rows in a DataFrame - works with any DataFrame, not only tesseract DataFrames

```python
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
```

### Fuzzsearch in multiple rows in a Series - works with any Series, not only tesseract Series

```python
fuzzcolumnsearch = df.text.ds_fuzz_multirow(fuzzsearch='Rocking BAND')
aa_npsum aa_weight  aa_whole_text   aa_whole_text_len aa_whole_text_len_difference
1        180.000000 rockin' band    12                0                              rockin'    90.000000       7         1  180.000000     rockin' band          0                 12                             0
													  0                                 band    90.000000       4         1  180.000000     rockin' band          1                 12                             0
		 130.000000 Playin’ in      10                2                              Playin’    40.000000       7         1  130.000000       Playin’ in         12                 10                             2
													  2                                   in    90.000000       2         1  130.000000       Playin’ in         13                 10                             2
		 122.142857 promise land    12                0                              promise    45.000000       7         1  122.142857     promise land         22                 12                             0
													  0                                 land    77.142857       4         1  122.142857     promise land         23                 12                             0
		 96.428571  Satan! Paid     11                1                               Satan!    45.000000       6         1   96.428571      Satan! Paid         56                 11                             1
		 
```

### Regex search in multiple rows in a DataFrame  - works with any DataFrame, not only tesseract DataFrames Only shows regex results that span over multiple rows!

```python
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

```

### Regex search in multiple rows in a Series  - works with any Series, not only tesseract Series Only shows regex results that span over multiple rows!

```python
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
```
