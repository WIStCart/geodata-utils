"""Helpers

These are small bits of code that are common to many modules.
"""

def create_file_list(in_path:str) -> list:
    """Given a path that could be a file or directory, return a list of all 
    possible JSON file paths. 
    
    If the in path is a JSON file, this is a list with a single item. If the 
    in path is a directory, the list is every JSON file within the directory 
    including within subdirectories.
    """

    import os
    import logging
    import glob

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

    import json

    with open(file_path) as f:
        return json.load(f)

class LogFormat:
    """Helper class to format log entries."""

    def indent(level, tree=False):
        """Indent with tabs with the option of a tree prefix."""
        return "\t"*level*2 + ("└── " if tree else "")
    
    def spaces(n):
        """Generate a specified number of spaces."""
        return " "*n
