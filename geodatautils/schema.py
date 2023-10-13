"""Tools relating to the schema of geoblacklight records.

See https://opengeometadata.org/ for helpful information on the schemas used in 
geoblacklight.
"""

import logging

from jsonschema import validate as jsonschemavalidate

from geodatautils import config
from .helpers import open_json


def validate(data:dict, schema_name:str) -> bool:
    """Validate GeoBlacklight JSON schema."""

    # Load schema from config
    schema_path = config['metadata-schemas'][schema_name]
    schema = open_json(schema_path)

    # Compare data to schema
    jsonschemavalidate(instance=data, schema=schema)