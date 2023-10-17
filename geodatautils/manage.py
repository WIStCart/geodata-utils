"""Manage Solr Instance

Manage Solr instance by updating the index.
"""


__version__ = 1.0


import logging
import re

from .helpers import create_file_list, open_json
from .logging_config import LogFormat
from .solr import Solr
from . import schema


def add(in_path, solr_instance_name):
    """Update a Solr instance with the given GeoBlacklight JSONs."""

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Initialize solr instance
    solr = Solr(solr_instance_name)

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    logging.info("Checking {} documents in {}.".format(len(file_list), in_path))

    # For each file
    for file_name in file_list:

        # Log the file path
        logging.info(file_name, extra={'indent': LogFormat.indent(1)})

        # Open the file
        data = open_json(file_name)

        # Validate schema
        schema.validate(data, 'geoblacklight-1-no_enum')

        # Check for errors
        errors = schema.error_check(data, solr) or errors
    
    # If no errors
    if not errors:

        logging.info("Uploading {} documents to {}.".format(len(file_list), solr_instance_name))
        
        # For each file
        for file_name in file_list:
            """Note: there is a risk of a time-of-check time-of-use (TOCTOU) error with this code
            structure. However, it allows us to minimize the risk of using too much memory while
            also checking all datasets before uploading."""

            # Log the file path
            logging.info(file_name, extra={'indent': LogFormat.indent(1)})

            # Open the file
            data = open_json(file_name)

            # Update solr index
            solr.update([data])

    else: 
        logging.warning("Exited with errors; check log.")