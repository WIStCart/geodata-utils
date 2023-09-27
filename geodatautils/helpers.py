# Helpers

def create_file_list(in_path):

    import os
    import logging
    import glob

    # Check if path exists; if not, exit
    if not os.path.exists(in_path):
        logging.error("'{}' is not a file or directory".format(in_path))
        raise SystemExit

    # If path is a file
    if os.path.isfile(in_path):
        return [in_path]

    # If path is a directory
    elif os.path.isdir(in_path):
        return [file_name for file_name in glob.glob(in_path+"**/*.json", recursive=True)]
    
    # Other?
    else:
        logging.error("'{}' is not a file or directory", in_path)
        raise SystemExit
    
def open_json(file_path):
    import json

    with open(file_path) as f:
        return json.load(f)
    
class logFormat:
    def indent(level, tree=False):
        return "\t"*level*2 + ("└── " if tree else "")
    
