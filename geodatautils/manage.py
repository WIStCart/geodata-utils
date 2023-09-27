from .helpers import create_file_list, open_json
import logging
from pprint import pprint

__version__ = 1.0

def upload():
    return

def error_check(data):

    # Initialize error tracker
    errors = False

    # Fields are not null
    fields = ['dc_title_s', 'dc_identifier_s', 'layer_slug_s', 'solr_geom', 'dct_provenance_s', 'dc_rights_s', 'geoblacklight_version', 'dc_creator_sm', 'dc_description_s', 'dct_references_s', 'dct_temporal_sm', 'solr_year_i', 'layer_modified_dt']
    for field in fields:
        if data[field] == "": 
            logging.error("{} is empty".format(field))
            errors = True

    # Check that dc_identifier_s and layer_slug_s match
    if data['dc_identifier_s'] != data['layer_slug_s']:
        logging.error("'dc_identifier_s' and 'layer_slug_s' do not match")
        errors = True
    
    # Check that dct_temporal_sm contains solr_year_i
    if str(data['solr_year_i']) not in data['dct_temporal_sm'][0]:
        logging.error("'dct_temporal_sm' does not contain 'solr_year_i'")
        errors = True

    # Check that dc_title_s contains solr_year_i 
    if str(data['solr_year_i']) not in data['dc_title_s']:
        logging.error("'dc_title_s' does not contain 'solr_year_i'")
        errors = True


    

    return errors
    


def update(in_path):

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    # For each file
    for file_name in file_list:
        logging.info("Checking {}".format(file_name))
        data = open_json(file_name)
        errors = error_check(data) or errors

        # break

    print("Upload?", not errors)