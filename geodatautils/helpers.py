"""Helpers

These are small bits of code that are common to many modules.
"""


import os
import logging
import glob
import json

from .logging_config import LogFormat


class Error:
    """An error contains an error message and a debug message."""

    def __init__(self, label:str, msg:str, debug:str):
        self.label = label
        self.msg = msg
        self.debug = debug

class Record:
    """Defines a record with a file path and data (JSON contents)."""

    def __init__(self, data:dict, filepath:str=None) -> None:
        self.filepath = filepath
        self.data = data
        self.errors = []
        self.warnings = []

    @property
    def has_errors(self) -> bool:
        """True if record has errors."""
        return (True if self.errors else False)
    
    @property
    def has_warnings(self) -> bool:
        """True if record has warnings."""
        return (True if self.warnings else False)

    def add_error(self, label:str, msg:str, debug:str):
        """Add an error to the record."""
        self.errors.append(Error(label, msg, debug))
    
    def add_warning(self, label:str, msg:str, debug:str):
        """Add an warning to the record."""
        self.warnings.append(Error(label, msg, debug))

    def log_record(self, level:str="debug"):
        """Log the file name of the record."""
        if level == "info":
            logging.info(self.filepath, extra={'indent': LogFormat.indent(1)})
        elif level == "debug":
            logging.debug(self.filepath, extra={'indent': LogFormat.indent(1)})
        else:
            print("Level '{}' is not recognized. Must be 'info' or 'debug'.")

    def log_errors(self):
        """Write errors to log."""

        self.log_record(level="info")
        
        for error in self.errors:
            if error.msg: 
                logging.error(error.msg, extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error.label)})
            if error.debug:
                logging.debug(error.debug, extra={'indent': LogFormat.indent(3)})
    
    def log_warnings(self):
        """Write warnings to log."""

        self.log_record(level="info")
        
        for warning in self.warnings:
            if warning.msg: 
                logging.warning(warning.msg, extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(warning.label)})
            if warning.debug:
                logging.debug(warning.debug, extra={'indent': LogFormat.indent(3)})

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
        return [file_name for file_name in glob.glob(in_path+"/**/*.json", recursive=True)]
    
    # Other?
    else:
        logging.error("'{}' is not a file or directory", in_path)
        raise SystemExit

def open_json(file_path:str) -> dict:
    """Given a file path to a JSON file, return the JSON loaded into a dictionary."""

    with open(file_path, encoding="utf8") as f:
        return json.load(f)