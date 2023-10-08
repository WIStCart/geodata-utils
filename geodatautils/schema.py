"""Tools relating to the schema of geoblacklight records.

See https://opengeometadata.org/ for helpful information on the schemas used in 
geoblacklight.
"""

import logging

def validate(data:dict, schema_name:str) -> bool:

    from geodatautils import config
    from .helpers import open_json
    from jsonschema import validate, ValidationError

    # Load schema from config
    schema_path = config['metadata-schemas'][schema_name]
    schema = open_json(schema_path)

    # Compare data to schema
    validate(instance=data, schema=schema)