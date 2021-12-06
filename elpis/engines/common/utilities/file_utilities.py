"""
Collection of utilities for finding and working with files.

Copyright: University of Queensland, 2019
Contributors:
             Nicholas Lambourne - (University of Queensland, 2018)
"""

import glob
import logging
import os
from typing import Set, List


def find_files_by_extensions(set_of_all_files: Set[str], extensions: Set[str]) -> Set[str]:
    """
    Searches for all files in the set of files with the given extensions.
    :param set_of_all_files: set of file names in string format
    :param extensions: file extension being searched for
    :return: set of file_names matched with given extension. if none exists, returns an empty set.
    """
    results = set()
    logging.info(set_of_all_files)
    for file_path in set_of_all_files:
        name, extension = os.path.splitext(file_path)
        logging.info(extension)
        if extension in extensions:
            results.add(file_path)
    return results


def find_first_file_by_extension(set_of_all_files: List[str], extensions: List[str]) -> str:
    """
    Searches for the first file with a given extension in a set of files.
    :param set_of_all_files: set of file names in string format
    :param extensions: file extension being searched for
    :return: name of the first file_name that is matched, if any. otherwise, this method returns an empty string
    """
    for file_ in set_of_all_files:
        name, extension = os.path.splitext(file_)
        if ("*" + extension.lower()) in extensions:
            return file_
    return ""


def find_all_files_in_dir_by_extensions(directory_path: str, extensions: Set[str]) -> Set[str]:
    """
    Find all files with given extensions in a directory recursively
    :param directory_path: path to directory to recursively search
    :param extensions: the set of allowed extensions
    :return: a set of file paths
    """
    path = str(os.path.join(directory_path, "**"))
    all_files_in_dir: Set[str] = set(glob.glob(path, recursive=True))
    return find_files_by_extensions(all_files_in_dir, extensions)
