"""Geodata Utility Interfaces

Command line interfaces for Geodata utilites.
"""


import argparse
import logging

from geodatautils import config, __version__
from . import config_tools
from . import manage
from . import indextools


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
        config_tools.edit()
    
    elif args.init:
        config_tools.init()

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

    # Optional arguments
    parser.add_argument(
        "-r", "--recursive",
        action='store_true',
        help="[Deprecated] Recurse into subfolders when adding JSON files.")

    # Print version
    parser.add_argument("--version", action="version", version="Geodata Utils - Version {}".format(__version__))

    # Parse arguments
    args = parser.parse_args()

    # Set logger level
    logging.getLogger().setLevel(logging.DEBUG)

    # Deprecation warning
    if args.recursive:
        logging.warning('The "-r" recursive option is deprecated and no longer used by script. Using -a will add either a file or a directory recursively.')

    # Run tools
    if args.add:
        manage.add(args.add, solr_instance_name=args.instance, confirm_action=True)
    elif args.purge:
        manage.delete(solr_instance_name=args.instance, query="*:*", confirm_action=True)
    elif args.delete:
        manage.delete(solr_instance_name=args.instance, query="layer_slug_s:{}".format(args.delete), confirm_action=True)
    elif args.delete_collection:
        manage.delete(solr_instance_name=args.instance, query='dct_isPartOf_sm:"{}"'.format(args.delete_collection), confirm_action=True)
    elif args.delete_provenance:
        manage.delete(solr_instance_name=args.instance, query='dct_provenance_s:"{}"'.format(args.delete_provenance), confirm_action=True)
    else:  # This shouldn't happen
        print("No tool selected")

def indexed():
    """Manage Indexed Datasets
    
    Tools for indexed datasets used in geodata@wisc.
    """

    def check_urls(args):
        indextools.check_urls(args.searchPath, args.verbose)

    # Create argument parser
    parser = argparse.ArgumentParser(prog='indexed')
    subparsers = parser.add_subparsers(title="subcommands",
                                       description="This program uses several subcommands. Use the help for each for more information.")

    # Coordinate precision subparser
    parser_p = subparsers.add_parser(
        "coordinate-precision", aliases=['p'],
        help="Read indexed dataset GeoJSON, reduce coordinate precision, and output to specified directory.")

    # Check URLs subparser
    parser_cu = subparsers.add_parser(
        "check-urls", aliases=['cu'],
        help="Check URLs in GeoJSON of indexed datasets to confirm they resolve.")
    parser_cu.add_argument("searchPath", help="Path to geojson or geojsons.")
    parser_cu.add_argument("-v", "--verbose", action='store_true', dest="verbose", help="Write successful responses to log.")
    parser_cu.set_defaults(func=check_urls)

    # Minify GeoJSON subparser
    parser_m = subparsers.add_parser(
        "minify-geojson", aliases=['m'],
        help="Minify geojson to have no return/new lines and no indentation. Optionally choose an indentation level.")

    # Update URL subparser
    parser_uu = subparsers.add_parser(
        "update-url", aliases=['uu'],
        help="Update websiteUrl of geojson to specified new URL.")

    # Remove missing tiles subparser
    parser_rt = subparsers.add_parser(
        "remove-missing-tiles", aliases=['rt'],
        help="Remove tiles from index geojson where downloadUrl returns 404.")

    # Print version
    parser.add_argument("--version", action="version", version="Geodata Utils - Version {}".format(__version__))

    # Parse arguments
    args = parser.parse_args()
    args.func(args)
