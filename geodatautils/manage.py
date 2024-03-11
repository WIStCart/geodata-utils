"""Manage Solr Instance

Manage Solr instance by updating the index.
"""


__version__ = 2.0


import logging

from geodatautils import config
from .helpers import create_file_list, open_json, RecordSet
from .logging_config import LogFormat
from .solr import Solr
from . import schema


def add(in_path:str, solr_instance_name:str, confirm_action:bool=False, metadata_schema:str=config['metadata-schema']['default']) -> None:
    """Update a Solr instance with the given GeoBlacklight JSONs."""

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Initialize records store
    record_set = RecordSet()

    # Initialize solr instance
    solr = Solr(solr_instance_name)

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    # Check that file_list is not empty
    if len(file_list) < 1:
        logging.info("No documents found in '{}'; exiting.".format(in_path))
        return

    # Load files into records
    logging.info("Opening {} documents.".format(len(file_list)))
    for filepath in file_list:

        # Open the file
        data = open_json(filepath)

        # Add record to record set
        record_set.add_record(data, filepath)

    # Validate schema of records
    logging.info("Validating schema of {} documents.".format(len(file_list)))
    errors = schema.validate(record_set, metadata_schema) or errors

    # Check for errors in records
    logging.info("Checking {} documents for errors.".format(len(file_list)))
    errors = schema.error_check(record_set, solr) or errors

    # Log errors and warnings
    record_set.log_errors_and_warnings(indent=1)

    # Upload records if no errors
    if not errors:

        # Confirm upload if desired
        if confirm_action:
            confirm = input("Are you sure you want to upload {} record{} to instance {}? (y/N)".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))
            if confirm.lower() != "y": 
                logging.info("Operation aborted by user.")
                return

            logging.debug("User confirmed upload. Uploading {} document{} to {}.".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))
        
        else:
            logging.info("Uploading {} document{} to {}.".format(len(file_list), ("" if len(file_list)==1 else "s"), solr_instance_name))

        # Log file names that will be uploaded
        for record in record_set.records.values():
            record.log_record(level='debug', indent=2)

        # Update solr index
        """Note: there is a risk of a time-of-check time-of-use (TOCTOU) error with this code
        structure because we check Solr for duplicates and later upload."""
        data = str(list(map(lambda record: record.data, record_set.records.values()))).encode()
        raw_response = solr.update(data)

        # Raise any errors
        raw_response.raise_for_status()
        
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
    raw_response.raise_for_status()  # Raise any errors
    num_found = raw_response.json()['response']['numFound']

    # Exit if no records to delete
    if num_found == 0:
        logging.info("No matching records found. Exiting.")
        return

    # List matching records
    logging.info("{} record{} will be deleted".format(num_found, ("" if num_found==1 else "s")))
    raw_response = solr.select(q=query, rows=num_found, fl='dc_identifier_s')
    raw_response.raise_for_status()  # Raise any errors
    for doc in raw_response.json()['response']['docs']:
        logging.debug(doc['dc_identifier_s'], extra={'indent': LogFormat.indent(1, tree=True)})
    
    # Confirm deletion if desired
    if confirm_action:
        confirm = input("Are you sure you want to delete {} record{} from instance {}? (y/N)".format(num_found, ("" if num_found==1 else "s"), solr_instance_name))
        if confirm.lower() != "y": 
            logging.info("Operation aborted by user.")
            return

    # Delete records
    solr.delete(q=query)
    logging.info("{} record{} successfully deleted.".format(num_found, ("" if num_found==1 else "s")))