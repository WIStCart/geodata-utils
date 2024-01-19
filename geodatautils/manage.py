"""Manage Solr Instance

Manage Solr instance by updating the index.
"""


__version__ = 1.1


import logging

from geodatautils import config
from .helpers import create_file_list, open_json
from .logging_config import LogFormat
from .solr import Solr
from . import schema


def add(in_path:str, solr_instance_name:str, confirm_action:bool=False, metadata_schema:str=config['metadata-schema']['default']) -> None:
    """Update a Solr instance with the given GeoBlacklight JSONs."""

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Initialize solr instance
    solr = Solr(solr_instance_name)

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    # Check that file_list is not empty
    if len(file_list) < 1:
        logging.info("No documents found in '{}'; exiting.".format(in_path))
        return

    logging.info("Checking {} documents in {}.".format(len(file_list), in_path))

    # Check each file for errors
    for file_name in file_list:

        # Log the file path
        logging.info(file_name, extra={'indent': LogFormat.indent(1)})

        # Open the file
        data = open_json(file_name)

        # Validate schema
        if not schema.validate(data, metadata_schema):
            errors = True

        # Check for errors
        errors = schema.error_check(data, solr) or errors
    
    # If no errors
    if not errors:

        # Confirm upload if desired
        if confirm_action:
            confirm = input("Are you sure you want to upload {} record{} to instance {}? (y/N)".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))
            if confirm.lower() != "y": 
                logging.info("Operation aborted by user.")
                return

        else:
            logging.info("Uploading {} document{} to {}.".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))

        # Upload each file
        for file_name in file_list:
            """Note: there is a risk of a time-of-check time-of-use (TOCTOU) error with this code
            structure. However, it allows us to minimize the risk of using too much memory while
            also checking all datasets before uploading."""

            # Log the file path
            logging.info(file_name, extra={'indent': LogFormat.indent(1)})

            # Open the file
            data = open_json(file_name)

            # Update solr index
            solr.update(str([data]))
        
        logging.info("Successfully uploaded {} document{} to {}.".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))

    else: 
        logging.warning("Exited with errors; check log.")

def delete(solr_instance_name:str, query:str, confirm_action:bool=False) -> None:
    """Delete records from Solr instance based on query."""

    # Initialize log
    logging.info("Delete from {} where {}".format(solr_instance_name, query))

    # Initialize solr instance
    solr = Solr(solr_instance_name)

    # Get number of records
    """Note: this is vulnerable to time-of-check time-of-use (TOCTOU) errors
    but there is no other way to report how many records will be deleted."""
    raw_response = solr.select(q=query, rows=0)
    num_found = raw_response['response']['numFound']

    # Exit if no records to delete
    if num_found == 0:
        logging.info("No matching records found. Exiting.")
        return

    # List matching records
    logging.info("{} record{} will be deleted".format(num_found, ("" if num_found==1 else "s")))
    for doc in solr.select(q=query, rows=num_found, fl='dc_identifier_s')['response']['docs']:
        logging.info(doc['dc_identifier_s'], extra={'indent': LogFormat.indent(1, tree=True)})
    
    # Confirm deletion if desired
    if confirm_action:
        confirm = input("Are you sure you want to delete {} record{} from instance {}? (y/N)".format(num_found, ("" if num_found==1 else "s"), solr_instance_name))
        if confirm.lower() != "y": 
            logging.info("Operation aborted by user.")
            return

    # Delete records
    solr.delete(q=query)
    logging.info("{} record{} successfully deleted.".format(num_found, ("" if num_found==1 else "s")))