"""Geodata Utilities

A set of utilities to manage the Wisconsin Geodata Geoblacklight instance.
"""


__version__ = "1.0"
__author__ = "Hayden Elza"
__license__ = "GPL-3"


import logging
import logging.config
from importlib.resources import files

import yaml


# Read in Config
with open(files('geodatautils.config').joinpath('config.yml'), 'r') as f:
    config = yaml.safe_load(f.read())

# Config logging
logging.config.dictConfig(config['log'])