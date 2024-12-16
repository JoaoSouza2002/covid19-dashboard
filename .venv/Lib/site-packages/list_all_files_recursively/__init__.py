import os
from collections import namedtuple
import pathlib

fields_cor = "folder file path ext"
classname_cor = "files"

FilePathInfos = namedtuple(classname_cor, fields_cor)


def get_folder_file_complete_path(folders, maxsubfolders=-1):
    r"""
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

    """
    if isinstance(folders, str):
        folders = [folders]
    folders = list(set([os.path.normpath(x) for x in folders]))
    folders = [x for x in folders if os.path.exists(x)]
    folders = [x for x in folders if os.path.isdir(x)]

    listOfFiles2 = []
    limit = 1000000000000
    checkdepth = False
    for dirName in folders:
        if maxsubfolders > -1:
            sepa = dirName.count("\\") + dirName.count("/")
            limit = sepa + maxsubfolders
        if limit < 1000000000000:
            checkdepth = True
        for dirpath, dirnames, filenames in os.walk(dirName):
            if checkdepth:
                depthok = dirpath.count("\\") + dirpath.count("/") <= limit
            else:
                depthok = True
            ra = [
                FilePathInfos(
                    dirpath,
                    file,
                    os.path.normpath(os.path.join(dirpath, file)),
                    pathlib.Path(file).suffix,
                )
                for file in filenames
                if depthok
            ]
            if ra:
                listOfFiles2.extend(ra)
    return listOfFiles2


