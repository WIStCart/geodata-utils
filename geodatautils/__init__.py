# from . import manage
import os
import logging
import logging.config
import yaml


# Metadata
__version__ = "0.1"
__author__ = "Hayden Elza"
__license__ = "GPL-3"


# Read in Config
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, '../config/config.yml'), 'r') as f:
    config = yaml.safe_load(f.read())

# Config logging
logging.config.dictConfig(config['log'])