"""Geodata Utilities

A set of utilities to manage the Wisconsin Geodata Geoblacklight instance.
"""


__version__ = "1.2.0"
__author__ = "Hayden Elza"
__license__ = "GPL-3"


import os
import logging
import logging.config
from importlib.resources import files

import yaml


# Set config path
config_path = files('geodatautils.config').joinpath('config.yml')

# Confirm config exists, if not initiate config
if not os.path.exists(config_path):
    os.system("gu_config -i")

# Read in Config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())

# Config logging
logging.config.dictConfig(config['log'])