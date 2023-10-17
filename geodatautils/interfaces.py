"""Geodata Utility Interfaces

Command line interfaces for Geodata utilites.
"""


import argparse
import logging

import geodatautils.manage
from geodatautils import config


def update_solr():
    """Update Solr
    
    Update a solr instance. Add records, remove records.
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
        "-a", "--addFolder",
        help="Indicate path to folder with GeoBlacklight JSON files that will be uploaded.")
    group.add_argument(
        "-d", "--delete",
        help="Delete the provided unique record ID (layer_slug) from the Solr index.")
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
        help="Recurse into subfolders when adding JSON files.")

    # Print version
    parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(geodatautils.manage.__version__))

    # Parse arguments
    args = parser.parse_args()

    # Set logger name
    logging.getLogger().setLevel(logging.DEBUG)

    # Run tools
    if any([args.delete, args.delete_collection, args.delete_provenance, args.purge]):
        print("Not implemented yet. Exiting.")
    elif args.addFolder:
        geodatautils.manage.add(args.addFolder, solr_instance_name=args.instance)
    else:  # This shouldn't happen
        print("No tool selected")
