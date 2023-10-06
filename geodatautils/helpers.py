"""
Helpers
"""



def create_file_list(in_path:str) -> list:
    """
    Given a path that could be a file or directory, return a list of all 
    possible JSON file paths. 
    
    If the in path is a JSON file, this is a list with a single item. If the 
    in path is a directory, the list is every JSON file within the directory 
    including within subdirectories.
    """

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
    
def open_json(file_path:str) -> dict:
    """
    Given a file path to a JSON file, return the JSON loaded into a dictionary.
    """

    import json

    with open(file_path) as f:
        return json.load(f)

class Solr:

    def __init__(self, instance_name) -> None:

        from geodatautils import config
        self.url = config['solr instances'][instance_name]['url']
        self.username = config['solr instances'][instance_name]['username']
        self.password = config['solr instances'][instance_name]['password']
        
        # connection = pysolr.Solr(solr_instance_config['url'], timeout=1800, auth=HTTPBasicAuth(SOLR_USERNAME, SOLR_PASSWORD))
        pass

    def select(self, q='', fl=''):
        import requests  # I chose requests over urllib because although it adds another dependency, it greatly simplifies working with solr
        from requests.compat import urljoin

        select_url = urljoin(self.url, 'select/')

        parameters = [
            ('q', q),
            ('fl', fl)
        ]
        
        raw_response = requests.get(select_url, params=parameters, auth=(self.username, self.password)).json()

        return raw_response


class LogFormat:
    """
    Helper class to format log entries.
    """
    def indent(level, tree=False):
        return "\t"*level*2 + ("└── " if tree else "")
