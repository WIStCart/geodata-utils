"""Helpers

These are small bits of code that are common to many modules.
"""


import os
import logging
import glob
import json


def create_file_list(in_path:str) -> list:
    """Given a path that could be a file or directory, return a list of all 
    possible JSON file paths. 
    
    If the in path is a JSON file, this is a list with a single item. If the 
    in path is a directory, the list is every JSON file within the directory 
    including within subdirectories.
    """

    # Check if path exists; if not, exit
    if not os.path.exists(in_path):
        logging.error("'{}' is not a file or directory".format(in_path))
        raise SystemExit

    # If path is a file
    if os.path.isfile(in_path):
        return [in_path]

    # If path is a directory
    elif os.path.isdir(in_path):
        return [file_name for file_name in glob.glob(in_path+"**/*.json", recursive=True)]
    
    # Other?
    else:
        logging.error("'{}' is not a file or directory", in_path)
        raise SystemExit


def open_json(file_path:str) -> dict:
    """Given a file path to a JSON file, return the JSON loaded into a dictionary."""

    with open(file_path, encoding="utf8") as f:
        return json.load(f)