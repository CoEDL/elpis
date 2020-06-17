"""
Collection of utilities for working with JSON files.

Copyright: University of Queensland, 2019
Contributors:
             Nicholas Lambourne - (University of Queensland, 2018)
             Ben Foley - (University of Queensland, 2020)
"""

import json
import os
import sys
from _io import TextIOWrapper
from typing import List, Dict, Union


def load_json_file(file_name: str) -> List[Dict[str, str]]:
    """
    Given a filename (parameter) containing JSON, load and
    return the a list of python dictionaries with containing the same information.
    :param file_name: name of file containing JSON to read from.
    :return a Python dictionary with the contents of the JSON file.
    """
    data = []
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, "r", encoding="utf-8") as file_:
            data = json.load(file_)
    return data


def write_data_to_json_file(data: object = None,
                            file_name: Union[str, TextIOWrapper] = None) -> None:
    """
    Writes the given Python dictionary (or list) object to a JSON file at the the given
    output location (which can either be a file - specified as a string, or
    directed to an output like sys.stdout or sys.stderr).
    :param data: the Python dictionary to be converted to JSON and written.
    :param file_name: the file to write the dictionary contents to.
    """
    if not data:
        data = dict()
    if not file_name:
        file_name = sys.stdout
    json_data_string = json.dumps(data,
                                  indent=4,
                                  separators=(',', ': '),
                                  sort_keys=False)
    if isinstance(file_name, str):
        with open(file_name, "w") as file:
            file.write(json_data_string)
    else:
        print(json_data_string, file=file_name, flush=True)
