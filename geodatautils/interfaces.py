"""Geodata Utility Interfaces

Command line interfaces for Geodata utilites.
"""


import argparse
import logging

import geodatautils.manage
from geodatautils import config


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
        geodatautils.manage.add(args.add, solr_instance_name=args.instance)
    elif args.purge:
        geodatautils.manage.delete(solr_instance_name=args.instance, query="*:*")
    elif args.delete:
        geodatautils.manage.delete(solr_instance_name=args.instance, query="layer_slug_s:{}".format(args.delete))
    elif args.delete_collection:
        geodatautils.manage.delete(solr_instance_name=args.instance, query='dct_isPartOf_sm:"{}"'.format(args.delete_collection))
    elif args.delete_provenance:
        geodatautils.manage.delete(solr_instance_name=args.instance, query='dct_provenance_s:"{}"'.format(args.delete_provenance))
    else:  # This shouldn't happen
        print("No tool selected")
