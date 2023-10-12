from .helpers import create_file_list, open_json, LogFormat
from .solr import Solr
from . import schema
import logging
import re

__version__ = 1.0


def error_check(data):

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
    # TODO: check if solr_year_i in any dct_temporal_sm
    if str(data['solr_year_i']) not in data['dct_temporal_sm'][0]:
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




    

    return errors
    

def update(in_path, solr_instance):

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    logging.info("Checking {} documents in {}.".format(len(file_list), in_path), extra={'indent': LogFormat.spaces(1)})

    # For each file
    for file_name in file_list:

        # Log the file path
        logging.info(file_name, extra={'indent': LogFormat.indent(1)})

        # Open the file
        data = open_json(file_name)

        # Validate schema
        schema.validate(data, 'geoblacklight-1-no_enum')

        # Check for errors
        errors = error_check(data) or errors

        # break
    
    # If no errors
    if not errors:

        logging.info("Uploading {} documents to {}.".format(len(file_list), solr_instance), extra={'indent': LogFormat.spaces(1)})
        
        for file_name in file_list:
            logging.info(file_name, extra={'indent': LogFormat.indent(1)})


    else: 
        print("Exited with errors; check log.")