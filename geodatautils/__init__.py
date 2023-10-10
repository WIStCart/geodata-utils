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

# Set default indent value so that it does not need to be specified
class CustomFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'indent'):
            record.indent = " "
        return True
logging.getLogger().addFilter(CustomFilter())
