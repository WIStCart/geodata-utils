"""Logging Config

Filters and helpers to format logging as desired."""
import logging

class DefaultIndent(logging.Filter, ):
    """Logging filter to allow the indent property to not be specified."""
    def filter(self, record):
        """Set default indent value so that it does not need to be specified"""
        if not hasattr(record, 'indent'):
            record.indent = " "
        return True
    
class LogFormat:
    """Helper class to format log entries."""

    def indent(level, tree=False):
        """Indent with tabs with the option of a tree prefix."""
        return "\t"*level*2 + ("└── " if tree else "")
    
    def spaces(n):
        """Generate a specified number of spaces."""
        return " "*n
