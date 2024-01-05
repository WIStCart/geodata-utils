"""Tools relating to the schema of geoblacklight records.

See https://opengeometadata.org/ for helpful information on the schemas used in 
geoblacklight.
"""


import logging
import re
from importlib.resources import files

from jsonschema import validate as jsonschemavalidate

from geodatautils import config
from .helpers import open_json
from .logging_config import LogFormat
from .solr import Solr


def error_check(data:dict, solr:Solr) -> bool:
    """Check for errors in a GeoBlacklight JSON file."""

    # Initialize error tracker
    errors = False

    # Fields are not null
    fields = ['dc_title_s', 'dc_identifier_s', 'layer_slug_s', 'solr_geom', 'dct_provenance_s', 'dc_rights_s', 'geoblacklight_version', 'dc_creator_sm', 'dc_description_s', 'dct_references_s', 'dct_temporal_sm', 'solr_year_i', 'layer_modified_dt']
    for field in fields:
        try:
            if data[field] == "": 
                logging.error("'{}' is empty".format(field), extra={'indent': LogFormat.indent(2, True)})
                errors = True
        except KeyError:
            logging.error("Required field '{}' was not found.".format(field), extra={'indent': LogFormat.indent(2, True)})
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


def validate(data:dict, schema_name:str) -> bool:
    """Validate GeoBlacklight JSON schema."""

    # Load schema from config
    schema_path = files('geodatautils.config.schemas').joinpath(config['metadata-schema']['options'][schema_name])
    schema = open_json(schema_path)

    # Compare data to schema
    jsonschemavalidate(instance=data, schema=schema)