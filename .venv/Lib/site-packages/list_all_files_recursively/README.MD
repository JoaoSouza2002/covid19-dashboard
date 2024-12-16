# List files recursively

```python
pip install list-all-files-recursively
```



```
    This module provides a function to retrieve information about files in a given folder and its subfolders.

    The function get_folder_file_complete_path takes one or more folder paths as input and returns a list of named tuples.
    Each named tuple contains information about a file found in the folder and its subfolders, including the folder path,
    file name, complete file path, and file extension.

    Example usage:
    folders = [r'C:\cygwin', r'C:/cygwinx']
    file_info_list = get_folder_file_complete_path(folders)
    for file_info in file_info_list:
        print(file_info.path)

    Note: This function only works for local file systems and does not support remote file systems.


    Args:
        folders: A string or a list of strings representing folder paths to retrieve file information from.
        maxsubfolders: An optional integer that limits the maximum number of subfolders to search in each folder.

    Returns:
        A list of named tuples. Each named tuple contains information about a file found in the folder and its subfolders,
        including the folder path, file name, complete file path, and file extension.

    Raises:
        ValueError: If the input folder path is invalid or does not exist.
        TypeError: If the input folders argument is not a string or a list of strings.

```


```python
from list_all_files_recursively import get_folder_file_complete_path
fi = get_folder_file_complete_path(folders=[r'C:\Users\Gamer\anaconda3\bin',r"C:\yolovtest"])
for file in fi[:10]:
    print(file.folder, file.file, file.path, file.ext)
	
	
	
C:\Users\Gamer\anaconda3\bin libLIEF.dll C:\Users\Gamer\anaconda3\bin\libLIEF.dll .dll
C:\Users\Gamer\anaconda3\bin omptarget.dll C:\Users\Gamer\anaconda3\bin\omptarget.dll .dll
C:\Users\Gamer\anaconda3\bin omptarget.rtl.level0.dll C:\Users\Gamer\anaconda3\bin\omptarget.rtl.level0.dll .dll
C:\Users\Gamer\anaconda3\bin omptarget.rtl.opencl.dll C:\Users\Gamer\anaconda3\bin\omptarget.rtl.opencl.dll .dll
C:\yolovtest devi.txt C:\yolovtest\devi.txt .txt
C:\yolovtest\backgroundimages 2022-10-14 13_13_09-.png C:\yolovtest\backgroundimages\2022-10-14 13_13_09-.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_17-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_17-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_39-.png C:\yolovtest\backgroundimages\2022-10-14 13_13_39-.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_46-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_46-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_54-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_54-Window.png .png



from list_all_files_recursively import get_folder_file_complete_path
fi = get_folder_file_complete_path(folders=[r"C:\yolovtest"])
for file in fi[:10]:
    print(file.folder, file.file, file.path, file.ext)
	
	
C:\yolovtest devi.txt C:\yolovtest\devi.txt .txt
C:\yolovtest\backgroundimages 2022-10-14 13_13_09-.png C:\yolovtest\backgroundimages\2022-10-14 13_13_09-.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_17-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_17-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_39-.png C:\yolovtest\backgroundimages\2022-10-14 13_13_39-.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_46-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_46-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_13_54-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_13_54-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 13_14_25-Window.png C:\yolovtest\backgroundimages\2022-10-14 13_14_25-Window.png .png
C:\yolovtest\backgroundimages 2022-10-14 21_29_08-Greenshot.png C:\yolovtest\backgroundimages\2022-10-14 21_29_08-Greenshot.png .png
C:\yolovtest\backgroundimages 2022-10-14 21_29_21-Greenshot.png C:\yolovtest\backgroundimages\2022-10-14 21_29_21-Greenshot.png .png
C:\yolovtest\backgroundimages 2022-10-14 21_29_25-Greenshot.png C:\yolovtest\backgroundimages\2022-10-14 21_29_25-Greenshot.png .png

```
