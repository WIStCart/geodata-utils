"""Geodata Utilities

A set of utilities to manage the Wisconsin Geodata Geoblacklight instance.
"""


__version__ = "1.3.2"
__author__ = "Hayden Elza"
__license__ = "GPL-3"


import os
import logging
import logging.config
from importlib.resources import files

import yaml

from . import config_tools


# Set config path
config_path = files('geodatautils.config').joinpath('config.yml')

# Confirm config exists, if not initiate config
if not os.path.exists(config_path):
    config_tools.init()

# Read in Config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())

# Config logging
logging.config.dictConfig(config['log'])