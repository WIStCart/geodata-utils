from . import manage
import logging
import logging.config
import yaml

# Metadata
__version__ = "0.1"
__author__ = "Hayden Elza"
__license__ = "GPL-3"

# Load environment
from dotenv import load_dotenv
load_dotenv()

from os import getenv
# version = getenv('VERSION')

# Logging
with open('config/logging.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)