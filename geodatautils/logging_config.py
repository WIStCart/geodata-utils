"""Logging Config

Filters and helpers to format logging as desired."""


import logging


class DefaultIndent(logging.Filter, ):
    """Logging filter to allow optional properties to not be specified."""

    def filter(self, record):
        """Set default values so that they do not need to be specified"""
        if not hasattr(record, 'indent'):
            record.indent = " "
        if not hasattr(record, 'label'):
            record.label = ""
        return True
  
    
class LogFormat:
    """Helper class to format log entries."""

    @staticmethod
    def indent(level:int, tree:bool=False):
        """Indent with tabs with the option of a tree prefix."""
        return "\t"*level*2 + ("└── " if tree else "")

    @staticmethod
    def label(label:str):
        """Add label to log entry. E.g., '(some-function)'"""
        return "(" + label + ") "
    
    @staticmethod
    def spaces(n):
        """Generate a specified number of spaces."""
        return " "*n
