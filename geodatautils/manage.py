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


def _error_check(data, solr):
    """Check for errors in a GeoBlacklight JSON file."""

    # Initialize error tracker
    errors = False

    # Fields are not null
    fields = ['dc_title_s', 'dc_identifier_s', 'layer_slug_s', 'solr_geom', 'dct_provenance_s', 'dc_rights_s', 'geoblacklight_version', 'dc_creator_sm', 'dc_description_s', 'dct_references_s', 'dct_temporal_sm', 'solr_year_i', 'layer_modified_dt']
    for field in fields:
        if data[field] == "": 
            logging.error("{} is empty".format(field), extra={'indent': LogFormat.indent(2, True)})
            errors = True

    # Check that dc_identifier_s and layer_slug_s match
    if data['dc_identifier_s'] != data['layer_slug_s']:
        logging.error("'dc_identifier_s' and 'layer_slug_s' do not match", extra={'indent': LogFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dc_identifier_s'], data['layer_slug_s']), extra={'indent': LogFormat.indent(3)})
        errors = True

    # Check that dct_temporal_sm contains solr_year_i
    if not any(str(data['solr_year_i']) in item for item in data['dct_temporal_sm']):
        logging.error("'dct_temporal_sm' does not contain 'solr_year_i'", extra={'indent': LogFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dct_temporal_sm'], data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
        errors = True

    # Check that dc_title_s contains solr_year_i 
    if str(data['solr_year_i']) not in data['dc_title_s']:
        logging.error("'dc_title_s' does not contain 'solr_year_i'", extra={'indent': LogFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dc_title_s'], data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
        errors = True

    # Check that solr_year_i is in dct_references_s['http://schema.org/downloadUrl\']
    regex = '(?<=downloadUrl":").+?([^\/]+?)(?=")'
    matches = re.findall(regex, data['dct_references_s'])

    if not any(str(data['solr_year_i']) in match for match in matches):
        logging.error("""'dct_references_s["http://schema.org/downloadUrl"]' does not contain 'solr_year_i'""", extra={'indent': LogFormat.indent(2, True)})
        logging.debug("{}, '{}'".format(matches, data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
        errors = True

    # Check for existing UID (`dc_identifier_s`) in current Solr index
    raw_response = solr.select(q=data['dc_identifier_s'])
    records_found = raw_response['response']['numFound']
    if records_found > 0:
        logging.error("""'dc_identifier_s' already exists in the Solr index.""", extra={'indent': LogFormat.indent(2, True)})
        logging.debug("{} records found for '{}'".format(records_found, data['dc_identifier_s']), extra={'indent': LogFormat.indent(3)})
        errors = True

    return errors
    

def update(in_path, solr_instance_name):
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
        errors = _error_check(data, solr) or errors
    
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