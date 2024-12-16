```python
#as dataframe
#pip install a-pandas-ex-xml2df

#### UPDATE 08.12.2022 - xpath / snippets 

from a_pandas_ex_xml2df import pd_add_read_xml_files, xml_to_dict, xml_to_df
import pandas as pd
pd_add_read_xml_files()
df=pd.Q_Xml2df('https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml',add_xpath_and_snippet=True)
print(df[1:6].to_string())
                                aa_all_keys                                        aa_value                                                                                                           aa_file                          aa_xpath                                                              aa_snippet
1  (artist, 0, album, 0, description, link)  http://en.wikipedia.org/wiki/The_King_of_Limbs  https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml  //artist[1]/album[1]/description     <description link="http://en.wikipedia.org/wiki/The_King_of_Limbs">
2    (artist, 0, album, 0, song, 0, length)                                            5:15  https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml      //artist[1]/album[1]/song[1]                                     <song length="5:15" title="Bloom"/>
3     (artist, 0, album, 0, song, 0, title)                                           Bloom  https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml      //artist[1]/album[1]/song[1]                                     <song length="5:15" title="Bloom"/>
4    (artist, 0, album, 0, song, 1, length)                                            4:41  https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml      //artist[1]/album[1]/song[2]                         <song length="4:41" title="Morning Mr Magpie"/>
5     (artist, 0, album, 0, song, 1, title)                               Morning Mr Magpie  https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml      //artist[1]/album[1]/song[2]                         <song length="4:41" title="Morning Mr Magpie"/>

 

from a_pandas_ex_xml2df import pd_add_read_xml_files, xml_to_dict, xml_to_df
import pandas as pd
pd_add_read_xml_files()
df=pd.Q_Xml2df('https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml')

pd.Q_Xml2df('https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml')
Out[4]: 
                                                                                                     aa_all_keys                                           aa_value
level_0 level_1 level_2 level_3 level_4     level_5     level_6                                                                                                    
artist  0       album   0.0     description description NaN      (artist, 0, album, 0, description, description)  \n\tThe King of Limbs is the eighth studio alb...
                                            link        NaN             (artist, 0, album, 0, description, link)     http://en.wikipedia.org/wiki/The_King_of_Limbs
                                song        0           length            (artist, 0, album, 0, song, 0, length)                                               5:15
                                                        title              (artist, 0, album, 0, song, 0, title)                                              Bloom
                                            1           length            (artist, 0, album, 0, song, 1, length)                                               4:41
                                                                                                          ...                                                ...
        1       album   1.0     song        9           title              (artist, 1, album, 1, song, 9, title)                                        Magic Doors
                                            10          length           (artist, 1, album, 1, song, 10, length)                                               5:45
                                                        title             (artist, 1, album, 1, song, 10, title)                                            Threads
                                title       NaN         NaN                         (artist, 1, album, 1, title)                                              Third
                name    NaN     NaN         NaN         NaN                                    (artist, 1, name)                                         Portishead
[98 rows x 2 columns]



#dataframe and dict
xmlfileorstrin11 = r"C:\Users\Gamer\Documents\Downloads\00000001_untouched.xml"
link='https://gist.githubusercontent.com/jasonbaldridge/2597611/raw/c2c6a072c7d018c35aefad6b4739ac75247e5d92/music.xml'

uu1=xml_to_dict(xmlfileorstrin11)
uu11=xml_to_df(xmlfileorstrin11)

with open(xmlfileorstrin11,encoding='utf-8') as f:
    xmlfileorstring = f.read()
uu2=xml_to_dict(xmlfileorstrin11)
uu22=xml_to_df(xmlfileorstrin11)

uu3=xml_to_dict(link)
uu33=xml_to_df(link)

uu1
Out[12]: 
{'folder': 'data',
 'filename': '00000001_untouched.png',
 'path': None,
 'source': {'database': 'Unknown'},
 'size': {'width': 1920, 'height': 1080, 'depth': 3},
 'segmented': 0,
 'object': [{'name': 'search_bar',
   'pose': 'Unspecified',
   'truncated': 0,
   'occluded': 0,
   'difficult': 0,
   'bndbox': {'xmin': 753, 'ymin': 8, 'xmax': 1172, 'ymax': 52}},
  {'name': 'home_text',
   'pose': 'Unspecified',
   'truncated': 0,
   'occluded': 0,
   'difficult': 0,
   'bndbox': {'xmin': 42, 'ymin': 5, 'xmax': 158, 'ymax': 55}},
  {'name': 'add_friends',
   'pose': 'Unspecified',
   'truncated': 0,
   'occluded': 0,
   'difficult': 0,
   'bndbox': {'xmin': 44, 'ymin': 185, 'xmax': 152, 'ymax': 310}}]}
   
uu11
Out[14]: 
                                                    aa_all_keys                aa_value
level_0   level_1  level_2   level_3                                                   
filename  NaN      NaN       NaN                    (filename,)  00000001_untouched.png
folder    NaN      NaN       NaN                      (folder,)                    data
object    0        bndbox    xmax     (object, 0, bndbox, xmax)                    1172
                             xmin     (object, 0, bndbox, xmin)                     753
                             ymax     (object, 0, bndbox, ymax)                      52
                             ymin     (object, 0, bndbox, ymin)                       8
                   difficult NaN         (object, 0, difficult)                       0
                   name      NaN              (object, 0, name)              search_bar
                   occluded  NaN          (object, 0, occluded)                       0
                   pose      NaN              (object, 0, pose)             Unspecified
                   truncated NaN         (object, 0, truncated)                       0
          1        bndbox    xmax     (object, 1, bndbox, xmax)                     158
                             xmin     (object, 1, bndbox, xmin)                      42
                             ymax     (object, 1, bndbox, ymax)                      55
                             ymin     (object, 1, bndbox, ymin)                       5
                   difficult NaN         (object, 1, difficult)                       0
                   name      NaN              (object, 1, name)               home_text
                   occluded  NaN          (object, 1, occluded)                       0
                   pose      NaN              (object, 1, pose)             Unspecified
                   truncated NaN         (object, 1, truncated)                       0
          2        bndbox    xmax     (object, 2, bndbox, xmax)                     152
                             xmin     (object, 2, bndbox, xmin)                      44
                             ymax     (object, 2, bndbox, ymax)                     310
                             ymin     (object, 2, bndbox, ymin)                     185
                   difficult NaN         (object, 2, difficult)                       0
                   name      NaN              (object, 2, name)             add_friends
                   occluded  NaN          (object, 2, occluded)                       0
                   pose      NaN              (object, 2, pose)             Unspecified
                   truncated NaN         (object, 2, truncated)                       0
path      NaN      NaN       NaN                        (path,)                    None
segmented NaN      NaN       NaN                   (segmented,)                       0
size      depth    NaN       NaN                  (size, depth)                       3
          height   NaN       NaN                 (size, height)                    1080
          width    NaN       NaN                  (size, width)                    1920
source    database NaN       NaN             (source, database)                 Unknown   


```
