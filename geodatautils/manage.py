from .helpers import create_file_list, open_json, logFormat
import logging
import re

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
            logging.error("{} is empty".format(field), extra={'indent': logFormat.indent(2, True)})
            errors = True

    # Check that dc_identifier_s and layer_slug_s match
    if data['dc_identifier_s'] != data['layer_slug_s']:
        logging.error("'dc_identifier_s' and 'layer_slug_s' do not match", extra={'indent': logFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dc_identifier_s'], data['layer_slug_s']), extra={'indent': logFormat.indent(3)})
        errors = True

    # Check that dct_temporal_sm contains solr_year_i
    if str(data['solr_year_i']) not in data['dct_temporal_sm'][0]:
        logging.error("'dct_temporal_sm' does not contain 'solr_year_i'", extra={'indent': logFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dct_temporal_sm'], data['solr_year_i']), extra={'indent': logFormat.indent(3)})
        errors = True

    # Check that dc_title_s contains solr_year_i 
    if str(data['solr_year_i']) not in data['dc_title_s']:
        logging.error("'dc_title_s' does not contain 'solr_year_i'", extra={'indent': logFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(data['dc_title_s'], data['solr_year_i']), extra={'indent': logFormat.indent(3)})
        errors = True

    # Check that solr_year_i is in dct_references_s['http://schema.org/downloadUrl\']
    if str(data['solr_year_i']) not in re.search('(?<=downloadUrl\\":\\")(?:.*?)([^\/]+(?=\\",))', data['dct_references_s']).group(1):
        logging.error("""'dct_references_s["http://schema.org/downloadUrl"]' does not contain 'solr_year_i'""", extra={'indent': logFormat.indent(2, True)})
        logging.debug("'{}', '{}'".format(re.search('(?<=downloadUrl\\":\\")(?:.*?)([^\/]+(?=\\",))', data['dct_references_s']).group(1), data['solr_year_i']), extra={'indent': logFormat.indent(3)})
        errors = True



    

    return errors
    


def update(in_path):

    # Initialize error tracker, tracks if any errors have been found. If so, program will stop before pushing to solr
    errors = False

    # Get list of geoblacklight json files to process
    file_list = create_file_list(in_path)

    # For each file
    for file_name in file_list:
        logging.info(file_name, extra={'indent': logFormat.indent(1)})
        data = open_json(file_name)
        errors = error_check(data) or errors

        # break

    print("Upload?", not errors)