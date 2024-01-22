"""Tools relating to the schema of geoblacklight records.

See https://opengeometadata.org/ for helpful information on the schemas used in 
geoblacklight.
"""


import logging
from importlib.resources import files
from typing import Union

from jsonschema import validators
from jsonschema.exceptions import SchemaError

from geodatautils import config
from .helpers import open_json, Record
from .logging_config import LogFormat
from .solr import Solr


def empty_missing(data:dict, fields:Union[str, list]) -> str:
    """Check if a required fields are present in geoblacklight JSON.

    Arguments:
    data (dict) -- contents of the geoblacklight JSON file
    fields (str|list) -- field name or list of field names

    Returns:
    empty_missing (str) -- Outputs None|"empty"|"missing"
    """
    
    # If fields is a string, recast to list
    if type(fields) == str:
        fields = [fields]
    
    # Check each field to see if it is empty or missing
    for field in fields:
        try:
            if data[field] == "":
                return "empty"
        
        except KeyError:
            return "missing"
    
    # If no fields are empty or missing
    return None

def error_check(records:list[Record], solr:Solr) -> bool:
    """Check for errors in a GeoBlacklight JSON file.
    
    Arguments:
    records (list[Record]) -- a list of Solr records
    solr (Solr) -- initilized solr object (geodatautils.solr.Solr)

    Returns:
    errors (bool) -- True if there were errors; False if no errors occured
    """
    # TODO: much of this function can be replace by the schema validation in most recent validator versions
    # For example: required and not empty

    # Initialize error tracker
    errors = False

    # For each record run checks
    for record in records:

        data = record.data

        # Fields are not null
        if 'properties-not-null' in config['error-checks'] and type(config['error-checks']['properties-not-null']) == list:
            fields = config['error-checks']['properties-not-null']
            for field in fields:
                error = empty_missing(data, field)
                
                if error:
                    # Compose message
                    if error == "empty":
                        msg = "'{}' is empty".format(field)
                    elif error == "missing":
                        msg = "Required field '{}' was not found.".format(field)

                    # Add error to record
                    record.add_error('properties-not-null', msg, None)        

        # Check that dc_identifier_s and layer_slug_s match
        error_check_name = 'identifier-layer-slug-match'
        if config['error-checks'][error_check_name] and not empty_missing(data, ['dc_identifier_s', 'layer_slug_s']):
            if data['dc_identifier_s'] != data['layer_slug_s']:
                record.add_error(error_check_name, "'dc_identifier_s' and 'layer_slug_s' do not match", "'{}', '{}'".format(data['dc_identifier_s'], data['layer_slug_s']))
                

        # Check that dct_temporal_sm contains solr_year_i
        error_check_name = 'temporal-contains-solr-year'
        if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dct_temporal_sm']):
            if not any(str(data['solr_year_i']) in item for item in data['dct_temporal_sm']):
                record.add_error(error_check_name, "'dct_temporal_sm' does not contain 'solr_year_i'", "'{}', '{}'".format(data['dct_temporal_sm'], data['solr_year_i']))

        # Check that dc_title_s contains solr_year_i 
        error_check_name = 'title-contains-solr-year'
        if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dc_title_s']):
            if str(data['solr_year_i']) not in data['dc_title_s']:
                record.add_error(error_check_name, "'dc_title_s' does not contain 'solr_year_i'", "'{}', '{}'".format(data['dc_title_s'], data['solr_year_i']))

        # Check that dct_references_s contains solr_year_i
        error_check_name = 'references-contains-solr-year'
        if config['error-checks'][error_check_name] and not empty_missing(data, ['solr_year_i', 'dct_references_s']):

            if not str(data['solr_year_i']) in data['dct_references_s']:
                record.add_warning(error_check_name, """'dct_references_s' does not contain 'solr_year_i'""", "{}, '{}'".format(data['dct_references_s'], data['solr_year_i']))
        
        # Log any errors or warnings else log the record for debug
        if record.has_errors:
            record.log_errors()
            errors = True
        if record.has_warnings:
            record.log_warnings()
        if not record.has_errors and record.has_warnings:
            record.log_record()

    # Check for existing UID (`dc_identifier_s`) in current Solr index
    error_check_name = 'existing-uid'
    if config['error-checks'][error_check_name]:

        # Check that no UIDs are empty or missing
        if not any(map(lambda record: empty_missing(record.data, ['dc_identifier_s']), records)):
            
            # Build UID list
            uid_list = list(map(lambda record: record.data['dc_identifier_s'], records))

            # Initialize records store
            records_found = []

            # Break filter query into chunks (neccessary when processing large numbers of JSONs all at once)
            fq_chunks = solr.build_query_chunks(uid_list, solr.max_uri_size)

            # Query each chunk
            for fq_chunk in fq_chunks:

                filter_query = "dc_identifier_s:({})".format(fq_chunk)

                # Query 
                raw_response = solr.select(fq=filter_query, fl='dc_identifier_s', rows=len(records))

                # Raise any errors
                raw_response.raise_for_status()

                # Store any matching records for logging later
                if raw_response.json()['response']['numFound']:
                    records_found.append([doc['dc_identifier_s'] for doc in raw_response.json()['response']['docs']])

            # Error if any matching records are found
            if records_found:
                logging.error("{} matching records found in the {} index.".format(len(records_found), solr.name), extra={'indent': LogFormat.indent(1), 'label': LogFormat.label(error_check_name)})
                
                for record_uid in records_found:
                    logging.debug(record_uid, extra={'indent': LogFormat.indent(2, tree=True)})
                
                errors = True
    
        else:
            logging.error("Aborted UID check because at least one UID is empty or missing from an input record.", extra={'indent': LogFormat.indent(1), 'label': LogFormat.label(error_check_name)})
            errors = True

    return errors

def validate(records:list[Record], schema_name:str) -> bool:
    """Validate GeoBlacklight JSON schema.
    
    Returns:
    errors (bool) -- False if all schemas are valid, True if at least one of 
        the schemas is invalid.
    """

    # Initialize error tracker
    errors = False

    # Validate each record
    for record in records:

        data = record.data

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

            # Log the file path
            logging.info(record.filepath, extra={'indent': LogFormat.indent(1)})

            # Log validator in debug
            logging.debug("Using '{}' validator".format(validator.__name__), extra={'indent': LogFormat.indent(2)})
            
            # Log errors
            for error in v.iter_errors(data):
                for suberror in sorted(error.context, key=lambda e: e.schema_path)[:-1]:
                    logging.error("{}: {}".format(":".join(map(str,list(suberror.schema_path))), suberror.message), extra={'indent': LogFormat.indent(2, True), 'label': LogFormat.label("schema-validation")})

            errors = True
        
        else: 
            # Log the file path
            logging.debug(record.filepath, extra={'indent': LogFormat.indent(1)})
    
    return errors