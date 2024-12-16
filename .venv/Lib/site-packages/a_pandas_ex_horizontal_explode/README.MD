# Explode list/tuples in columns 

```python
pip install a-pandas-ex-horizontal-explode
```

```python
from a_pandas_ex_horizontal_explode import pd_add_horizontal_explode
pd_add_horizontal_explode()
import pandas as pd
df = pd.Series(
    [
        ("enabled_previews_v1", "type", 0),
        ("enabled_previews_v1", "version", 0),
        True,
        ("enabled_previews_v1", "type", 0),
        ("enabled_previews_v1", 0),
        ("locale", 0),
        ("properties", "property_key", 0),
        ("properties", "property_value", 0),
        ("properties",),
        ("resume", "package_name", 0),
        ("resume", "stack", 0),
        ("resume", "timestamp", 0),
        ("resume", "external", 0),
        ("android_metadata", "locale", 0),
        ("android_metadata", "locale", 0),
        ("android_metadata", "locale", 0),
        33,
        ("_sync_state", "_id", 0),
    ]
)
df2 = df.to_frame()
df2.columns=['aa']

dfex = df.ds_horizontal_explode(concat=True)
print(dfex.to_string())

dfex2 = df2.ds_horizontal_explode('aa',concat=False)
print(dfex2.to_string())


                                    0                  0_0             0_1   0_2
0      (enabled_previews_v1, type, 0)  enabled_previews_v1            type     0
1   (enabled_previews_v1, version, 0)  enabled_previews_v1         version     0
2                                True                 <NA>            <NA>  <NA>
3      (enabled_previews_v1, type, 0)  enabled_previews_v1            type     0
4            (enabled_previews_v1, 0)  enabled_previews_v1               0  <NA>
5                         (locale, 0)               locale               0  <NA>
6       (properties, property_key, 0)           properties    property_key     0
7     (properties, property_value, 0)           properties  property_value     0
8                       (properties,)           properties            <NA>  <NA>
9           (resume, package_name, 0)               resume    package_name     0
10                 (resume, stack, 0)               resume           stack     0
11             (resume, timestamp, 0)               resume       timestamp     0
12              (resume, external, 0)               resume        external     0
13      (android_metadata, locale, 0)     android_metadata          locale     0
14      (android_metadata, locale, 0)     android_metadata          locale     0
15      (android_metadata, locale, 0)     android_metadata          locale     0
16                                 33                 <NA>            <NA>  <NA>
17              (_sync_state, _id, 0)          _sync_state             _id     0
                   aa_0            aa_1  aa_2
0   enabled_previews_v1            type     0
1   enabled_previews_v1         version     0
2                  <NA>            <NA>  <NA>
3   enabled_previews_v1            type     0
4   enabled_previews_v1               0  <NA>
5                locale               0  <NA>
6            properties    property_key     0
7            properties  property_value     0
8            properties            <NA>  <NA>
9                resume    package_name     0
10               resume           stack     0
11               resume       timestamp     0
12               resume        external     0
13     android_metadata          locale     0
14     android_metadata          locale     0
15     android_metadata          locale     0
16                 <NA>            <NA>  <NA>
17          _sync_state             _id     0

```
