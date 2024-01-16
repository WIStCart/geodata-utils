"""Tools relating to the schema of geoblacklight records.

See https://opengeometadata.org/ for helpful information on the schemas used in 
geoblacklight.
"""


import logging
import re
from importlib.resources import files
from typing import Union

from jsonschema import validators
from jsonschema.exceptions import SchemaError

from geodatautils import config
from .helpers import open_json
from .logging_config import LogFormat
from .solr import Solr


def empty_missing(data:dict, fields:Union[str, list], label:str=None) -> bool:
    
    # If fields is a string, recast to list
    if type(fields) == str:
        fields = [fields]
    
    # Check each field to see if it is empty or missing
    for field in fields:
        try:
            if data[field] == "": 
                logging.error("'{}' is empty".format(field), extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(label)})
                return True
        
        except KeyError:
            logging.error("Required field '{}' was not found.".format(field), extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(label)})
            return True
    
    # If no fields are empty or missing
    return False


def error_check(data:dict, solr:Solr) -> bool:
    """Check for errors in a GeoBlacklight JSON file.
    
    Arguments:
    data (dict) -- contents of the geoblacklight JSON file
    solr (Solr) -- initilized solr object (geodatautils.solr.Solr)

    Returns:
    errors (bool) -- True if there were errors; False if no errors occured
    """
    # TODO: much of this function can be replace by the schema validation in most recent validator versions
    # For example: required and not empty

    # Initialize error tracker
    errors = False

    # Fields are not null
    if 'properties-not-null' in config['error-checks'] and type(config['error-checks']['properties-not-null']) == list:
        fields = config['error-checks']['properties-not-null']
        for field in fields:
            if empty_missing(data, field, 'properties-not-null'):
                errors = True

    # Check that dc_identifier_s and layer_slug_s match
    error_check_name = 'identifier-layer-slug-match'
    if config['error-checks'][error_check_name] and not empty_missing(data, ['dc_identifier_s', 'layer_slug_s'], error_check_name):
        if data['dc_identifier_s'] != data['layer_slug_s']:
            logging.error("'dc_identifier_s' and 'layer_slug_s' do not match", extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error_check_name)})
            logging.debug("'{}', '{}'".format(data['dc_identifier_s'], data['layer_slug_s']), extra={'indent': LogFormat.indent(3)})
            errors = True

    # Check that dct_temporal_sm contains solr_year_i
    error_check_name = 'temporal-contains-solr-year'
    if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dct_temporal_sm'], error_check_name):
        if not any(str(data['solr_year_i']) in item for item in data['dct_temporal_sm']):
            logging.error("'dct_temporal_sm' does not contain 'solr_year_i'", extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error_check_name)})
            logging.debug("'{}', '{}'".format(data['dct_temporal_sm'], data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
            errors = True

    # Check that dc_title_s contains solr_year_i 
    error_check_name = 'title-contains-solr-year'
    if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dc_title_s'], error_check_name):
        if str(data['solr_year_i']) not in data['dc_title_s']:
            logging.error("'dc_title_s' does not contain 'solr_year_i'", extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error_check_name)})
            logging.debug("'{}', '{}'".format(data['dc_title_s'], data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
            errors = True

    # Check that dct_references_s['http://schema.org/downloadUrl\'] contains solr_year_i
    error_check_name = 'references-contains-solr-year'
    if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dct_references_s'], error_check_name):
        regex = '(?<=downloadUrl":").+?([^\/]+?)(?=")'
        matches = re.findall(regex, data['dct_references_s'])

        if not any(str(data['solr_year_i']) in match for match in matches):
            logging.error("""'dct_references_s["http://schema.org/downloadUrl"]' does not contain 'solr_year_i'""", extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error_check_name)})
            logging.debug("{}, '{}'".format(matches, data['solr_year_i']), extra={'indent': LogFormat.indent(3)})
            errors = True

    # Check for existing UID (`dc_identifier_s`) in current Solr index
    error_check_name = 'existing-uid'
    if config['error-checks'][error_check_name] and not empty_missing(data, ['dc_identifier_s'], error_check_name):
        raw_response = solr.select(q=data['dc_identifier_s'])
        records_found = raw_response['response']['numFound']
        if records_found > 0:
            logging.error("""'dc_identifier_s' already exists in the Solr index.""", extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label(error_check_name)})
            logging.debug("{} records found for '{}'".format(records_found, data['dc_identifier_s']), extra={'indent': LogFormat.indent(3)})
            errors = True

    return errors


def validate(data:dict, schema_name:str) -> bool:
    """Validate GeoBlacklight JSON schema."""

    # Load schema from config
    schema_path = files('geodatautils.config.schemas').joinpath(config['metadata-schema']['options'][schema_name])
    schema = open_json(schema_path)

    # Set validator
    validator = validators.validator_for(schema)
    v = validator(schema)

    # Validate schema
    try:
        validator.check_schema(schema)
    except SchemaError as e:
        logging.error("Schema Error: the input schema '{}' is not valid".format(schema), extra={'indent': LogFormat.indent(2, True)})

    # If schema of data is invlaid
    if not v.is_valid(data):

        # Log validator in debug
        logging.debug("Using '{}' validator".format(validator.__name__), extra={'indent': LogFormat.indent(2)})
        
        # Log errors
        for error in v.iter_errors(data):
            for suberror in sorted(error.context, key=lambda e: e.schema_path)[:-1]:
                logging.error("{}: {}".format(":".join(map(str,list(suberror.schema_path))), suberror.message), extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label("schema-validation")})

        return False
    
    # If schema of data is valid
    else:
        return True