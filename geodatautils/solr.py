"""Solr Interface

Connect to a Solr instance so that you can select or update documents.
"""

class Solr:
    """Create an object representing a connection to a Solr instance."""

    def __init__(self, instance_name:str) -> None:
        """Initiate Solr object with settings from config."""

        from geodatautils import config
        self.url = config['solr instances'][instance_name]['url']
        self.username = config['solr instances'][instance_name]['username']
        self.password = config['solr instances'][instance_name]['password']

    def select(self, q:str='', fl:str='') -> dict:
        """Select records based on query and field list."""

        import requests  # I chose requests over urllib because although it adds another dependency, it greatly simplifies working with solr
        from requests.compat import urljoin

        select_url = urljoin(self.url, 'select/')

        parameters = [
            ('q', q),
            ('fl', fl)
        ]
        
        raw_response = requests.get(select_url, params=parameters, auth=(self.username, self.password)).json()

        return raw_response