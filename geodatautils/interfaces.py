import geodatautils
import argparse
import logging

def update_solr():

    # Create argument parser
    
    parser = argparse.ArgumentParser()

    # Mandatory argument
    parser.add_argument("inPath", help="Path to geoblacklight JSON or directory of JSONs.")
    # parser.add_argument("outPath", help="Output path to place updated geojsons.")

    # Optional arguments
    # parser.add_argument("-p", "--precision", help="How many digits after the decimial (default=4)", dest='precision', type=int, default=4)
    # parser.add_argument("-i", "--indent", help="Indent level. (default=None)", dest='indentation', type=int, default=None)
    # parser.add_argument("-s", "--skip-feature", help="Gracefully skip feature instead of entire dataset if there is an unsupported geometry type.", dest='skip_feature', action='store_true')
    # parser.add_argument("-v", "--verbose", help="Write successful precision changes to log as well.", dest='verbose', action='store_true')

    # Print version
    parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(geodatautils.manage.__version__))

    # Parse arguments
    args = parser.parse_args()

    # Set logger name
    logging.getLogger().setLevel(logging.DEBUG)

    # Run update
    geodatautils.manage.update(args.inPath)