"""Geodata Utility Interfaces

Command line interfaces for Geodata utilites.
"""


import argparse
import logging
import os
import shutil

import geodatautils.manage
from geodatautils import config


def gu_config():
    """Configure Geodata Utilites"""

    # Create argument parser
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-e", "--edit",
        action='store_true',
        help="Open Geodata Utilities config file for editing.")
    group.add_argument(
        "-i", "--init",
        action='store_true',
        help="Initiate Geodata Utilities config file and open for editing.")

    # Parse arguments
    args = parser.parse_args()

    # Run tools
    if args.edit:

        # Open config text editor
        config_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config.yml")
        os.system(config_path)
    
    elif args.init:

        # Copy template
        template_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config-template.yml")
        config_path = os.path.join(os.path.dirname(geodatautils.__file__), "config", "config.yml")
        shutil.copyfile(template_path, config_path)

        # Open config text editor
        os.system(config_path)

def update_solr():
    """Update Solr
    
    Interface to update a solr instance. Add records, remove records.
    """

    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required arguments
    instance_choices = list(config['solr instances'].keys())
    parser.add_argument(
        "-i", "--instance",
        choices = instance_choices,
        help="Identify which instance of Solr to use.",
        required=True)

    # Required exclusive group (one and only one from group)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-a", "--add",
        help="Indicate path to a single file or folder with GeoBlacklight JSON files that will be uploaded.")
    group.add_argument(
        "-d", "--delete",
        help="Delete the provided unique record ID (layer_slug_s) from the Solr index.")
    group.add_argument(
        "-dc", "--delete-collection",
        help="Remove an entire collection from the Solr index.")
    group.add_argument(
        "-dp", "--delete-provenance",
        help="Remove all records from Solr index that belong to the specified provenance.")
    group.add_argument(
        "-p", "--purge",
        action='store_true',
        help="Delete the entire Solr index.")

    # Optoinal arguments
    parser.add_argument(
        "-r", "--recursive",
        action='store_true',
        help="[Deprecated] Recurse into subfolders when adding JSON files.")

    # Print version
    parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(geodatautils.manage.__version__))

    # Parse arguments
    args = parser.parse_args()

    # Set logger level
    logging.getLogger().setLevel(logging.DEBUG)

    # Deprecation warning
    if args.recursive:
        logging.warning('The "-r" recursive option is deprecated and no longer used by script. Using -a will add either a file or a directory recursively.')

    # Run tools
    if args.add:
        geodatautils.manage.add(args.add, solr_instance_name=args.instance, confirm_action=True)
    elif args.purge:
        geodatautils.manage.delete(solr_instance_name=args.instance, query="*:*", confirm_action=True)
    elif args.delete:
        geodatautils.manage.delete(solr_instance_name=args.instance, query="layer_slug_s:{}".format(args.delete), confirm_action=True)
    elif args.delete_collection:
        geodatautils.manage.delete(solr_instance_name=args.instance, query='dct_isPartOf_sm:"{}"'.format(args.delete_collection), confirm_action=True)
    elif args.delete_provenance:
        geodatautils.manage.delete(solr_instance_name=args.instance, query='dct_provenance_s:"{}"'.format(args.delete_provenance), confirm_action=True)
    else:  # This shouldn't happen
        print("No tool selected")