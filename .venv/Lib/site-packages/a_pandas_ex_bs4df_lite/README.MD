# Light version of https://github.com/hansalemaos/a_pandas_ex_bs4df

## Less details, but much faster

### pip install a_pandas_ex_bs4df_lite 

```python
from a_pandas_ex_bs4df_lite import pd_add_bs4_to_df_lite
import pandas as pd
pd_add_bs4_to_df_lite()
df=pd.Q_bs4_to_df_lite(r'https://github.com/search?l=Python&q=python&type=Repositories',parser="lxml", fake_header=True)


     aa_name          aa_contents            aa_parent  aa_previous_element      aa_next_element aa_next_sibling  aa_previous_sibling  aa_hidden  aa_element_index             aa_value aa_key
990      div  [\n      Jump to...  [\n, [\n, [\n, <...                   \n  \n      Jump to\...              \n                   \n      False               159               d-none  class
991      div  [\n      Jump to...  [\n, [\n, [\n, <...                   \n  \n      Jump to\...              \n                   \n      False               159       d-on-nav-focus  class
992      div  [\n      Jump to...  [\n, [\n, [\n, <...                   \n  \n      Jump to\...              \n                   \n      False               159  js-jump-to-badge...  class
993     span                  [↵]  [\n      Jump to...  \n      Jump to\...                    ↵              \n  \n      Jump to\...      False               160       d-inline-block  class
994     span                  [↵]  [\n      Jump to...  \n      Jump to\...                    ↵              \n  \n      Jump to\...      False               160                 ml-1  class
995     span                  [↵]  [\n      Jump to...  \n      Jump to\...                    ↵              \n  \n      Jump to\...      False               160       v-align-middle  class
996       ul  [\n, [\n, [No su...  [\n, [\n, [\n, <...                   \n                   \n              \n                   \n      False               161               d-none  class
997       ul  [\n, [\n, [No su...  [\n, [\n, [\n, <...                   \n                   \n              \n                   \n      False               161  js-jump-to-no-re...  class
998       li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162               d-flex  class
999       li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162  flex-justify-center  class
1000      li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162    flex-items-center  class
1001      li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162                   f5  class
1002      li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162               d-none  class
1003      li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162  js-jump-to-sugge...  class
1004      li  [\n, [No suggest...  [\n, [\n, [No su...                   \n                   \n              \n                   \n      False               162                  p-2  class


```