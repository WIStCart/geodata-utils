"""Tools for configuring Geodata Utilities."""


import os
import shutil

import geodatautils


def edit():
    # Open config text editor
    config_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config.yml")
    os.system(config_path)

def init():
    # Copy template
    template_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config-template.yml")
    config_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config.yml")
    shutil.copyfile(template_path, config_path)

    # Open config text editor
    os.system(config_path)