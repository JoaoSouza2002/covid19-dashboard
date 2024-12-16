# Use the power of pandas to manage the files on your Android device

```python
pip install a-pandas-ex-adb-to-df
```

```python
################################################
#Update 2022/12/06:

# select individual folder
df = pd.Q_adb_to_df(device=deviceserial,adb_path=adb_path, folder='data/') # will automatically switch to su

################################################
#Update 2022/12/05:
# Added ff_pull_file_cat to pull files that usually need su rights, which is not possible using "adb pull" (Maybe it is, but I haven't 
# found a way)

# Make sure to exclude folders and symlinks when you copy files using cat:
df.loc[(df.aa_symlink.isna()) & (df.aa_size > 0) & (~df.aa_rights.str.contains('^d'))].ff_pull_file_cat.apply(lambda x:x('f:\\gvbadsasww', timeout=15))
################################################


################################################
#Update 2022/11/22:
################################################
#you can now pull files (folders will be created if they don't exist)
for key, item in dff.loc[(dff.aa_size > 10) & (dff.aa_size < 200) & (~dff.aa_filename.str.contains('->')) & (~dff.aa_filename.str.contains('/tmp'))].iterrows():
    try:
        item.ff_pull_file(f'f:\\keyboardstuffxx2')
    except Exception:
        pass
        
#and remove files 
for key, item in dff.loc[dff.aa_fullpath.str.contains(r'tmp.*\.bin') & dff.aa_folder.str.contains(r'sdcard/')].iterrows():
    try:
        item.ff_remove_file()
    except Exception:
        pass
################################################
from a_pandas_ex_adb_to_df import pd_add_adb_to_df
import pandas as pd
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5745"
pd_add_adb_to_df()
df = pd.Q_adb_to_df(device=deviceserial,adb_path=adb_path)
print(df)


print(df.loc[df.aa_fullpath.str.contains(r'download.*_.*\.mp4',na=False,regex=True, flags=re.IGNORECASE)][:5].to_string())

                                          aa_filename                    aa_folder                                                                aa_fullpath   aa_id  aa_index   aa_rights  aa_links aa_owner  aa_group  aa_size             aa_date
634994                               von_haus_aus.mp4  storage/emulated/0/Download                               storage/emulated/0/Download/von_haus_aus.mp4  140306      5428  -rwxrwx---         1  u0_a219  media_rw  5552768 2022-03-21 17:31:00
634995                            ins_haus_stehen.mp4  storage/emulated/0/Download                            storage/emulated/0/Download/ins_haus_stehen.mp4  186233      6328  -rwxrwx---         1  u0_a219  media_rw  6471958 2022-03-21 17:31:00
634996                            aufs_haus_gehen.mp4  storage/emulated/0/Download                            storage/emulated/0/Download/aufs_haus_gehen.mp4  126498      6588  -rwxrwx---         1  u0_a219  media_rw  6738374 2022-03-21 17:31:00
634997               mit_der_tuer_ins_haus_fallen.mp4  storage/emulated/0/Download               storage/emulated/0/Download/mit_der_tuer_ins_haus_fallen.mp4  130773      6832  -rwxrwx---         1  u0_a219  media_rw  6989353 2022-03-21 17:31:00
635004  Alfredo_stiftete_seinen_Lieferwagen_final.mp4  storage/emulated/0/Download  storage/emulated/0/Download/Alfredo_stiftete_seinen_Lieferwagen_final.mp4  136706      5104  -rw-rw----         1  u0_a219  media_rw  5219973 2022-06-01 22:58:00



```
