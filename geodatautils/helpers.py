"""Helpers

These are small bits of code that are common to many modules.
"""


import os
import logging
import glob
import json
from typing import Union, ClassVar

from .logging_config import LogFormat


class Error:
    """An error contains an error message and a debug message."""

    def __init__(self, label:str, msg:str, debug:Union[str, None]):
        self.label = label
        self.msg = msg
        self.debug = debug

class Record:
    """Defines a record with a file path and data (JSON contents)."""

    def __init__(self, data: dict, filepath: Union[str, None] = None, set_counts: Union[dict, None] = None) -> None:
        self.filepath = filepath
        self.data = data
        self.errors = []
        self.warnings = []
        self.set_counts = set_counts

    @property
    def has_errors(self) -> int:
        """Returns error count for record."""
        return len(self.errors)
    
    @property
    def has_warnings(self) -> int:
        """Returns warning count for record."""
        return len(self.warnings)

    def add_error(self, label:str, msg:str, debug:Union[str, None]):
        """Add an error to the record."""
        self.errors.append(Error(label, msg, debug))
        self.set_counts['errors'] += 1
    
    def add_warning(self, label:str, msg:str, debug:str):
        """Add an warning to the record."""
        self.warnings.append(Error(label, msg, debug))
        self.set_counts['warnings'] += 1

    def log_record(self, level: str = "debug", indent: int = 1):
        """Log the file name of the record."""
        if level == "info":
            logging.info(self.filepath, extra={'indent': LogFormat.indent(indent)})
        elif level == "debug":
            logging.debug(self.filepath, extra={'indent': LogFormat.indent(indent)})
        else:
            print("Level '{}' is not recognized. Must be 'info' or 'debug'.")

    def log_errors(self, indent: int = 2):
        """Write errors to log."""

        self.log_record(level="info", indent=indent)
        
        for error in self.errors:
            if error.msg: 
                logging.error(error.msg, extra={'indent': LogFormat.indent(indent+1, True), 'label': LogFormat.label(error.label)})
            if error.debug:
                logging.debug(error.debug, extra={'indent': LogFormat.indent(indent+3)})
    
    def log_warnings(self, indent: int = 2):
        """Write warnings to log."""

        self.log_record(level="info", indent=indent)
        
        for warning in self.warnings:
            if warning.msg: 
                logging.warning(warning.msg, extra={'indent': LogFormat.indent(indent+1, True), 'label': LogFormat.label(warning.label)})
            if warning.debug:
                logging.debug(warning.debug, extra={'indent': LogFormat.indent(indent+3)})

class RecordSet:
    """A set of multiple Records.
    
    Attributes:
    records (dict[str, Record]) -- A dictionary with UID as the key and a Record object as the value.
    counts (dict[str, int]) -- A dictionary storing the counts for errors and warnings.
    """

    records: dict[str, Record] = {}

    def __init__(self) -> None:
        self.counts = {
            'errors': 0,
            'warnings': 0
        }

    def add_record(self, data, filepath) -> None:
        self.records[data['dc_identifier_s']] = Record(data, filepath=filepath, set_counts=self.counts)

    def log_errors_and_warnings(self, indent: int = 0) -> None:
        """Log errors and warnings for each record in set."""

        # Initialize stores
        records_with_errors = []
        records_with_warnings = []

        # Collect record uids with errors or warnings
        for uid, record in self.records.items():
            if record.has_errors:
                records_with_errors.append(uid)
            if record.has_warnings:
                records_with_warnings.append(uid)

        # Begin logging
        logging.info("Error and Warning Summary:", extra={'indent': LogFormat.indent(indent)})
        
        # Log errors
        logging.info("{} Error{}{}".format(len(records_with_errors), ("" if len(records_with_errors)==1 else "s"), ("" if len(records_with_errors)==0 else ":")), extra={'indent': LogFormat.indent(indent+1)})
        for uid in records_with_errors:
            self.records[uid].log_errors(indent=indent+2)

        # Log warnings
        logging.info("{} Warning{}{}".format(len(records_with_warnings), ("" if len(records_with_warnings)==1 else "s"), ("" if len(records_with_warnings)==0 else ":")), extra={'indent': LogFormat.indent(indent+1)})
        for uid in records_with_warnings:
            self.records[uid].log_warnings(indent=indent+2)

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
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as e:
            logging.critical("Could not decode JSON: {}".format(file_path))
            logging.debug(e)
            logging.info("Exiting; see log for debug.")
            raise SystemExit
